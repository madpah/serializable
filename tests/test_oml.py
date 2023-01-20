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

from typing import Optional
from unittest import TestCase

from serializable import ObjectMetadataLibrary


class TestOmlSp(TestCase):

    def test_prop_primitive_int_1(self) -> None:
        p = ObjectMetadataLibrary.SerializableProperty(
            prop_name='test_int', prop_type=int, custom_names={}
        )
        self.assertFalse(p.is_array)
        self.assertFalse(p.is_enum)
        self.assertFalse(p.is_optional)
        self.assertTrue(p.is_primitive_type())

    def test_prop_optional_primitive_int_1(self) -> None:
        p = ObjectMetadataLibrary.SerializableProperty(
            prop_name='test_int', prop_type=Optional[int], custom_names={}
        )
        self.assertFalse(p.is_array)
        self.assertFalse(p.is_enum)
        self.assertTrue(p.is_optional)
        self.assertTrue(p.is_primitive_type())
