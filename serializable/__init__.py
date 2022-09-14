# encoding: utf-8

# This file is part of py-serializable
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Paul Horton. All Rights Reserved.
import enum
import functools
import inspect
import json
import logging
import re
import typing  # noqa: F401
import warnings
from copy import copy
from decimal import Decimal
from io import StringIO, TextIOWrapper
from json import JSONEncoder
from sys import version_info
from typing import Any, Callable, Dict, Iterable, List, Optional, Set, Tuple, Type, TypeVar, Union, cast
from xml.etree import ElementTree

if version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol  # type: ignore[misc]

from .formatters import BaseNameFormatter, CurrentFormatter
from .helpers import BaseHelper

logger = logging.getLogger('serializable')
logger.setLevel(logging.INFO)


class _Klass(Protocol):
    __qualname__: str


_F = TypeVar("_F", bound=Callable[..., Any])
_T = TypeVar('_T', bound=_Klass)


@enum.unique
class SerializationType(str, enum.Enum):
    """
    Enum to define the different formats supported for serialization and deserialization.
    """
    JSON = 'JSON'
    XML = 'XML'


_DEFAULT_SERIALIZATION_TYPES = [SerializationType.JSON, SerializationType.XML]


@enum.unique
class XmlArraySerializationType(enum.Enum):
    """
    Enum to differentiate how array-type properties (think Iterables) are serialized.

    Given a ``Warehouse`` has a property ``boxes`` that returns `List[Box]`:

    ``FLAT`` would allow for XML looking like:

    ``
    <warehouse>
        <box>..box 1..</box>
        <box>..box 2..</box>
    </warehouse>
    ``

    ``NESTED`` would allow for XML looking like:

    ``
    <warehouse>
        <boxes>
            <box>..box 1..</box>
            <box>..box 2..</box>
        </boxes>
    </warehouse>
    ``
    """
    FLAT = 1
    NESTED = 2


def _allow_property_for_view(prop_info: 'ObjectMetadataLibrary.SerializableProperty',
                             view_: Optional[Type[Any]]) -> bool:
    if prop_info.name == 'address':
        print(f'{prop_info.name} for {view_} vs {prop_info.views}')

    if view_:
        if prop_info.views and view_ in prop_info.views:
            return True
        elif not prop_info.views:
            return True
    else:
        if prop_info.views:
            return False
        else:
            return True


class _SerializableJsonEncoder(JSONEncoder):
    """
    ``serializable``'s custom implementation of ``JSONEncode``.

    You don't need to call this directly - it is all handled for you by ``serializable``.
    """

    def __init__(self, *, skipkeys: bool = False, ensure_ascii: bool = True, check_circular: bool = True,
                 allow_nan: bool = True, sort_keys: bool = False, indent: Optional[int] = None,
                 separators: Optional[Tuple[str, str]] = None, default: Optional[Callable] = None,
                 view_: Optional[Type[Any]] = None) -> None:
        super().__init__(
            skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular, allow_nan=allow_nan,
            sort_keys=sort_keys, indent=indent, separators=separators, default=default
        )
        self._view = view_

    @property
    def view(self) -> Optional[Type[Any]]:
        return self._view

    def default(self, o: Any) -> Any:
        # Enum
        if isinstance(o, enum.Enum):
            return o.value

        # Iterables
        if isinstance(o, (list, set)):
            return list(o)

        # Classes
        if isinstance(o, object):
            d: Dict[Any, Any] = {}
            klass_qualified_name = f'{o.__module__}.{o.__class__.__qualname__}'
            serializable_property_info = ObjectMetadataLibrary.klass_property_mappings.get(klass_qualified_name, {})

            # Handle remaining Properties that will be sub elements
            for k, prop_info in serializable_property_info.items():
                if not _allow_property_for_view(prop_info=prop_info, view_=self._view):
                    # Skip as rendering for a view and this Property is not registered form this View
                    continue

                v = getattr(o, k)

                # Ignore None values by default
                if v is None:
                    continue

                new_key = BaseNameFormatter.decode_handle_python_builtins_and_keywords(name=k)

                if prop_info.custom_names.get(SerializationType.JSON, None):
                    new_key = prop_info.custom_names.get(SerializationType.JSON)

                if CurrentFormatter.formatter:
                    new_key = CurrentFormatter.formatter.encode(property_name=new_key)

                if prop_info.custom_type:
                    if prop_info.is_helper_type():
                        v = prop_info.custom_type.serialize(v)
                    else:
                        v = prop_info.custom_type(v)
                elif prop_info.is_array:
                    if len(v) > 0:
                        v = list(v)
                    else:
                        v = None
                elif prop_info.is_enum:
                    v = str(v.value)
                elif not prop_info.is_primitive_type():
                    if isinstance(v, Decimal):
                        if prop_info.string_format:
                            v = float(f'{v:{prop_info.string_format}}')
                        else:
                            v = float(v)
                    else:
                        global_klass_name = f'{prop_info.concrete_type.__module__}.{prop_info.concrete_type.__name__}'
                        if global_klass_name not in ObjectMetadataLibrary.klass_mappings:
                            if prop_info.string_format:
                                v = f'{v:{prop_info.string_format}}'
                            else:
                                v = str(v)

                if new_key == '.':
                    return v

                if v is not None:
                    d.update({new_key: v})

            return d

        # Fallback to default
        super().default(o=o)


