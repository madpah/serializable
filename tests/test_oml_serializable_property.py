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
import datetime
from typing import List, Optional, Set
from unittest import TestCase

from serializable import ObjectMetadataLibrary
from serializable.helpers import Iso8601Date
from tests.model import BookEdition


class TestOmlSerializableProperty(TestCase):

    def test_simple_primitive_1(self) -> None:
        sp = ObjectMetadataLibrary.SerializableProperty(
            prop_name='name', prop_type=str, custom_names={}
        )
        self.assertEqual(sp.name, 'name')
        self.assertEqual(sp.type_, str)
        self.assertEqual(sp.concrete_type, str)
        self.assertDictEqual(sp.custom_names, {})
        self.assertIsNone(sp.custom_type)
        self.assertFalse(sp.is_array)
        self.assertFalse(sp.is_enum)
        self.assertFalse(sp.is_optional)
        self.assertFalse(sp.is_xml_attribute)
        self.assertTrue(sp.is_primitive_type())
        self.assertFalse(sp.is_helper_type())

    def test_optional_simple_primitive_1(self) -> None:
        sp = ObjectMetadataLibrary.SerializableProperty(
            prop_name='name', prop_type=Optional[str], custom_names={}
        )
        self.assertEqual(sp.name, 'name')
        self.assertEqual(sp.type_, Optional[str])
        self.assertEqual(sp.concrete_type, str)
        self.assertDictEqual(sp.custom_names, {})
        self.assertIsNone(sp.custom_type)
        self.assertFalse(sp.is_array)
        self.assertFalse(sp.is_enum)
        self.assertTrue(sp.is_optional)
        self.assertFalse(sp.is_xml_attribute)
        self.assertTrue(sp.is_primitive_type())
        self.assertFalse(sp.is_helper_type())

    def test_iterable_primitive_1(self) -> None:
        sp = ObjectMetadataLibrary.SerializableProperty(
            prop_name='name', prop_type=List[str], custom_names={}
        )
        self.assertEqual(sp.name, 'name')
        self.assertEqual(sp.type_, List[str])
        self.assertEqual(sp.concrete_type, str)
        self.assertDictEqual(sp.custom_names, {})
        self.assertIsNone(sp.custom_type)
        self.assertTrue(sp.is_array)
        self.assertFalse(sp.is_enum)
        self.assertFalse(sp.is_optional)
        self.assertFalse(sp.is_xml_attribute)
        self.assertTrue(sp.is_primitive_type())
        self.assertFalse(sp.is_helper_type())

    def test_optional_iterable_primitive_1(self) -> None:
        sp = ObjectMetadataLibrary.SerializableProperty(
            prop_name='name', prop_type=Optional[List[str]], custom_names={}
        )
        self.assertEqual(sp.name, 'name')
        self.assertEqual(sp.type_, Optional[List[str]])
        self.assertEqual(sp.concrete_type, str)
        self.assertDictEqual(sp.custom_names, {})
        self.assertIsNone(sp.custom_type)
        self.assertTrue(sp.is_array)
        self.assertFalse(sp.is_enum)
        self.assertTrue(sp.is_optional)
        self.assertFalse(sp.is_xml_attribute)
        self.assertTrue(sp.is_primitive_type())
        self.assertFalse(sp.is_helper_type())

    def test_sorted_set_1(self) -> None:
        sp = ObjectMetadataLibrary.SerializableProperty(
            prop_name='name', prop_type='SortedSet[BookEdition]', custom_names={}
        )
        self.assertEqual(sp.name, 'name')
        self.assertEqual(sp.type_, Set[BookEdition])
        self.assertEqual(sp.concrete_type, BookEdition)
        self.assertDictEqual(sp.custom_names, {})
        self.assertIsNone(sp.custom_type)
        self.assertTrue(sp.is_array)
        self.assertFalse(sp.is_enum)
        self.assertFalse(sp.is_optional)
        self.assertFalse(sp.is_xml_attribute)
        self.assertFalse(sp.is_primitive_type())
        self.assertFalse(sp.is_helper_type())

    def test_sorted_set_2(self) -> None:
        sp = ObjectMetadataLibrary.SerializableProperty(
            prop_name='name', prop_type="SortedSet['BookEdition']", custom_names={}
        )
        self.assertEqual(sp.name, 'name')
        self.assertEqual(sp.type_, Set[BookEdition])
        self.assertEqual(sp.concrete_type, BookEdition)
        self.assertDictEqual(sp.custom_names, {})
        self.assertIsNone(sp.custom_type)
        self.assertTrue(sp.is_array)
        self.assertFalse(sp.is_enum)
        self.assertFalse(sp.is_optional)
        self.assertFalse(sp.is_xml_attribute)
        self.assertFalse(sp.is_primitive_type())
        self.assertFalse(sp.is_helper_type())

    def test_datetime_using_helper(self) -> None:
        sp = ObjectMetadataLibrary.SerializableProperty(
            prop_name='publish_date', prop_type=datetime.datetime, custom_names={}, custom_type=Iso8601Date
        )
        self.assertEqual(sp.name, 'publish_date')
        self.assertEqual(sp.type_, datetime.datetime)
        self.assertEqual(sp.concrete_type, datetime.datetime)
        self.assertDictEqual(sp.custom_names, {})
        self.assertEqual(sp.custom_type, Iso8601Date)
        self.assertFalse(sp.is_array)
        self.assertFalse(sp.is_enum)
        self.assertFalse(sp.is_optional)
        self.assertFalse(sp.is_xml_attribute)
        self.assertFalse(sp.is_primitive_type())
        self.assertTrue(sp.is_helper_type())
