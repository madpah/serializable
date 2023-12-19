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

from serializable.formatters import (
    CamelCasePropertyNameFormatter,
    CurrentFormatter,
    KebabCasePropertyNameFormatter,
    SnakeCasePropertyNameFormatter,
)
from tests.base import FIXTURES_DIRECTORY, BaseTestCase
from tests.model import Book, SchemaVersion2, SchemaVersion3, SchemaVersion4, ThePhoenixProject, ThePhoenixProject_v1


class TestJson(BaseTestCase):

    def test_serialize_tfp_cc(self) -> None:
        CurrentFormatter.formatter = CamelCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-camel-case.json')) as expected_json:
            self.assertEqualJson(expected_json.read(), ThePhoenixProject.as_json())

    def test_serialize_tfp_cc_v2(self) -> None:
        CurrentFormatter.formatter = CamelCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-camel-case-v2.json')) as expected_json:
            self.assertEqualJson(expected_json.read(), ThePhoenixProject.as_json(view_=SchemaVersion2))

    def test_serialize_tfp_cc_v3(self) -> None:
        CurrentFormatter.formatter = CamelCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-camel-case-v3.json')) as expected_json:
            self.assertEqualJson(expected_json.read(), ThePhoenixProject.as_json(view_=SchemaVersion3))

    def test_serialize_tfp_cc_v4(self) -> None:
        CurrentFormatter.formatter = CamelCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-camel-case-v4.json')) as expected_json:
            self.assertEqualJson(expected_json.read(), ThePhoenixProject.as_json(view_=SchemaVersion4))

    def test_deserialize_tfp_cc(self) -> None:
        CurrentFormatter.formatter = CamelCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-camel-case.json')) as input_json:
            book: Book = Book.from_json(data=json.loads(input_json.read()))
            self.assertEqual(str(ThePhoenixProject_v1.id), 'f3758bf0-0ff7-4366-a5e5-c209d4352b2d')
            self.assertEqual(ThePhoenixProject_v1.title, book.title)
            self.assertEqual(ThePhoenixProject_v1.isbn, book.isbn)
            self.assertEqual(ThePhoenixProject_v1.edition, book.edition)
            self.assertEqual(ThePhoenixProject_v1.publish_date, book.publish_date)
            self.assertEqual(ThePhoenixProject_v1.authors, book.authors)
            self.assertEqual(ThePhoenixProject_v1.publisher, book.publisher)
            self.assertEqual(ThePhoenixProject_v1.chapters, book.chapters)
            self.assertEqual(ThePhoenixProject_v1.references, book.references)
            self.assertEqual(ThePhoenixProject_v1.rating, book.rating)

    def test_deserialize_tfp_cc_with_references(self) -> None:
        CurrentFormatter.formatter = CamelCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-camel-case-references.json')) as input_json:
            book: Book = Book.from_json(data=json.loads(input_json.read()))
            self.assertEqual(str(ThePhoenixProject.id), 'f3758bf0-0ff7-4366-a5e5-c209d4352b2d')
            self.assertEqual(ThePhoenixProject.title, book.title)
            self.assertEqual(ThePhoenixProject.isbn, book.isbn)
            self.assertEqual(ThePhoenixProject.edition, book.edition)
            self.assertEqual(ThePhoenixProject.publish_date, book.publish_date)
            self.assertEqual(ThePhoenixProject.authors, book.authors)
            self.assertEqual(ThePhoenixProject.publisher, book.publisher)
            self.assertEqual(ThePhoenixProject.chapters, book.chapters)
            self.assertEqual(3, len(book.references))
            self.assertEqual(ThePhoenixProject.references, book.references)
            self.assertEqual(ThePhoenixProject.rating, book.rating)

    def test_deserialize_tfp_cc_with_ignored(self) -> None:
        CurrentFormatter.formatter = CamelCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-camel-case-with-ignored.json')) as input_json:
            book: Book = Book.from_json(data=json.loads(input_json.read()))
            self.assertEqual(ThePhoenixProject_v1.title, book.title)
            self.assertEqual(ThePhoenixProject_v1.isbn, book.isbn)
            self.assertEqual(ThePhoenixProject_v1.edition, book.edition)
            self.assertEqual(ThePhoenixProject_v1.publish_date, book.publish_date)
            self.assertEqual(ThePhoenixProject_v1.authors, book.authors)
            self.assertEqual(ThePhoenixProject_v1.publisher, book.publisher)
            self.assertEqual(ThePhoenixProject_v1.chapters, book.chapters)
            self.assertEqual(ThePhoenixProject_v1.rating, book.rating)

    def test_serialize_tfp_kc(self) -> None:
        CurrentFormatter.formatter = KebabCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-kebab-case.json')) as expected_json:
            self.assertEqualJson(expected_json.read(), ThePhoenixProject.as_json())

    def test_deserialize_tfp_kc(self) -> None:
        CurrentFormatter.formatter = KebabCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-kebab-case.json')) as input_json:
            book: Book = Book.from_json(data=json.loads(input_json.read()))
            self.assertEqual(ThePhoenixProject_v1.title, book.title)
            self.assertEqual(ThePhoenixProject_v1.isbn, book.isbn)
            self.assertEqual(ThePhoenixProject_v1.edition, book.edition)
            self.assertEqual(ThePhoenixProject_v1.publish_date, book.publish_date)
            self.assertEqual(ThePhoenixProject_v1.authors, book.authors)
            self.assertEqual(ThePhoenixProject_v1.publisher, book.publisher)
            self.assertEqual(ThePhoenixProject_v1.chapters, book.chapters)
            self.assertEqual(ThePhoenixProject_v1.rating, book.rating)

    def test_serialize_tfp_sc(self) -> None:
        CurrentFormatter.formatter = SnakeCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-snake-case.json')) as expected_json:
            self.assertEqualJson(expected_json.read(), ThePhoenixProject.as_json())

    def test_deserialize_tfp_sc(self) -> None:
        CurrentFormatter.formatter = SnakeCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-snake-case.json')) as input_json:
            book: Book = Book.from_json(data=json.loads(input_json.read()))
            self.assertEqual(ThePhoenixProject_v1.title, book.title)
            self.assertEqual(ThePhoenixProject_v1.isbn, book.isbn)
            self.assertEqual(ThePhoenixProject_v1.edition, book.edition)
            self.assertEqual(ThePhoenixProject_v1.publish_date, book.publish_date)
            self.assertEqual(ThePhoenixProject_v1.authors, book.authors)
            self.assertEqual(ThePhoenixProject_v1.publisher, book.publisher)
            self.assertEqual(ThePhoenixProject_v1.chapters, book.chapters)
            self.assertEqual(ThePhoenixProject_v1.rating, book.rating)
