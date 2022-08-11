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

from serializable import CurrentFormatter, DefaultJsonEncoder
from serializable.formatters import (
    CamelCasePropertyNameFormatter,
    KebabCasePropertyNameFormatter,
    SnakeCasePropertyNameFormatter,
)
from tests.base import FIXTURES_DIRECTORY, BaseTestCase
from tests.model import Book, ThePhoenixProject


class TestJson(BaseTestCase):

    def test_serialize_tfp_cc(self) -> None:
        CurrentFormatter.formatter = CamelCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-camel-case.json')) as expected_json:
            self.assertEqualJson(expected_json.read(), json.dumps(ThePhoenixProject, cls=DefaultJsonEncoder))

    def test_deserialize_tfp_cc(self) -> None:
        CurrentFormatter.formatter = CamelCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-camel-case.json')) as input_json:
            book: Book = Book.from_json(data=json.loads(input_json.read()))
            self.assertEqual(ThePhoenixProject.title, book.title)
            self.assertEqual(ThePhoenixProject.isbn, book.isbn)
            self.assertEqual(ThePhoenixProject.edition, book.edition)
            self.assertEqual(ThePhoenixProject.publish_date, book.publish_date)
            self.assertEqual(ThePhoenixProject.authors, book.authors)
            self.assertEqual(ThePhoenixProject.publisher,
                             book.publisher)
            self.assertEqual(ThePhoenixProject.chapters, book.chapters)

    def test_serialize_tfp_kc(self) -> None:
        CurrentFormatter.formatter = KebabCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-kebab-case.json')) as expected_json:
            self.assertEqualJson(expected_json.read(), json.dumps(ThePhoenixProject, cls=DefaultJsonEncoder))

    def test_deserialize_tfp_kc(self) -> None:
        CurrentFormatter.formatter = KebabCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-kebab-case.json')) as input_json:
            book: Book = Book.from_json(data=json.loads(input_json.read()))
            self.assertEqual(ThePhoenixProject.title, book.title)
            self.assertEqual(ThePhoenixProject.isbn, book.isbn)
            self.assertEqual(ThePhoenixProject.edition, book.edition)
            self.assertEqual(ThePhoenixProject.publish_date, book.publish_date)
            self.assertEqual(ThePhoenixProject.authors, book.authors)
            self.assertEqual(ThePhoenixProject.publisher, book.publisher)
            self.assertEqual(ThePhoenixProject.chapters, book.chapters)

    def test_serialize_tfp_sc(self) -> None:
        CurrentFormatter.formatter = SnakeCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-snake-case.json')) as expected_json:
            self.assertEqualJson(expected_json.read(), json.dumps(ThePhoenixProject, cls=DefaultJsonEncoder))

    def test_deserialize_tfp_sc(self) -> None:
        CurrentFormatter.formatter = SnakeCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-snake-case.json')) as input_json:
            book: Book = Book.from_json(data=json.loads(input_json.read()))
            self.assertEqual(ThePhoenixProject.title, book.title)
            self.assertEqual(ThePhoenixProject.isbn, book.isbn)
            self.assertEqual(ThePhoenixProject.edition, book.edition)
            self.assertEqual(ThePhoenixProject.publish_date, book.publish_date)
            self.assertEqual(ThePhoenixProject.authors, book.authors)
            self.assertEqual(ThePhoenixProject.publisher, book.publisher)
            self.assertEqual(ThePhoenixProject.chapters, book.chapters)
