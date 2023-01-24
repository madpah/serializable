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
import re
import warnings
from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Any


class BaseHelper(ABC):

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


class Iso8601Date(BaseHelper):
    _PATTERN_DATE = '%Y-%m-%d'

    @classmethod
    def serialize(cls, o: object) -> str:
        if isinstance(o, date):
            return o.strftime(Iso8601Date._PATTERN_DATE)

        raise ValueError(f'Attempt to serialize a non-date: {o.__class__}')

    @classmethod
    def deserialize(cls, o: object) -> date:
        try:
            return date.fromisoformat(str(o))
        except ValueError:
            raise ValueError(f'Date string supplied ({o}) does not match either "{Iso8601Date._PATTERN_DATE}"')


class XsdDate(BaseHelper):

    @classmethod
    def serialize(cls, o: object) -> str:
        if isinstance(o, date):
            return o.isoformat()

        raise ValueError(f'Attempt to serialize a non-date: {o.__class__}')

    @classmethod
    def deserialize(cls, o: object) -> date:
        try:
            if str(o).startswith('-'):
                # Remove any leading hyphen
                o = str(o)[1:]

            if str(o).endswith('Z'):
                o = str(o)[:-1]
                warnings.warn(
                    'Potential data loss will occur: dates with timezones not supported in Python', UserWarning
                )
            if '+' in str(o):
                o = str(o)[:str(o).index('+')]
                warnings.warn(
                    'Potential data loss will occur: dates with timezones not supported in Python', UserWarning
                )
            return date.fromisoformat(str(o))
        except ValueError:
            raise ValueError(f'Date string supplied ({o}) is not a supported ISO Format')


class XsdDateTime(BaseHelper):

    @classmethod
    def serialize(cls, o: object) -> str:
        if isinstance(o, datetime):
            return o.isoformat()

        raise ValueError(f'Attempt to serialize a non-date: {o.__class__}')

    @classmethod
    def deserialize(cls, o: object) -> datetime:
        try:
            if str(o).startswith('-'):
                # Remove any leading hyphen
                o = str(o)[1:]

            # Ensure any milliseconds are 6 digits
            o = re.sub(r"\.(\d{1,6})", lambda v: f'.{int(v.group()[1:]):06}', str(o))

            if str(o).endswith('Z'):
                # Replace ZULU time with 00:00 offset
                o = f'{str(o)[:-1]}+00:00'
            return datetime.fromisoformat(str(o))
        except ValueError:
            raise ValueError(f'Date-Time string supplied ({o}) is not a supported ISO Format')
