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

import json
import os
from typing import Any, Optional, Union
from unittest import TestCase

import lxml  # type: ignore
from defusedxml import ElementTree as SafeElementTree  # type: ignore
from xmldiff import main  # type: ignore
from xmldiff.actions import MoveNode  # type: ignore

FIXTURES_DIRECTORY = os.path.join(os.path.dirname(__file__), 'fixtures')


class BaseTestCase(TestCase):

    @staticmethod
    def _sort_json_dict(item: object) -> Any:
        if isinstance(item, dict):
            return sorted((key, BaseTestCase._sort_json_dict(values)) for key, values in item.items())
        if isinstance(item, list):
            return sorted(BaseTestCase._sort_json_dict(x) for x in item)
        else:
            return item

    def assertEqualJson(self, expected: str, actual: str) -> None:
        self.assertEqual(
            BaseTestCase._sort_json_dict(json.loads(expected)),
            BaseTestCase._sort_json_dict(json.loads(actual))
        )

    def assertEqualXml(self, expected: str, actual: str) -> None:
        a = SafeElementTree.tostring(
            SafeElementTree.fromstring(expected, lxml.etree.XMLParser(remove_blank_text=True, remove_comments=True)),
            'unicode'
        )
        b = SafeElementTree.tostring(
            SafeElementTree.fromstring(actual, lxml.etree.XMLParser(remove_blank_text=True, remove_comments=True)),
            'unicode'
        )
        diff_results = main.diff_texts(a, b, diff_options={'F': 0.5})
        diff_results = list(filter(lambda o: not isinstance(o, MoveNode), diff_results))
        self.assertEqual(len(diff_results), 0,
                         f'There are XML differences: {diff_results!r}\n- {a!s}\n+ {b!s}')


class DeepCompareMixin(object):
    def assertDeepEqual(self: Union[TestCase, 'DeepCompareMixin'],
                        first: Any, second: Any, msg: Optional[str] = None) -> None:
        """costly compare, but very verbose"""
        _omd = self.maxDiff
        try:
            self.maxDiff = None
            dd1 = self.__deepDict(first)
            dd2 = self.__deepDict(second)
            self.assertDictEqual(dd1, dd2, msg)
        finally:
            self.maxDiff = _omd

    def __deepDict(self, o: Any) -> Any:
        if isinstance(o, tuple):
            return tuple(self.__deepDict(i) for i in o)
        if isinstance(o, list):
            return list(self.__deepDict(i) for i in o)
        if isinstance(o, dict):
            return {k: self.__deepDict(v) for k, v in o.items()}
        if isinstance(o, set):
            # this method returns dict. `dict` is not hashable, so use `tuple` instead.
            return tuple(self.__deepDict(i) for i in sorted(o, key=hash)) + ('%conv:%set',)
        if hasattr(o, '__dict__'):
            d = {a: self.__deepDict(v) for a, v in o.__dict__.items() if '__' not in a}
            d['%conv'] = str(type(o))
            return d
        return o