def _as_json(self: _T, view_: Optional[Type[Any]] = None) -> str:
    """
    Internal function that is injected into Classes that are annotated for serialization and deserialization by
    ``serializable``.
    """
    logging.debug(f'Dumping {self} to JSON with view: {view_}...')
    return json.dumps(self, cls=_SerializableJsonEncoder, view_=view_)


def _from_json(cls: Type[_T], data: Dict[str, Any]) -> object:
    """
    Internal function that is injected into Classes that are annotated for serialization and deserialization by
    ``serializable``.
    """
    logging.debug(f'Rendering JSON to {cls}...')
    klass = ObjectMetadataLibrary.klass_mappings.get(f'{cls.__module__}.{cls.__qualname__}', None)
    klass_properties = ObjectMetadataLibrary.klass_property_mappings.get(f'{cls.__module__}.{cls.__qualname__}', {})

    if klass is None:
        warnings.warn(f'{cls.__module__}.{cls.__qualname__} is not a known serializable class')
        return None

    _data = copy(data)
    for k, v in data.items():
        decoded_k = CurrentFormatter.formatter.decode(property_name=k)
        if decoded_k in klass.ignore_during_deserialization:
            logger.debug(f'Ignoring {k} when deserializing {cls.__module__}.{cls.__qualname__}')
            del _data[k]
            continue

        new_key = None
        if decoded_k not in klass_properties:
            for p, pi in klass_properties.items():
                if pi.custom_names.get(SerializationType.JSON, None) == decoded_k:
                    new_key = p
        else:
            new_key = decoded_k

        if new_key is None:
            raise ValueError(f'Unexpected key {k} in data being serialized to {cls.__module__}.{cls.__qualname__}')

        del (_data[k])
        _data[new_key] = v

    for k, v in _data.items():
        prop_info = klass_properties.get(k, None)
        if not prop_info:
            raise ValueError(f'No Prop Info for {k} in {cls}')

        if prop_info.custom_type:
            if prop_info.is_helper_type():
                _data[k] = prop_info.custom_type.deserialize(v)
            else:
                _data[k] = prop_info.custom_type(v)
        elif prop_info.is_array:
            items = []
            for j in v:
                if not prop_info.is_primitive_type():
                    items.append(prop_info.concrete_type.from_json(data=j))
                else:
                    items.append(prop_info.concrete_type(j))
            _data[k] = items
        elif prop_info.is_enum:
            _data[k] = prop_info.concrete_type(v)
        elif not prop_info.is_primitive_type():
            global_klass_name = f'{prop_info.concrete_type.__module__}.{prop_info.concrete_type.__name__}'
            if global_klass_name in ObjectMetadataLibrary.klass_mappings:
                _data[k] = prop_info.concrete_type.from_json(data=v)
            else:
                _data[k] = prop_info.concrete_type(v)

    logging.debug(f'Creating {cls} from {_data}')

    return cls(**_data)


