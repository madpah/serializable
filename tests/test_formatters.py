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

from unittest import TestCase

from serializable.formatters import (
    CamelCasePropertyNameFormatter,
    KebabCasePropertyNameFormatter,
    SnakeCasePropertyNameFormatter,
)


class TestFormatterCamelCase(TestCase):

    def test_encode_1(self) -> None:
        self.assertEqual('bookChapters', CamelCasePropertyNameFormatter.encode(property_name='book_chapters'))

    def test_encode_2(self) -> None:
        self.assertEqual('id', CamelCasePropertyNameFormatter.encode(property_name='id'))

    def test_encode_3(self) -> None:
        self.assertEqual('book', CamelCasePropertyNameFormatter.encode(property_name='Book'))

    def test_encode_4(self) -> None:
        self.assertEqual('type', CamelCasePropertyNameFormatter.encode(property_name='type'))

    def test_decode_1(self) -> None:
        self.assertEqual('book_chapters', CamelCasePropertyNameFormatter.decode(property_name='bookChapters'))

    def test_decode_2(self) -> None:
        self.assertEqual('id', CamelCasePropertyNameFormatter.decode(property_name='id'))

    def test_decode_4(self) -> None:
        self.assertEqual('type', CamelCasePropertyNameFormatter.decode(property_name='type'))

    def test_decode_class_name_1(self) -> None:
        self.assertEqual('Book', CamelCasePropertyNameFormatter.decode_as_class_name(name='book'))

    def test_decode_class_name_2(self) -> None:
        self.assertEqual('BookChapters', CamelCasePropertyNameFormatter.decode_as_class_name(name='bookChapters'))


class TestFormatterKebabCase(TestCase):

    def test_encode_1(self) -> None:
        self.assertEqual('book-chapters', KebabCasePropertyNameFormatter.encode(property_name='book_chapters'))

    def test_encode_2(self) -> None:
        self.assertEqual('id', KebabCasePropertyNameFormatter.encode(property_name='id'))

    def test_encode_3(self) -> None:
        self.assertEqual('book', KebabCasePropertyNameFormatter.encode(property_name='Book'))

    def test_decode_1(self) -> None:
        self.assertEqual('book_chapters', KebabCasePropertyNameFormatter.decode(property_name='book-chapters'))

    def test_decode_2(self) -> None:
        self.assertEqual('id', KebabCasePropertyNameFormatter.decode(property_name='id'))


class TestFormatterSnakeCase(TestCase):

    def test_encode_1(self) -> None:
        self.assertEqual('book_chapters', SnakeCasePropertyNameFormatter.encode(property_name='book_chapters'))

    def test_encode_2(self) -> None:
        self.assertEqual('id', SnakeCasePropertyNameFormatter.encode(property_name='id'))

    def test_encode_3(self) -> None:
        self.assertEqual('book', SnakeCasePropertyNameFormatter.encode(property_name='Book'))

    def test_decode_1(self) -> None:
        self.assertEqual('book_chapters', SnakeCasePropertyNameFormatter.decode(property_name='book_chapters'))

    def test_decode_2(self) -> None:
        self.assertEqual('id', SnakeCasePropertyNameFormatter.decode(property_name='id'))
