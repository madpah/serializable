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

import os
from xml.etree import ElementTree

from serializable.formatters import (
    CamelCasePropertyNameFormatter,
    CurrentFormatter,
    KebabCasePropertyNameFormatter,
    SnakeCasePropertyNameFormatter,
)
from tests.base import FIXTURES_DIRECTORY, BaseTestCase
from tests.model import Book, SchemaVersion2, SchemaVersion3, ThePhoenixProject, ThePhoenixProject_v1


class TestXml(BaseTestCase):

    def test_serialize_tfp_cc1(self) -> None:
        CurrentFormatter.formatter = CamelCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-camel-case-1.xml')) as expected_xml:
            self.assertEqualXml(expected_xml.read(), ThePhoenixProject.as_xml())

    def test_serialize_tfp_cc1_v2(self) -> None:
        CurrentFormatter.formatter = CamelCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-camel-case-1-v2.xml')) as expected_xml:
            self.assertEqualXml(expected_xml.read(), ThePhoenixProject.as_xml(SchemaVersion2))

    def test_serialize_tfp_cc1_v3(self) -> None:
        CurrentFormatter.formatter = CamelCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-camel-case-1-v3.xml')) as expected_xml:
            self.assertEqualXml(expected_xml.read(), ThePhoenixProject.as_xml(SchemaVersion3))

    def test_serialize_tfp_kc1(self) -> None:
        CurrentFormatter.formatter = KebabCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-kebab-case-1.xml')) as expected_xml:
            self.assertEqualXml(expected_xml.read(), ThePhoenixProject.as_xml())

    def test_serialize_tfp_kc1_v2(self) -> None:
        CurrentFormatter.formatter = KebabCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-kebab-case-1-v2.xml')) as expected_xml:
            self.assertEqualXml(expected_xml.read(), ThePhoenixProject.as_xml(SchemaVersion2))

    def test_serialize_tfp_sc1(self) -> None:
        CurrentFormatter.formatter = SnakeCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-snake-case-1.xml')) as expected_xml:
            self.assertEqualXml(expected_xml.read(), ThePhoenixProject.as_xml())

    def test_deserialize_tfp_cc1(self) -> None:
        CurrentFormatter.formatter = CamelCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-camel-case-1.xml')) as input_xml:
            book: Book = Book.from_xml(data=ElementTree.fromstring(input_xml.read()))
            self.assertEqual(ThePhoenixProject_v1.title, book.title)
            self.assertEqual(ThePhoenixProject_v1.isbn, book.isbn)
            self.assertEqual(ThePhoenixProject_v1.edition, book.edition)
            self.assertEqual(ThePhoenixProject_v1.publish_date, book.publish_date)
            self.assertEqual(ThePhoenixProject_v1.publisher, book.publisher)
            self.assertEqual(ThePhoenixProject_v1.authors, book.authors)
            self.assertEqual(ThePhoenixProject_v1.chapters, book.chapters)

    def test_deserialize_tfp_cc1_v2(self) -> None:
        CurrentFormatter.formatter = CamelCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-camel-case-1-v2.xml')) as input_xml:
            book: Book = Book.from_xml(data=ElementTree.fromstring(input_xml.read()))
            self.assertEqual(ThePhoenixProject.title, book.title)
            self.assertEqual(ThePhoenixProject.isbn, book.isbn)
            self.assertEqual(ThePhoenixProject.edition, book.edition)
            self.assertEqual(ThePhoenixProject.publish_date, book.publish_date)
            self.assertEqual(ThePhoenixProject.publisher, book.publisher)
            self.assertEqual(ThePhoenixProject.authors, book.authors)
            self.assertEqual(ThePhoenixProject.chapters, book.chapters)

    def test_deserialize_tfp_cc1_with_ignored(self) -> None:
        CurrentFormatter.formatter = CamelCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-camel-case-with-ignored.xml')) as input_xml:
            book: Book = Book.from_xml(data=ElementTree.fromstring(input_xml.read()))
            self.assertEqual(ThePhoenixProject_v1.title, book.title)
            self.assertEqual(ThePhoenixProject_v1.isbn, book.isbn)
            self.assertEqual(ThePhoenixProject_v1.edition, book.edition)
            self.assertEqual(ThePhoenixProject_v1.publish_date, book.publish_date)
            self.assertEqual(ThePhoenixProject_v1.publisher, book.publisher)
            self.assertEqual(ThePhoenixProject_v1.authors, book.authors)
            self.assertEqual(ThePhoenixProject_v1.chapters, book.chapters)

    def test_deserialize_tfp_kc1(self) -> None:
        CurrentFormatter.formatter = KebabCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-kebab-case-1.xml')) as input_xml:
            book: Book = Book.from_xml(data=input_xml)
            self.assertEqual(ThePhoenixProject_v1.title, book.title)
            self.assertEqual(ThePhoenixProject_v1.isbn, book.isbn)
            self.assertEqual(ThePhoenixProject_v1.edition, book.edition)
            self.assertEqual(ThePhoenixProject_v1.publish_date, book.publish_date)
            self.assertEqual(ThePhoenixProject_v1.publisher, book.publisher)
            self.assertEqual(ThePhoenixProject_v1.authors, book.authors)
            self.assertEqual(ThePhoenixProject_v1.chapters, book.chapters)

    def test_deserialize_tfp_sc1(self) -> None:
        CurrentFormatter.formatter = SnakeCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-snake-case-1.xml')) as input_xml:
            book: Book = Book.from_xml(data=ElementTree.fromstring(input_xml.read()))
            self.assertEqual(ThePhoenixProject_v1.title, book.title)
            self.assertEqual(ThePhoenixProject_v1.isbn, book.isbn)
            self.assertEqual(ThePhoenixProject_v1.edition, book.edition)
            self.assertEqual(ThePhoenixProject_v1.publish_date, book.publish_date)
            self.assertEqual(ThePhoenixProject_v1.publisher, book.publisher)
            self.assertEqual(ThePhoenixProject_v1.authors, book.authors)
            self.assertEqual(ThePhoenixProject_v1.chapters, book.chapters)