def _as_xml(self: _T, view_: Type[Any] = None, as_string: bool = True, element_name: Optional[str] = None,
            xmlns: Optional[str] = None) -> Union[ElementTree.Element, str]:
    logging.debug(f'Dumping {self} to XML with view {view_}...')

    this_e_attributes = {}
    klass_qualified_name = f'{self.__module__}.{self.__class__.__qualname__}'
    serializable_property_info = {k: v for k, v in sorted(
        ObjectMetadataLibrary.klass_property_mappings.get(klass_qualified_name, {}).items(),
        key=lambda i: i[1].xml_sequence)}

    for k, v in self.__dict__.items():
        # Remove leading _ in key names
        new_key = k[1:]
        if new_key.startswith('_') or '__' in new_key:
            continue
        new_key = BaseNameFormatter.decode_handle_python_builtins_and_keywords(name=new_key)

        # Ignore Nones
        if not v:
            continue

        if new_key in serializable_property_info:
            prop_info = serializable_property_info.get(new_key)

            if not _allow_property_for_view(prop_info=prop_info, view_=view_):
                # Skip as rendering for a view and this Property is not registered form this View
                continue

            if prop_info and prop_info.is_xml_attribute:
                new_key = prop_info.custom_names.get(SerializationType.XML, new_key)
                if CurrentFormatter.formatter:
                    new_key = CurrentFormatter.formatter.encode(property_name=new_key)

                if prop_info.custom_type and prop_info.is_helper_type():
                    v = prop_info.custom_type.serialize(v)
                elif prop_info.is_enum:
                    v = v.value

                this_e_attributes.update({new_key: str(v)})

    element_name = _namespace_element_name(tag_name=element_name,
                                           xmlns=xmlns) if element_name else _namespace_element_name(
        tag_name=CurrentFormatter.formatter.encode(self.__class__.__name__), xmlns=xmlns)
    this_e = ElementTree.Element(element_name, this_e_attributes)

    # Handle remaining Properties that will be sub elements
    for k, prop_info in serializable_property_info.items():
        # Skip if rendering for a View and this Property is not designated for this View
        if not _allow_property_for_view(prop_info=prop_info, view_=view_):
            continue

        v = getattr(self, k)

        # Ignore None values by default
        if v is None:
            continue

        new_key = BaseNameFormatter.decode_handle_python_builtins_and_keywords(name=k)

        if not prop_info:
            raise ValueError(f'{new_key} is not a known Property for {klass_qualified_name}')

        if not prop_info.is_xml_attribute:
            new_key = prop_info.custom_names.get(SerializationType.XML, new_key)

            if new_key == '.':
                this_e.text = str(v)
                continue

            if CurrentFormatter.formatter:
                new_key = CurrentFormatter.formatter.encode(property_name=new_key)
            new_key = _namespace_element_name(tag_name=new_key, xmlns=xmlns)

            if prop_info.custom_type:
                if prop_info.is_helper_type():
                    ElementTree.SubElement(this_e, new_key).text = str(prop_info.custom_type.serialize(v))
                else:
                    ElementTree.SubElement(this_e, new_key).text = str(prop_info.custom_type(v))
            elif prop_info.is_array and prop_info.xml_array_config:
                _array_type, nested_key = prop_info.xml_array_config
                nested_key = _namespace_element_name(tag_name=nested_key, xmlns=xmlns)
                if _array_type and _array_type == XmlArraySerializationType.NESTED and len(v) > 0:
                    nested_e = ElementTree.SubElement(this_e, new_key)
                else:
                    nested_e = this_e

                for j in v:
                    if not prop_info.is_primitive_type() and not prop_info.is_enum:
                        nested_e.append(j.as_xml(view_=view_, as_string=False, element_name=nested_key, xmlns=xmlns))
                    elif prop_info.is_enum:
                        ElementTree.SubElement(nested_e, nested_key).text = str(j.value)
                    elif prop_info.concrete_type in (float, int):
                        ElementTree.SubElement(nested_e, nested_key).text = str(j)
                    elif prop_info.concrete_type is bool:
                        ElementTree.SubElement(nested_e, nested_key).text = str(j).lower()
                    else:
                        # Assume type is str
                        ElementTree.SubElement(nested_e, nested_key).text = str(j)
            elif prop_info.is_enum:
                ElementTree.SubElement(this_e, new_key).text = str(v.value)
            elif not prop_info.is_primitive_type():
                global_klass_name = f'{prop_info.concrete_type.__module__}.{prop_info.concrete_type.__name__}'
                if global_klass_name in ObjectMetadataLibrary.klass_mappings:
                    # Handle other Serializable Classes
                    this_e.append(v.as_xml(view_=view_, as_string=False, element_name=new_key, xmlns=xmlns))
                else:
                    # Handle properties that have a type that is not a Python Primitive (e.g. int, float, str)
                    if prop_info.string_format:
                        ElementTree.SubElement(this_e, new_key).text = f'{v:{prop_info.string_format}}'
                    else:
                        ElementTree.SubElement(this_e, new_key).text = str(v)
            elif prop_info.concrete_type in (float, int):
                ElementTree.SubElement(this_e, new_key).text = str(v)
            elif prop_info.concrete_type is bool:
                ElementTree.SubElement(this_e, new_key).text = str(v).lower()
            else:
                # Assume type is str
                ElementTree.SubElement(this_e, new_key).text = str(v)

    if as_string:
        return ElementTree.tostring(this_e, 'unicode')
    else:
        return this_e


