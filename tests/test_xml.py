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

import logging
import os
from copy import deepcopy

from defusedxml import ElementTree as SafeElementTree

from serializable.formatters import (
    CamelCasePropertyNameFormatter,
    CurrentFormatter,
    KebabCasePropertyNameFormatter,
    SnakeCasePropertyNameFormatter,
)
from tests.base import FIXTURES_DIRECTORY, BaseTestCase, DeepCompareMixin
from tests.model import (
    Book,
    SchemaVersion2,
    SchemaVersion3,
    SchemaVersion4,
    ThePhoenixProject,
    ThePhoenixProject_unnormalized,
    ThePhoenixProject_v1,
)

logger = logging.getLogger('serializable')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class TestXml(BaseTestCase, DeepCompareMixin):

    # region test_serialize

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

    def test_serialize_tfp_cc1_v4(self) -> None:
        CurrentFormatter.formatter = CamelCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-camel-case-1-v4.xml')) as expected_xml:
            self.assertEqualXml(expected_xml.read(), ThePhoenixProject.as_xml(SchemaVersion4))

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
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-snake-case-1.xml'), 'r') as expected_xml:
            self.assertEqualXml(expected_xml.read(), ThePhoenixProject.as_xml())

    def test_serializable_no_defaultNS(self) -> None:
        """regression test for https://github.com/madpah/serializable/issues/12"""
        from xml.etree import ElementTree
        xmlns = 'http://the.phoenix.project/testing/defaultNS'
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-defaultNS-unset.SNAPSHOT.xml')) as expected_xml:
            expected = expected_xml.read()
        data = deepcopy(ThePhoenixProject_v1)
        data._authors = {'Karl Ranseier', }  # only one item, so order is no issue
        actual = ElementTree.tostring(
            data.as_xml(as_string=False, xmlns=xmlns),
            method='xml',
            encoding='unicode',
            # default_namespace=None
        )
        # byte-wise string compare is intentional!
        self.maxDiff = None
        self.assertEqual(expected, actual)

    def test_serializable_with_defaultNS(self) -> None:
        """regression test for https://github.com/madpah/serializable/issues/12"""
        from xml.etree import ElementTree
        xmlns = 'http://the.phoenix.project/testing/defaultNS'
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-defaultNS-isset.SNAPSHOT.xml')) as expected_xml:
            expected = expected_xml.read()
        data = deepcopy(ThePhoenixProject_v1)
        data._authors = {'Karl Ranseier', }  # only one item, so order is no issue
        actual = ElementTree.tostring(
            data.as_xml(SchemaVersion4, as_string=False, xmlns=xmlns),
            method='xml',
            encoding='unicode',
            default_namespace=xmlns,
        )
        # byte-wise string compare is intentional!
        self.maxDiff = None
        self.assertEqual(expected, actual)

    def test_serialize_unnormalized(self) -> None:
        """regression test #119
        for https://github.com/madpah/serializable/issues/114
        and https://github.com/madpah/serializable/issues/115
        """
        CurrentFormatter.formatter = CamelCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-camel-case-1-v4.xml')) as expected_xml:
            self.assertEqualXml(expected_xml.read(), ThePhoenixProject_unnormalized.as_xml(SchemaVersion4))

    # endregion test_serialize

    # region test_deserialize

    def test_deserialize_tfp_cc1(self) -> None:
        CurrentFormatter.formatter = CamelCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-camel-case-1-v1.xml')) as input_xml:
            book: Book = Book.from_xml(data=SafeElementTree.fromstring(input_xml.read()))
            self.assertEqual(ThePhoenixProject_v1.title, book.title)
            self.assertEqual(ThePhoenixProject_v1.isbn, book.isbn)
            self.assertEqual(ThePhoenixProject_v1.edition, book.edition)
            self.assertEqual(ThePhoenixProject_v1.publish_date, book.publish_date)
            self.assertEqual(ThePhoenixProject_v1.publisher, book.publisher)
            self.assertEqual(ThePhoenixProject_v1.authors, book.authors)
            self.assertEqual(ThePhoenixProject_v1.chapters, book.chapters)
            self.assertEqual(ThePhoenixProject_v1.rating, book.rating)

    def test_deserialize_tfp_cc1_v2(self) -> None:
        CurrentFormatter.formatter = CamelCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-camel-case-1-v2.xml')) as input_xml:
            book: Book = Book.from_xml(data=SafeElementTree.fromstring(input_xml.read()))
            self.assertEqual(ThePhoenixProject.title, book.title)
            self.assertEqual(ThePhoenixProject.isbn, book.isbn)
            self.assertEqual(ThePhoenixProject.edition, book.edition)
            self.assertEqual(ThePhoenixProject.publish_date, book.publish_date)
            self.assertEqual(ThePhoenixProject.publisher.name, book.publisher.name)
            self.assertEqual(ThePhoenixProject.publisher.address, book.publisher.address)
            self.assertEqual(ThePhoenixProject.authors, book.authors)
            self.assertEqual(ThePhoenixProject.chapters, book.chapters)
            self.assertSetEqual(set(), book.references)
            self.assertEqual(ThePhoenixProject.rating, book.rating)

    def test_deserialize_tfp_cc1_v3(self) -> None:
        CurrentFormatter.formatter = CamelCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-camel-case-1-v3.xml')) as input_xml:
            book: Book = Book.from_xml(data=SafeElementTree.fromstring(input_xml.read()))
            self.assertEqual(ThePhoenixProject_v1.title, book.title)
            self.assertEqual(ThePhoenixProject_v1.isbn, book.isbn)
            self.assertEqual(ThePhoenixProject_v1.edition, book.edition)
            self.assertEqual(ThePhoenixProject_v1.publish_date, book.publish_date)
            self.assertEqual(ThePhoenixProject_v1.publisher.name, book.publisher.name)
            self.assertEqual(ThePhoenixProject_v1.publisher.address, book.publisher.address)
            self.assertEqual(ThePhoenixProject_v1.authors, book.authors)
            self.assertEqual(ThePhoenixProject_v1.chapters, book.chapters)
            self.assertEqual(ThePhoenixProject_v1.references, book.references)
            self.assertEqual(ThePhoenixProject_v1.rating, book.rating)

    def test_deserialize_tfp_cc1_v4(self) -> None:
        CurrentFormatter.formatter = CamelCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-camel-case-1-v4.xml')) as input_xml:
            book: Book = Book.from_xml(data=SafeElementTree.fromstring(input_xml.read()))
            self.assertEqual(ThePhoenixProject.title, book.title)
            self.assertEqual(ThePhoenixProject.isbn, book.isbn)
            self.assertEqual(ThePhoenixProject.edition, book.edition)
            self.assertEqual(ThePhoenixProject.publish_date, book.publish_date)
            self.assertEqual(ThePhoenixProject.publisher.name, book.publisher.name)
            self.assertEqual(ThePhoenixProject.publisher.address, book.publisher.address)
            self.assertEqual(ThePhoenixProject.authors, book.authors)
            self.assertEqual(ThePhoenixProject.chapters, book.chapters)
            self.assertEqual(ThePhoenixProject.references, book.references)
            self.assertEqual(ThePhoenixProject.rating, book.rating)

    def test_deserialize_tfp_cc1_with_ignored(self) -> None:
        CurrentFormatter.formatter = CamelCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-camel-case-with-ignored.xml')) as input_xml:
            book: Book = Book.from_xml(data=SafeElementTree.fromstring(input_xml.read()))
            self.assertEqual(ThePhoenixProject_v1.title, book.title)
            self.assertEqual(ThePhoenixProject_v1.isbn, book.isbn)
            self.assertEqual(ThePhoenixProject_v1.edition, book.edition)
            self.assertEqual(ThePhoenixProject_v1.publish_date, book.publish_date)
            self.assertEqual(ThePhoenixProject_v1.publisher, book.publisher)
            self.assertEqual(ThePhoenixProject_v1.authors, book.authors)
            self.assertEqual(ThePhoenixProject_v1.chapters, book.chapters)
            self.assertEqual(ThePhoenixProject_v1.rating, book.rating)

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
            self.assertEqual(ThePhoenixProject_v1.rating, book.rating)

    def test_deserialize_tfp_sc1(self) -> None:
        CurrentFormatter.formatter = SnakeCasePropertyNameFormatter
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-snake-case-1.xml')) as input_xml:
            book: Book = Book.from_xml(data=SafeElementTree.fromstring(input_xml.read()))
            self.assertEqual(ThePhoenixProject_v1.title, book.title)
            self.assertEqual(ThePhoenixProject_v1.isbn, book.isbn)
            self.assertEqual(ThePhoenixProject_v1.edition, book.edition)
            self.assertEqual(ThePhoenixProject_v1.publish_date, book.publish_date)
            self.assertEqual(ThePhoenixProject_v1.publisher, book.publisher)
            self.assertEqual(ThePhoenixProject_v1.authors, book.authors)
            self.assertEqual(ThePhoenixProject_v1.chapters, book.chapters)
            self.assertEqual(ThePhoenixProject_v1.rating, book.rating)

    def test_deserializable_with_defaultNS(self) -> None:
        """regression test for https://github.com/madpah/serializable/issues/11"""
        expected = ThePhoenixProject
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-defaultNS-isset-v4.xml')) as fixture_xml:
            actual = Book.from_xml(fixture_xml)
        self.assertDeepEqual(expected, actual)

    def test_deserializable_no_defaultNS_explicit(self) -> None:
        """regression test for https://github.com/madpah/serializable/issues/11"""
        expected = ThePhoenixProject
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-defaultNS-unset-v4.xml')) as fixture_xml:
            actual = Book.from_xml(fixture_xml, 'http://the.phoenix.project/testing/defaultNS')
        self.assertDeepEqual(expected, actual)

    def test_deserializable_no_defaultNS_autodetect(self) -> None:
        """regression test for https://github.com/madpah/serializable/issues/11"""
        expected = ThePhoenixProject
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-defaultNS-unset-v4.xml')) as fixture_xml:
            actual = Book.from_xml(fixture_xml)
        self.assertDeepEqual(expected, actual)

    def test_deserializable_mixed_defaultNS_autodetect(self) -> None:
        """regression test for https://github.com/madpah/serializable/issues/11"""
        expected = ThePhoenixProject
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project-defaultNS-mixed-v4.xml')) as fixture_xml:
            actual = Book.from_xml(fixture_xml)
        self.assertDeepEqual(expected, actual)

    def test_deserializable_unnormalized(self) -> None:
        """regression test #119
        for https://github.com/madpah/serializable/issues/114
        and https://github.com/madpah/serializable/issues/115
        """
        expected = ThePhoenixProject
        with open(os.path.join(FIXTURES_DIRECTORY, 'the-phoenix-project_unnormalized-input_v4.xml')) as fixture_xml:
            actual = Book.from_xml(fixture_xml)
        self.assertDeepEqual(expected, actual)

    # region test_deserialize
