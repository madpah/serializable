# encoding: utf-8

# This file is part of serializable
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

from typing import List, Optional
from unittest import TestCase

from serializable import ObjectMetadataLibrary


class TestOmlSerializableProperty(TestCase):

    def test_simple_primitive_1(self) -> None:
        sp = ObjectMetadataLibrary.SerializableProperty(
            prop_name='name', prop_type=str, custom_names={}
        )
        self.assertEqual(sp.name, 'name')
        self.assertEqual(sp.type_, str)
        self.assertEqual(sp.concrete_type(), str)
        self.assertDictEqual(sp.custom_names, {})
        self.assertFalse(sp.is_array())
        self.assertFalse(sp.is_enum())
        self.assertFalse(sp.is_optional())
        self.assertFalse(sp.is_xml_attribute)
        self.assertTrue(sp.is_primitive_type())

    def test_optional_simple_primitive_1(self) -> None:
        sp = ObjectMetadataLibrary.SerializableProperty(
            prop_name='name', prop_type=Optional[str], custom_names={}
        )
        self.assertEqual(sp.name, 'name')
        self.assertEqual(sp.type_, Optional[str])
        self.assertEqual(sp.concrete_type(), str)
        self.assertDictEqual(sp.custom_names, {})
        self.assertFalse(sp.is_array())
        self.assertFalse(sp.is_enum())
        self.assertTrue(sp.is_optional())
        self.assertFalse(sp.is_xml_attribute)
        self.assertTrue(sp.is_primitive_type())

    def test_iterable_primitive_1(self) -> None:
        sp = ObjectMetadataLibrary.SerializableProperty(
            prop_name='name', prop_type=List[str], custom_names={}
        )
        self.assertEqual(sp.name, 'name')
        self.assertEqual(sp.type_, List[str])
        self.assertEqual(sp.concrete_type(), str)
        self.assertDictEqual(sp.custom_names, {})
        self.assertTrue(sp.is_array())
        self.assertFalse(sp.is_enum())
        self.assertFalse(sp.is_optional())
        self.assertFalse(sp.is_xml_attribute)
        self.assertTrue(sp.is_primitive_type())

    def test_optional_iterable_primitive_1(self) -> None:
        sp = ObjectMetadataLibrary.SerializableProperty(
            prop_name='name', prop_type=Optional[List[str]], custom_names={}
        )
        self.assertEqual(sp.name, 'name')
        self.assertEqual(sp.type_, Optional[List[str]])
        self.assertEqual(sp.concrete_type(), str)
        self.assertDictEqual(sp.custom_names, {})
        self.assertTrue(sp.is_array())
        self.assertFalse(sp.is_enum())
        self.assertTrue(sp.is_optional())
        self.assertFalse(sp.is_xml_attribute)
        self.assertTrue(sp.is_primitive_type())