def _from_xml(cls: Type[_T], data: Union[TextIOWrapper, ElementTree.Element],
              default_namespace: Optional[str] = None) -> object:
    logging.debug(f'Rendering XML from {type(data)} to {cls}...')
    klass = ObjectMetadataLibrary.klass_mappings.get(f'{cls.__module__}.{cls.__qualname__}', None)
    if klass is None:
        warnings.warn(f'{cls.__module__}.{cls.__qualname__} is not a known serializable class')
        return None

    klass_properties = ObjectMetadataLibrary.klass_property_mappings.get(f'{cls.__module__}.{cls.__qualname__}', {})

    if isinstance(data, TextIOWrapper):
        data = ElementTree.fromstring(data.read())

    if default_namespace is None:
        _namespaces = dict([node for _, node in ElementTree.iterparse(StringIO(ElementTree.tostring(data, 'unicode')),
                                                                      events=['start-ns'])])
        if 'ns0' in _namespaces:
            default_namespace = _namespaces['ns0']
        else:
            default_namespace = ''

    _data: Dict[str, Any] = {}

    # Handle attributes on the root element if there are any
    for k, v in data.attrib.items():
        decoded_k = CurrentFormatter.formatter.decode(property_name=k)
        if decoded_k in klass.ignore_during_deserialization:
            logger.debug(f'Ignoring {decoded_k} when deserializing {cls.__module__}.{cls.__qualname__}')
            continue

        if decoded_k not in klass_properties:
            for p, pi in klass_properties.items():
                if pi.custom_names.get(SerializationType.XML, None) == decoded_k:
                    decoded_k = p

        prop_info = klass_properties.get(decoded_k, None)
        if not prop_info:
            raise ValueError(f'Non-primitive types not supported from XML Attributes - see {decoded_k} for '
                             f'{cls.__module__}.{cls.__qualname__} which has Prop Metadata: {prop_info}')

        if prop_info.custom_type and prop_info.is_helper_type():
            _data[decoded_k] = prop_info.custom_type.deserialize(v)
        elif prop_info.is_enum:
            _data[decoded_k] = prop_info.concrete_type(v)
        elif prop_info.is_primitive_type():
            _data[decoded_k] = prop_info.concrete_type(v)
        else:
            raise ValueError(f'Non-primitive types not supported from XML Attributes - see {decoded_k}')

    # Handle Node text content
    if data.text:
        for p, pi in klass_properties.items():
            if pi.custom_names.get(SerializationType.XML, None) == '.':
                _data[p] = data.text.strip()

    # Handle Sub-Elements
    for child_e in data:
        child_e_tag_name = str(child_e.tag).replace('{' + default_namespace + '}', '')

        decoded_k = CurrentFormatter.formatter.decode(property_name=child_e_tag_name)
        if decoded_k in klass.ignore_during_deserialization:
            logger.debug(f'Ignoring {decoded_k} when deserializing {cls.__module__}.{cls.__qualname__}')
            continue

        if decoded_k not in klass_properties:
            for p, pi in klass_properties.items():
                if pi.xml_array_config:
                    array_type, nested_name = pi.xml_array_config
                    if nested_name == decoded_k:
                        if array_type == XmlArraySerializationType.FLAT:
                            decoded_k = p
                        else:
                            decoded_k = '____SKIP_ME____'
                elif pi.custom_names.get(SerializationType.XML, None) == decoded_k:
                    decoded_k = p

        if decoded_k == '____SKIP_ME____':
            continue

        prop_info = klass_properties.get(decoded_k, None)
        if not prop_info:
            raise ValueError(f'{decoded_k} is not a known Property for {cls.__module__}.{cls.__qualname__}')

        if prop_info.custom_type:
            if prop_info.is_helper_type():
                _data[decoded_k] = prop_info.custom_type.deserialize(child_e.text)
            else:
                _data[decoded_k] = prop_info.custom_type(child_e.text)
        elif prop_info.is_array and prop_info.xml_array_config:
            array_type, nested_name = prop_info.xml_array_config

            if decoded_k not in _data:
                _data[decoded_k] = []

            if array_type == XmlArraySerializationType.NESTED:
                for sub_child_e in child_e:
                    if not prop_info.is_primitive_type():
                        _data[decoded_k].append(prop_info.concrete_type.from_xml(
                            data=sub_child_e, default_namespace=default_namespace)
                        )
                    else:
                        _data[decoded_k].append(prop_info.concrete_type(sub_child_e.text))
            else:
                if not prop_info.is_primitive_type():
                    _data[decoded_k].append(prop_info.concrete_type.from_xml(
                        data=child_e, default_namespace=default_namespace)
                    )
                else:
                    _data[decoded_k].append(prop_info.concrete_type(child_e.text))
        elif prop_info.is_enum:
            _data[decoded_k] = prop_info.concrete_type(child_e.text)
        elif not prop_info.is_primitive_type():
            global_klass_name = f'{prop_info.concrete_type.__module__}.{prop_info.concrete_type.__name__}'
            if global_klass_name in ObjectMetadataLibrary.klass_mappings:
                _data[decoded_k] = prop_info.concrete_type.from_xml(data=child_e, default_namespace=default_namespace)
            else:
                _data[decoded_k] = prop_info.concrete_type(child_e.text)
        else:
            if prop_info.concrete_type == bool:
                _data[decoded_k] = True if str(child_e.text) in (1, 'true') else False
            else:
                _data[decoded_k] = prop_info.concrete_type(child_e.text)

    logging.debug(f'Creating {cls} from {_data}')

    return cls(**_data)


def _namespace_element_name(tag_name: str, xmlns: Optional[str]) -> str:
    if tag_name.startswith('{'):
        return tag_name
    if xmlns:
        return f'{{{xmlns}}}{tag_name}'
    return tag_name


