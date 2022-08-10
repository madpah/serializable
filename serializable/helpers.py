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

from datetime import date

from serializable import SimpleSerializable


class Iso8601Date(SimpleSerializable):
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
