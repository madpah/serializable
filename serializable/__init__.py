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
import inspect
from abc import ABC, abstractmethod
from copy import copy
from json import JSONEncoder
from typing import Any, Dict, List, Set, Tuple, Type, Union, cast
from xml.etree import ElementTree

from .formatters import CurrentFormatter

AnySerializable = Union[Type["SimpleSerializable"], Type["SerializableObject"], Type["JsonSerializableObject"]]


@enum.unique
class XmlArraySerializationType(enum.Enum):
    FLAT = 1
    NESTED = 2


class SimpleSerializable(ABC):
    """
    You can create your own class (or use one of the provided classes in `serializable.helpers` to handle
    serializable and deserialization to Python primitive data types - e.g. datetime.

    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    @classmethod
    @abstractmethod
    def serialize(cls, o: object) -> str:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def deserialize(cls, o: str) -> object:
        raise NotImplementedError


class SerializableObject(ABC):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    @classmethod
    def get_array_property_configuration(cls) -> Dict[str, Tuple[XmlArraySerializationType, str, Any]]:
        """
        For properties that are arrays (think List or Set), this configuration can be used to affect how these
        properties are (de-)serialized.

        Return:
             `Dict[str, Tuple[XmlArraySerializationType, str, Type]]`
        """
        return {}

    @staticmethod
    def get_property_data_class_mappings() -> Dict[str, AnySerializable]:
        """
        This method should return a mapping from Python property name to either the Class that it deserializes to OR
        a Callable that handles the data for this property as part of deserialization.

        For example:
        ``
        {
            "chapters": Chapter
        }
        ``
        would allow for an Array of Chapters to be deserialized to a Set of `Chapter` objects.

        Returns:
            `Dict[str, AnySerializable]`
        """
        return {}

    @staticmethod
    def get_property_key_mappings() -> Dict[str, str]:
        """
        This method should return a `Dict[str, str]` that maps JSON property or key names to Python object property
        names.

        For example, in Python 'id' is a keyword and best practice is to suffix your property name with an underscore.
        Thus, your Python class might have a property named `id_` which when represented in JSON or XML should be 'id'.

        Therefor this method should return:
        ``
        {
           "id": "id_"
        }
        ``

        Returns:
            `Dict[str, str]`
        """
        return {}


class JsonSerializableObject(SerializableObject):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_json_key_removals() -> List[str]:
        """


        Returns:
            `List[str]`
        """
        return []

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> object:
        _data = copy(data)
        for k, v in data.items():
            if k in cls.get_json_key_removals():
                del (_data[k])
            else:
                decoded_k = CurrentFormatter.formatter.decode(property_name=k)
                if decoded_k in cls.get_property_key_mappings().values():
                    del (_data[k])
                    _data[list(cls.get_property_key_mappings().keys())[
                        list(cls.get_property_key_mappings().values()).index(decoded_k)]] = v
                else:
                    del (_data[k])
                    _data[decoded_k] = v

        for k, v in _data.items():
            if k in cls.get_property_data_class_mappings():
                klass: AnySerializable = cls.get_property_data_class_mappings()[k]
                if isinstance(v, (list, set)):
                    items = []
                    for j in v:
                        if inspect.isclass(klass) and callable(getattr(klass, "from_json", None)):
                            items.append(klass.from_json(data=j))
                        elif inspect.isclass(klass) and callable(getattr(klass, "deserialize", None)):
                            items.append(klass.deserialize(j))
                        else:
                            items.append(klass(j))
                    _data[k] = items
                else:
                    if inspect.isclass(klass) and callable(getattr(klass, "from_json", None)):
                        _data[k] = klass.from_json(data=v)
                    elif inspect.isclass(klass) and callable(getattr(klass, "deserialize", None)):
                        _data[k] = klass.deserialize(v)
                    else:
                        _data[k] = klass(v)

            elif k in cls.get_array_property_configuration():
                serialization_type, sub_element_name, klass = cls.get_array_property_configuration()[k]
                if isinstance(v, (list, set)):
                    items = []
                    for j in v:
                        if inspect.isclass(klass) and callable(getattr(klass, "from_json", None)):
                            items.append(klass.from_json(data=j))
                        else:
                            items.append(klass(j))
                    _data[k] = items

        return cls(**_data)


class XmlSerializableObject(SerializableObject):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    def properties_as_attributes(cls) -> Set[str]:
        """
        A set of Property names that should be attributes on this class object when (de-)serialized as XML.

        Returns:
            `Set[str]`
        """
        return set()

    def as_xml(self, as_string: bool = True) -> Union[ElementTree.Element, str]:
        this_e_attributes = {}
        for k, v in self.__dict__.items():
            # Remove leading _ in key names
            new_key = k[1:]
            if new_key.startswith('_') or '__' in new_key:
                continue

            if new_key in self.properties_as_attributes():
                if new_key in self.get_property_key_mappings():
                    new_key = self.get_property_key_mappings()[new_key]
                if CurrentFormatter.formatter:
                    new_key = CurrentFormatter.formatter.encode(property_name=new_key)

                this_e_attributes.update({new_key: v})

        this_e = ElementTree.Element(CurrentFormatter.formatter.encode(self.__class__.__name__), this_e_attributes)

        for k, v in self.__dict__.items():
            # Remove leading _ in key names
            new_key = k[1:]
            if new_key.startswith('_') or '__' in new_key:
                continue

            if new_key not in self.properties_as_attributes():
                if new_key in self.get_property_key_mappings():
                    new_key = self.get_property_key_mappings()[new_key]

                if new_key in self.get_property_data_class_mappings():
                    klass_ss: Type[SimpleSerializable] = cast(Type[SimpleSerializable],
                                                              self.get_property_data_class_mappings()[new_key])
                    if CurrentFormatter.formatter:
                        new_key = CurrentFormatter.formatter.encode(property_name=new_key)
                    ElementTree.SubElement(this_e, new_key).text = str(klass_ss.serialize(v))
                elif isinstance(v, (list, set)):
                    if new_key in self.get_array_property_configuration():
                        (array_type, nested_key, klass) = self.get_array_property_configuration()[new_key]
                    else:
                        (array_type, nested_key) = (XmlArraySerializationType.FLAT, new_key)

                    if CurrentFormatter.formatter:
                        new_key = CurrentFormatter.formatter.encode(property_name=new_key)

                    if array_type == XmlArraySerializationType.NESTED:
                        nested_e = ElementTree.SubElement(this_e, new_key)
                        item_key = new_key
                    else:
                        nested_e = this_e
                        item_key = nested_key

                    for j in v:
                        if callable(getattr(j, "as_xml", None)):
                            nested_e.append(j.as_xml(as_string=False))
                        else:
                            ElementTree.SubElement(nested_e, item_key).text = str(j)

                    # if array_config
                else:
                    if CurrentFormatter.formatter:
                        new_key = CurrentFormatter.formatter.encode(property_name=new_key)
                    ElementTree.SubElement(this_e, new_key).text = str(v)

        if as_string:
            return ElementTree.tostring(this_e, 'unicode')
        else:
            return this_e

    @classmethod
    def from_xml(cls, data: ElementTree.Element) -> object:
        _data: Dict[str, Any] = {}

        # Handle any attributes first
        for attribute_name, attribute_value in data.attrib.items():
            decoded_name = CurrentFormatter.formatter.decode(property_name=attribute_name)
            if decoded_name in cls.get_property_key_mappings().values():
                _data[list(cls.get_property_key_mappings().keys())[
                    list(cls.get_property_key_mappings().values()).index(decoded_name)]] = attribute_value

        # Handle child elements
        for child_e in data:
            decoded_name = CurrentFormatter.formatter.decode(property_name=child_e.tag)
            array_config = [{k: v} for k, v in cls.get_array_property_configuration().items() if str(child_e.tag) in v]

            if decoded_name in cls.get_property_key_mappings().values():
                decoded_name = list(cls.get_property_key_mappings().keys())[
                    list(cls.get_property_key_mappings().values()).index(decoded_name)]

            if child_e.tag in cls.get_array_property_configuration():
                # Handle Nested Lists
                array_type, nested_tag, klass = cls.get_array_property_configuration()[child_e.tag]
                if not array_type == XmlArraySerializationType.NESTED:
                    raise ValueError('Only NESTED expected here!')

                _data.update({
                    decoded_name: []
                })

                for sub_child_e in child_e:
                    if sub_child_e.tag != nested_tag:
                        raise ValueError(f'Only {nested_tag} elements expected under {child_e.tag}')
                    _data[decoded_name].append(klass.from_xml(data=sub_child_e))

            elif array_config:
                prop_name, (array_type, tag_name, klass) = next(iter(array_config[0].items()))
                if not array_type == XmlArraySerializationType.FLAT:
                    raise ValueError('Only FLAT expected here!')
                if prop_name not in _data:
                    _data.update({
                        prop_name: []
                    })
                if callable(getattr(klass, "from_xml", None)):
                    _data[prop_name].append(klass.from_xml(data=child_e))
                else:
                    _data[prop_name].append(klass(child_e.text))

            elif decoded_name in cls.get_property_data_class_mappings():
                klass = cls.get_property_data_class_mappings()[decoded_name]
                _data.update({
                    decoded_name: klass.deserialize(str(child_e.text))
                })

            elif decoded_name in cls.__dict__:
                _data.update({
                    decoded_name: int(str(child_e.text)) if str(child_e.text).isdigit() else child_e.text
                })

            else:
                raise ValueError(f'Element "{child_e.tag}" does not map to a Property of Class {cls.__name__}')

        return cls(**_data)


class DefaultJsonEncoder(JSONEncoder):

    def default(self, o: Any) -> Any:
        # Iterables
        if isinstance(o, (list, set)):
            return list(o)

        # Classes
        if isinstance(o, object):
            d: Dict[Any, Any] = {}
            for k, v in o.__dict__.items():
                # Remove leading _ in key names
                new_key = k[1:]
                if new_key.startswith('_') or '__' in new_key:
                    continue

                if isinstance(o, SerializableObject):
                    if new_key in o.get_property_key_mappings():
                        new_key = o.get_property_key_mappings()[new_key]

                    if new_key in o.get_property_data_class_mappings():
                        klass: Type[SimpleSerializable] = cast(Type[SimpleSerializable],
                                                               o.get_property_data_class_mappings()[new_key])
                        v = klass.serialize(v)

                if CurrentFormatter.formatter:
                    new_key = CurrentFormatter.formatter.encode(property_name=new_key)

                d.update({new_key: v})

            return d

        # Fallback to default
        super().default(o=o)