class ObjectMetadataLibrary:
    """
    The core Class in ``serializable`` that is used to record all metadata about classes that you annotate for
    serialization and deserialization.
    """
    _deferred_property_type_parsing: Dict[str, Set['ObjectMetadataLibrary.SerializableProperty']] = {}
    _klass_views: Dict[str, Type[Any]] = {}
    _klass_property_array_config: Dict[str, Tuple[XmlArraySerializationType, str]] = {}
    _klass_property_attributes: Set[str] = set()
    _klass_property_names: Dict[str, Dict[SerializationType, str]] = {}
    _klass_property_string_formats: Dict[str, str] = {}
    _klass_property_types: Dict[str, Type[Any]] = {}
    _klass_property_views: Dict[str, Set[_T]] = {}
    _klass_property_xml_sequence: Dict[str, int] = {}
    custom_enum_klasses: Set[Type[Any]] = set()
    klass_mappings: Dict[str, 'ObjectMetadataLibrary.SerializableClass'] = {}
    klass_property_mappings: Dict[str, Dict[str, 'ObjectMetadataLibrary.SerializableProperty']] = {}

    class SerializableClass:
        """
        Internal model class used to represent metadata we hold about Classes that are being included in
        (de-)serialization.
        """

        def __init__(self, *, klass: Any, custom_name: Optional[str] = None,
                     serialization_types: Optional[Iterable[SerializationType]] = None,
                     ignore_during_deserialization: Optional[Iterable[str]] = None) -> None:
            self._name = str(klass.__name__)
            self._klass = klass
            self._custom_name = custom_name
            if serialization_types is None:
                serialization_types = _DEFAULT_SERIALIZATION_TYPES
            self._serialization_types = serialization_types
            self._ignore_during_deserialization = set(ignore_during_deserialization or {})

        @property
        def name(self) -> str:
            return self._name

        @property
        def klass(self) -> Any:
            return self._klass

        @property
        def custom_name(self) -> Optional[str]:
            return self._custom_name

        @property
        def serialization_types(self) -> Iterable[SerializationType]:
            return self._serialization_types

        @property
        def ignore_during_deserialization(self) -> Set[str]:
            return self._ignore_during_deserialization

        def __repr__(self) -> str:
            return f'<s.oml.SerializableClass name={self.name}>'

    class SerializableProperty:
        """
        Internal model class used to represent metadata we hold about Properties that are being included in
        (de-)serialization.
        """

        _ARRAY_TYPES = ('List', 'Set', 'SortedSet')
        _SORTED_CONTAINERS_TYPES = {'SortedList': List, 'SortedSet': Set}
        _PRIMITIVE_TYPES = (bool, int, float, str)

        def __init__(self, *, prop_name: str, prop_type: Any, custom_names: Dict[SerializationType, str],
                     custom_type: Optional[Any] = None, is_xml_attribute: bool = False, string_format: Optional[str],
                     views: Optional[Iterable[_T]] = None,
                     xml_array_config: Optional[Tuple[XmlArraySerializationType, str]] = None,
                     xml_sequence: Optional[int] = None) -> None:
            self._name = prop_name
            self._custom_names = custom_names
            self._type_ = None
            self._concrete_type = None
            self._is_array = False
            self._is_enum = False
            self._is_optional = False
            self._custom_type = custom_type
            self._is_xml_attribute = is_xml_attribute
            self._string_format = string_format
            self._views = set(views or [])
            self._xml_array_config = xml_array_config
            self._xml_sequence = xml_sequence or 100

            self._deferred_type_parsing = False
            self._parse_type(type_=prop_type)

        @property
        def name(self) -> str:
            return self._name

        @property
        def custom_names(self) -> Dict[SerializationType, str]:
            return self._custom_names

        def custom_name(self, serialization_type: SerializationType) -> Optional[str]:
            return self.custom_names.get(serialization_type, None)

        @property
        def type_(self) -> Any:
            return self._type_

        @property
        def concrete_type(self) -> Any:
            return self._concrete_type

        @property
        def custom_type(self) -> Optional[Any]:
            return self._custom_type

        @property
        def is_xml_attribute(self) -> bool:
            return self._is_xml_attribute

        @property
        def string_format(self) -> Optional[str]:
            return self._string_format

        @property
        def views(self) -> Set[Type[Any]]:
            return self._views

        @property
        def xml_array_config(self) -> Optional[Tuple[XmlArraySerializationType, str]]:
            return self._xml_array_config

        @property
        def is_array(self) -> bool:
            return self._is_array

        @property
        def is_enum(self) -> bool:
            return self._is_enum

        @property
        def is_optional(self) -> bool:
            return self._is_optional

        @property
        def xml_sequence(self) -> int:
            return self._xml_sequence

        def is_helper_type(self) -> bool:
            if inspect.isclass(self.custom_type):
                return issubclass(self.custom_type, BaseHelper)
            return False

        def is_primitive_type(self) -> bool:
            return self.concrete_type in self._PRIMITIVE_TYPES

        def parse_type_deferred(self) -> None:
            self._parse_type(type_=self._type_)

        def _parse_type(self, type_: Any) -> None:
            self._type_ = type_

            if type(type_) == str:
                type_to_parse = str(type_)
                # Handle types that are quoted strings e.g. 'SortedSet[MyObject]' or 'Optional[SortedSet[MyObject]]'
                if type_to_parse.startswith('typing.Optional['):
                    self._is_optional = True
                    type_to_parse = type_to_parse[16:-1]
                elif type_to_parse.startswith('Optional['):
                    self._is_optional = True
                    type_to_parse = type_to_parse[9:-1]

                match = re.search(r"^(?P<array_type>[\w.]+)\[['\"]?(?P<array_of>\w+)['\"]?]$", type_to_parse)
                if match:
                    results = match.groupdict()
                    if results.get('array_type', None) in self._SORTED_CONTAINERS_TYPES:
                        mapped_array_type = self._SORTED_CONTAINERS_TYPES.get(str(results.get("array_type")))
                        self._is_array = True
                        try:
                            # Will load any class already loaded assuming fully qualified name
                            self._type_ = eval(f'{mapped_array_type}[{results.get("array_of")}]')
                            self._concrete_type = eval(str(results.get("array_of")))
                        except NameError:
                            # Likely a class that is missing its fully qualified name
                            _k = None
                            for _k_name, _oml_sc in ObjectMetadataLibrary.klass_mappings.items():
                                if _oml_sc.name == results.get("array_of"):
                                    _k = _oml_sc.klass

                            if _k is None:
                                # Perhaps a custom ENUM?
                                if results.get("array_of") in ObjectMetadataLibrary.custom_enum_klasses:
                                    prrint(f'CUSTOM ENUM')
                                for _enum_klass in ObjectMetadataLibrary.custom_enum_klasses:
                                    if _enum_klass.__name__ == results.get("array_of"):
                                        _k = _enum_klass

                            if _k is None:
                                self._type_ = type_  # type: ignore
                                self._deferred_type_parsing = True
                                ObjectMetadataLibrary.defer_property_type_parsing(
                                    prop=self, klasses=[str(results.get("array_of"))]
                                )
                                return

                            self._type_ = mapped_array_type[_k]  # type: ignore
                            self._concrete_type = _k
                else:
                    raise ValueError(f'Unable to handle Property with declared type: {type_}')
            else:
                # Handle real types
                if len(getattr(self.type_, '__args__', ())) > 1:
                    # Is this an Optional Property
                    self._is_optional = type(None) in self.type_.__args__

                if self.is_optional:
                    t, n = self.type_.__args__
                    if getattr(t, '_name', None) in self._ARRAY_TYPES:
                        self._is_array = True
                        t, = t.__args__
                    self._concrete_type = t
                else:
                    if getattr(self.type_, '_name', None) in self._ARRAY_TYPES:
                        self._is_array = True
                        self._concrete_type, = self.type_.__args__
                    else:
                        self._concrete_type = self.type_

            # Handle Enums
            if issubclass(type(self.concrete_type), enum.EnumMeta):
                self._is_enum = True

            # Ensure marked as not deferred
            if self._deferred_type_parsing:
                self._deferred_type_parsing = False

        def __eq__(self, other: Any) -> bool:
            if isinstance(other, ObjectMetadataLibrary.SerializableProperty):
                return hash(other) == hash(self)
            return False

        def __lt__(self, other: Any) -> bool:
            if isinstance(other, ObjectMetadataLibrary.SerializableProperty):
                return self.xml_sequence < other.xml_sequence
            return NotImplemented

        def __hash__(self) -> int:
            return hash((
                self.concrete_type, tuple(self.custom_names), self.custom_type, self.is_array, self.is_enum,
                self.is_optional, self.is_xml_attribute, self.name, self.type_,
                tuple(self.xml_array_config) if self.xml_array_config else None, self.xml_sequence
            ))

        def __repr__(self) -> str:
            return f'<s.oml.SerializableProperty name={self.name}, custom_names={self.custom_names}, ' \
                   f'array={self.is_array}, enum={self.is_enum}, optional={self.is_optional}, ' \
                   f'c_type={self.concrete_type}, type={self.type_}, custom_type={self.custom_type}, ' \
                   f'xml_attr={self.is_xml_attribute}, xml_sequence={self.xml_sequence}>'

    @classmethod
    def defer_property_type_parsing(cls, prop: 'ObjectMetadataLibrary.SerializableProperty',
                                    klasses: Iterable[str]) -> None:
        for _k in klasses:
            if _k not in ObjectMetadataLibrary._deferred_property_type_parsing:
                ObjectMetadataLibrary._deferred_property_type_parsing.update({_k: set([])})
            ObjectMetadataLibrary._deferred_property_type_parsing[_k].add(prop)

    @classmethod
    def is_klass_serializable(cls, klass: _T) -> bool:
        if type(klass) is Type:
            return f'{klass.__module__}.{klass.__name__}' in cls.klass_mappings  # type: ignore
        return klass in cls.klass_mappings

    @classmethod
    def is_property(cls, o: object) -> bool:
        return isinstance(o, property)

    @classmethod
    def register_enum(cls, klass: _T) -> _T:
        cls.custom_enum_klasses.add(klass)

    @classmethod
    def register_klass(cls, klass: _T, custom_name: Optional[str],
                       serialization_types: Iterable[SerializationType],
                       ignore_during_deserialization: Optional[Iterable[str]] = None) -> _T:
        if cls.is_klass_serializable(klass=klass):
            return klass

        cls.klass_mappings.update({
            f'{klass.__module__}.{klass.__qualname__}': ObjectMetadataLibrary.SerializableClass(  # type: ignore
                klass=klass, serialization_types=serialization_types,
                ignore_during_deserialization=ignore_during_deserialization
            )
        })

        qualified_class_name = f'{klass.__module__}.{klass.__qualname__}'  # type: ignore
        cls.klass_property_mappings.update({qualified_class_name: {}})
        logging.debug(f'Registering Class {qualified_class_name} with custom name {custom_name}')
        for name, o in inspect.getmembers(klass, ObjectMetadataLibrary.is_property):
            qualified_property_name = f'{qualified_class_name}.{name}'
            prop_arg_specs = inspect.getfullargspec(o.fget)

            cls.klass_property_mappings[qualified_class_name].update({
                name: ObjectMetadataLibrary.SerializableProperty(
                    prop_name=name,
                    custom_names=ObjectMetadataLibrary._klass_property_names.get(qualified_property_name, {}),
                    prop_type=prop_arg_specs.annotations.get('return', None),
                    custom_type=ObjectMetadataLibrary._klass_property_types.get(qualified_property_name, None),
                    is_xml_attribute=(qualified_property_name in ObjectMetadataLibrary._klass_property_attributes),
                    string_format=ObjectMetadataLibrary._klass_property_string_formats.get(
                        qualified_property_name, None
                    ),
                    views=ObjectMetadataLibrary._klass_property_views.get(
                        qualified_property_name, None
                    ),
                    xml_array_config=ObjectMetadataLibrary._klass_property_array_config.get(
                        qualified_property_name, None
                    ),
                    xml_sequence=ObjectMetadataLibrary._klass_property_xml_sequence.get(qualified_property_name, 100)
                )
            })

        if SerializationType.JSON in serialization_types:
            klass.as_json = _as_json  # type: ignore
            klass.from_json = classmethod(_from_json)  # type: ignore

        if SerializationType.XML in serialization_types:
            klass.as_xml = _as_xml  # type: ignore
            klass.from_xml = classmethod(_from_xml)  # type: ignore

        # Handle any deferred Properties depending on this class
        if klass.__qualname__ in ObjectMetadataLibrary._deferred_property_type_parsing:
            for _p in ObjectMetadataLibrary._deferred_property_type_parsing.get(klass.__qualname__, {}):
                _p.parse_type_deferred()

        return klass

    @classmethod
    def register_custom_json_property_name(cls, qual_name: str, json_property_name: str) -> None:
        if qual_name in cls._klass_property_names:
            cls._klass_property_names[qual_name].update({SerializationType.JSON: json_property_name})
        else:
            cls._klass_property_names.update({qual_name: {SerializationType.JSON: json_property_name}})

    @classmethod
    def register_custom_string_format(cls, qual_name: str, string_format: str) -> None:
        cls._klass_property_string_formats.update({qual_name: string_format})

    @classmethod
    def register_custom_xml_property_name(cls, qual_name: str, xml_property_name: str) -> None:
        if qual_name in cls._klass_property_names:
            cls._klass_property_names[qual_name].update({SerializationType.XML: xml_property_name})
        else:
            cls._klass_property_names.update({qual_name: {SerializationType.XML: xml_property_name}})

    @classmethod
    def register_klass_view(cls, klass: _T, view: Type[Any]) -> _T:
        ObjectMetadataLibrary._klass_views.update({
            f'{klass.__module__}.{klass.__qualname__}': view
        })
        return klass

    @classmethod
    def register_property_view(cls, qual_name: str, view_: _T) -> None:
        if qual_name not in ObjectMetadataLibrary._klass_property_views:
            ObjectMetadataLibrary._klass_property_views.update({qual_name: set([view_])})
        else:
            ObjectMetadataLibrary._klass_property_views.get(qual_name).add(view_)

    @classmethod
    def register_xml_property_array_config(cls, qual_name: str,
                                           array_type: XmlArraySerializationType, child_name: str) -> None:
        cls._klass_property_array_config.update({qual_name: (array_type, child_name)})

    @classmethod
    def register_xml_property_attribute(cls, qual_name: str) -> None:
        cls._klass_property_attributes.add(qual_name)

    @classmethod
    def register_xml_property_sequence(cls, qual_name: str, sequence: int) -> None:
        cls._klass_property_xml_sequence.update({qual_name: sequence})

    @classmethod
    def register_property_type_mapping(cls, qual_name: str, mapped_type: Any) -> None:
        cls._klass_property_types.update({qual_name: mapped_type})


