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
import xml
from typing import Any
from unittest import TestCase

import lxml  # type: ignore
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

    def assertEqualJson(self, a: str, b: str) -> None:
        self.assertEqual(
            BaseTestCase._sort_json_dict(json.loads(a)),
            BaseTestCase._sort_json_dict(json.loads(b))
        )

    def assertEqualXml(self, a: str, b: str) -> None:
        a = xml.etree.ElementTree.tostring(
            xml.etree.ElementTree.fromstring(a, lxml.etree.XMLParser(remove_blank_text=True, remove_comments=True)),
            'unicode'
        )
        b = xml.etree.ElementTree.tostring(
            xml.etree.ElementTree.fromstring(b, lxml.etree.XMLParser(remove_blank_text=True, remove_comments=True)),
            'unicode'
        )
        diff_results = main.diff_texts(a, b, diff_options={'F': 0.5})
        diff_results = list(filter(lambda o: not isinstance(o, MoveNode), diff_results))
        self.assertEqual(len(diff_results), 0, f'There are XML differences: {diff_results}\n- {a}\n+ {b}')
