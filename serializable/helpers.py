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

from datetime import date, datetime
from logging import getLogger
from re import sub as re_sub
from typing import TYPE_CHECKING, Any, Optional, Type, TypeVar, Union

if TYPE_CHECKING:  # pragma: no cover
    from xml.etree.ElementTree import Element

    from . import ObjectMetadataLibrary, ViewType

_T = TypeVar('_T')

_logger = getLogger(__name__)


class BaseHelper:
    """Base Helper.

    Inherit from this class and implement/override the needed functions!

    This class does not provide any functionality,
    it is more like a Protocol with some fallback implementations.
    """

    # region general/fallback

    @classmethod
    def serialize(cls, o: Any) -> Union[Any, str]:
        """general purpose serializer"""
        raise NotImplementedError()

    @classmethod
    def deserialize(cls, o: Any) -> Any:
        """general purpose deserializer"""
        raise NotImplementedError()

    # endregion general/fallback

    # region json specific

    @classmethod
    def json_normalize(cls, o: Any, *,
                       view: Optional[Type['ViewType']],
                       prop_info: 'ObjectMetadataLibrary.SerializableProperty',
                       ctx: Type[Any],
                       **kwargs: Any) -> Optional[Any]:
        """json specific normalizer"""
        return cls.json_serialize(o)

    @classmethod
    def json_serialize(cls, o: Any) -> Union[str, Any]:
        """json specific serializer"""
        return cls.serialize(o)

    @classmethod
    def json_denormalize(cls, o: Any, *,
                         prop_info: 'ObjectMetadataLibrary.SerializableProperty',
                         ctx: Type[Any],
                         **kwargs: Any) -> Any:
        """json specific denormalizer

        :param tCls: the class that was desired to denormalize to
        :param pCls: tha prent class - as context
        """
        return cls.json_deserialize(o)

    @classmethod
    def json_deserialize(cls, o: Any) -> Any:
        """json specific deserializer"""
        return cls.deserialize(o)

    # endregion json specific

    # endregion xml specific

    @classmethod
    def xml_normalize(cls, o: Any, *,
                      element_name: str,
                      view: Optional[Type['ViewType']],
                      xmlns: Optional[str],
                      prop_info: 'ObjectMetadataLibrary.SerializableProperty',
                      ctx: Type[Any],
                      **kwargs: Any) -> Optional[Union['Element', Any]]:
        """xml specific normalizer"""
        return cls.xml_serialize(o)

    @classmethod
    def xml_serialize(cls, o: Any) -> Union[str, Any]:
        """xml specific serializer"""
        return cls.serialize(o)

    @classmethod
    def xml_denormalize(cls, o: 'Element', *,
                        default_ns: Optional[str],
                        prop_info: 'ObjectMetadataLibrary.SerializableProperty',
                        ctx: Type[Any],
                        **kwargs: Any) -> Any:
        """xml specific denormalizer"""
        return cls.xml_deserialize(o.text)

    @classmethod
    def xml_deserialize(cls, o: Union[str, Any]) -> Any:
        """xml specific deserializer"""
        return cls.deserialize(o)

    # endregion xml specific


class Iso8601Date(BaseHelper):
    _PATTERN_DATE = '%Y-%m-%d'

    @classmethod
    def serialize(cls, o: Any) -> str:
        if isinstance(o, date):
            return o.strftime(Iso8601Date._PATTERN_DATE)

        raise ValueError(f'Attempt to serialize a non-date: {o.__class__}')

    @classmethod
    def deserialize(cls, o: Any) -> date:
        try:
            return date.fromisoformat(str(o))
        except ValueError:
            raise ValueError(f'Date string supplied ({o}) does not match either "{Iso8601Date._PATTERN_DATE}"')


class XsdDate(BaseHelper):

    @classmethod
    def serialize(cls, o: Any) -> str:
        if isinstance(o, date):
            return o.isoformat()

        raise ValueError(f'Attempt to serialize a non-date: {o.__class__}')

    @classmethod
    def deserialize(cls, o: Any) -> date:
        try:
            if str(o).startswith('-'):
                # Remove any leading hyphen
                o = str(o)[1:]

            if str(o).endswith('Z'):
                o = str(o)[:-1]
                _logger.warning(
                    'Potential data loss will occur: dates with timezones not supported in Python',
                    stacklevel=2)
            if '+' in str(o):
                o = str(o)[:str(o).index('+')]
                _logger.warning(
                    'Potential data loss will occur: dates with timezones not supported in Python',
                    stacklevel=2)
            return date.fromisoformat(str(o))
        except ValueError:
            raise ValueError(f'Date string supplied ({o}) is not a supported ISO Format')


class XsdDateTime(BaseHelper):

    @staticmethod
    def __fix_tz(dt: datetime) -> datetime:
        """
        Fix for Python's violation of ISO8601: :py:meth:`datetime.isoformat()` might omit the time offset when in doubt,
        but the ISO-8601 assumes local time zone.
        Anyway, the time offset is mandatory for this purpose.
        """
        return dt.astimezone() \
            if dt.tzinfo is None \
            else dt

    @classmethod
    def serialize(cls, o: Any) -> str:
        if isinstance(o, datetime):
            return cls.__fix_tz(o).isoformat()

        raise ValueError(f'Attempt to serialize a non-date: {o.__class__}')

    @classmethod
    def deserialize(cls, o: Any) -> datetime:
        try:
            if str(o).startswith('-'):
                # Remove any leading hyphen
                o = str(o)[1:]

            # Ensure any milliseconds are 6 digits
            o = re_sub(r'\.(\d{1,6})', lambda v: f'.{int(v.group()[1:]):06}', str(o))

            if str(o).endswith('Z'):
                # Replace ZULU time with 00:00 offset
                o = f'{str(o)[:-1]}+00:00'
            return datetime.fromisoformat(str(o))
        except ValueError:
            raise ValueError(f'Date-Time string supplied ({o}) is not a supported ISO Format')