def serializable_enum(cls: Optional[Type[_T]] = None) -> Union[Callable[[Any], Type[_T]], Type[_T]]:
    def wrap(kls: Type[_T]) -> Type[_T]:
        ObjectMetadataLibrary.register_enum(klass=kls)
        return kls

    # See if we're being called as @enum or @enum().
    if cls is None:
        # We're called with parens.
        return wrap

    # We're called as @register_klass without parens.
    return wrap(cls)


def serializable_class(cls: Optional[Type[_T]] = None, *, name: Optional[str] = None,
                       serialization_types: Optional[Iterable[SerializationType]] = None,
                       ignore_during_deserialization: Optional[Iterable[str]] = None
                       ) -> Union[Callable[[Any], Type[_T]], Type[_T]]:
    """
    Decorator used to tell ``serializable`` that a class is to be included in (de-)serialization.

    :param cls: Class
    :param name: Alternative name to use for this Class
    :param serialization_types: Serialization Types that are to be supported for this class.
    :param ignore_during_deserialization: List of properties/elements to ignore during deserialization
    :return:
    """
    if serialization_types is None:
        serialization_types = _DEFAULT_SERIALIZATION_TYPES

    def wrap(kls: Type[_T]) -> Type[_T]:
        ObjectMetadataLibrary.register_klass(
            klass=kls, custom_name=name, serialization_types=serialization_types or {},
            ignore_during_deserialization=ignore_during_deserialization
        )
        return kls

    # See if we're being called as @register_klass or @register_klass().
    if cls is None:
        # We're called with parens.
        return wrap

    # We're called as @register_klass without parens.
    return wrap(cls)


def type_mapping(type_: Any) -> Callable[[_F], _F]:
    """
    Deoc
    :param type_:
    :return:
    """

    def outer(f: _F) -> _F:
        logger.debug(f'Registering {f.__module__}.{f.__qualname__} with custom type: {type_}')
        ObjectMetadataLibrary.register_property_type_mapping(
            qual_name=f'{f.__module__}.{f.__qualname__}', mapped_type=type_
        )

        @functools.wraps(f)
        def inner(*args: Any, **kwargs: Any) -> Any:
            return f(*args, **kwargs)

        return cast(_F, inner)

    return outer


def json_name(name: str) -> Callable[[_F], _F]:
    def outer(f: _F) -> _F:
        logger.debug(f'Registering {f.__module__}.{f.__qualname__} with JSON name: {name}')
        ObjectMetadataLibrary.register_custom_json_property_name(
            qual_name=f'{f.__module__}.{f.__qualname__}', json_property_name=name
        )

        @functools.wraps(f)
        def inner(*args: Any, **kwargs: Any) -> Any:
            return f(*args, **kwargs)

        return cast(_F, inner)

    return outer


def string_format(format_: str) -> Callable[[_F], _F]:
    def outer(f: _F) -> _F:
        logger.debug(f'Registering {f.__module__}.{f.__qualname__} with String Format: {format_}')
        ObjectMetadataLibrary.register_custom_string_format(
            qual_name=f'{f.__module__}.{f.__qualname__}', string_format=format_
        )

        @functools.wraps(f)
        def inner(*args: Any, **kwargs: Any) -> Any:
            return f(*args, **kwargs)

        return cast(_F, inner)

    return outer


def view(view_: Type[Any]) -> Callable[[_F], _F]:
    def outer(f: _F) -> _F:
        logger.debug(f'Registering {f.__module__}.{f.__qualname__} with View: {view_}')
        ObjectMetadataLibrary.register_property_view(
            qual_name=f'{f.__module__}.{f.__qualname__}', view_=view_
        )

        @functools.wraps(f)
        def inner(*args: Any, **kwargs: Any) -> Any:
            return f(*args, **kwargs)

        return cast(_F, inner)

    return outer


def xml_attribute() -> Callable[[_F], _F]:
    def outer(f: _F) -> _F:
        logger.debug(f'Registering {f.__module__}.{f.__qualname__} as XML attribute')
        ObjectMetadataLibrary.register_xml_property_attribute(qual_name=f'{f.__module__}.{f.__qualname__}')

        @functools.wraps(f)
        def inner(*args: Any, **kwargs: Any) -> Any:
            return f(*args, **kwargs)

        return cast(_F, inner)

    return outer


def xml_array(array_type: XmlArraySerializationType, child_name: str) -> Callable[[_F], _F]:
    def outer(f: _F) -> _F:
        logger.debug(f'Registering {f.__module__}.{f.__qualname__} as XML Array: {array_type}:{child_name}')
        ObjectMetadataLibrary.register_xml_property_array_config(
            qual_name=f'{f.__module__}.{f.__qualname__}', array_type=array_type, child_name=child_name
        )

        @functools.wraps(f)
        def inner(*args: Any, **kwargs: Any) -> Any:
            return f(*args, **kwargs)

        return cast(_F, inner)

    return outer


def xml_name(name: str) -> Callable[[_F], _F]:
    def outer(f: _F) -> _F:
        logger.debug(f'Registering {f.__module__}.{f.__qualname__} with XML name: {name}')
        ObjectMetadataLibrary.register_custom_xml_property_name(
            qual_name=f'{f.__module__}.{f.__qualname__}', xml_property_name=name
        )

        @functools.wraps(f)
        def inner(*args: Any, **kwargs: Any) -> Any:
            return f(*args, **kwargs)

        return cast(_F, inner)

    return outer


def xml_sequence(sequence: int) -> Callable[[_F], _F]:
    def outer(f: _F) -> _F:
        logger.debug(f'Registering {f.__module__}.{f.__qualname__} with XML sequence: {sequence}')
        ObjectMetadataLibrary.register_xml_property_sequence(
            qual_name=f'{f.__module__}.{f.__qualname__}', sequence=sequence
        )

        @functools.wraps(f)
        def inner(*args: Any, **kwargs: Any) -> Any:
            return f(*args, **kwargs)

        return cast(_F, inner)

    return outer
