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

from datetime import date, datetime, timedelta, timezone
from unittest import TestCase

from serializable import logger
from serializable.helpers import Iso8601Date, XsdDate, XsdDateTime


class TestIso8601Date(TestCase):

    def test_serialize_date(self) -> None:
        self.assertEqual(
            Iso8601Date.serialize(date(year=2022, month=8, day=3)),
            '2022-08-03'
        )

    def test_serialize_datetime(self) -> None:
        self.assertEqual(
            Iso8601Date.serialize(datetime(year=2022, month=8, day=3)),
            '2022-08-03'
        )

    def test_deserialize_valid_date(self) -> None:
        self.assertEqual(
            Iso8601Date.deserialize('2022-08-03'),
            date(year=2022, month=8, day=3)
        )

    def test_deserialize_valid(self) -> None:
        with self.assertRaises(ValueError):
            Iso8601Date.deserialize('2022-08-03zzz')


class TestXsdDate(TestCase):
    """
    See: http://books.xmlschemata.org/relaxng/ch19-77041.html
    """

    def test_deserialize_valid_1(self) -> None:
        self.assertEqual(
            XsdDate.deserialize('2001-10-26'),
            date(year=2001, month=10, day=26)
        )

    def test_deserialize_valid_2(self) -> None:
        with self.assertLogs(logger) as logs:
            self.assertEqual(
                XsdDate.deserialize('2001-10-26+02:00'),
                date(year=2001, month=10, day=26)
            )
        self.assertIn(
            'WARNING:serializable.helpers:'
            'Potential data loss will occur: dates with timezones not supported in Python',
            logs.output)

    def test_deserialize_valid_3(self) -> None:
        with self.assertLogs(logger) as logs:
            self.assertEqual(
                XsdDate.deserialize('2001-10-26Z'),
                date(year=2001, month=10, day=26)
            )
        self.assertIn(
            'WARNING:serializable.helpers:'
            'Potential data loss will occur: dates with timezones not supported in Python',
            logs.output)

    def test_deserialize_valid_4(self) -> None:
        with self.assertLogs(logger) as logs:
            self.assertEqual(
                XsdDate.deserialize('2001-10-26+00:00'),
                date(year=2001, month=10, day=26)
            )
        self.assertIn(
            'WARNING:serializable.helpers:'
            'Potential data loss will occur: dates with timezones not supported in Python',
            logs.output)

    def test_deserialize_valid_5(self) -> None:
        self.assertEqual(
            XsdDate.deserialize('-2001-10-26'),
            date(year=2001, month=10, day=26)
        )

    def test_serialize_1(self) -> None:
        self.assertEqual(
            XsdDate.serialize(date(year=2001, month=10, day=26)),
            '2001-10-26'
        )


class TestXsdDateTime(TestCase):
    """
    See: http://books.xmlschemata.org/relaxng/ch19-77049.html
    """

    def test_deserialize_valid_1(self) -> None:
        self.assertEqual(
            XsdDateTime.deserialize('2001-10-26T21:32:52'),
            datetime(year=2001, month=10, day=26, hour=21, minute=32, second=52, tzinfo=None)
        )

    def test_deserialize_valid_2(self) -> None:
        self.assertEqual(
            XsdDateTime.deserialize('2001-10-26T21:32:52+02:00'),
            datetime(
                year=2001, month=10, day=26, hour=21, minute=32, second=52,
                tzinfo=timezone(timedelta(seconds=7200))
            )
        )

    def test_deserialize_valid_3(self) -> None:
        self.assertEqual(
            XsdDateTime.deserialize('2001-10-26T19:32:52Z'),
            datetime(year=2001, month=10, day=26, hour=19, minute=32, second=52, tzinfo=timezone.utc)
        )

    def test_deserialize_valid_4(self) -> None:
        self.assertEqual(
            XsdDateTime.deserialize('2001-10-26T19:32:52+00:00'),
            datetime(year=2001, month=10, day=26, hour=19, minute=32, second=52, tzinfo=timezone.utc)
        )

    def test_deserialize_valid_5(self) -> None:
        self.assertEqual(
            XsdDateTime.deserialize('-2001-10-26T21:32:52'),
            datetime(year=2001, month=10, day=26, hour=21, minute=32, second=52, tzinfo=None)
        )

    def test_deserialize_valid_6(self) -> None:
        self.assertEqual(
            XsdDateTime.deserialize('2001-10-26T21:32:52.12679'),
            datetime(year=2001, month=10, day=26, hour=21, minute=32, second=52, microsecond=12679, tzinfo=None)
        )

    def test_serialize_1(self) -> None:
        serialized = XsdDateTime.serialize(
            # assume winter time
            datetime(year=2001, month=2, day=26, hour=21, minute=32, second=52, microsecond=12679, tzinfo=None)
        )
        self.assertRegex(serialized, r'2001-02-26T21:32:52.012679(?:Z|[+-]\d\d:\d\d)')

    def test_serialize_2(self) -> None:
        serialized = XsdDateTime.serialize(
            # assume summer time
            datetime(year=2001, month=7, day=26, hour=21, minute=32, second=52, microsecond=12679, tzinfo=None)
        )
        self.assertRegex(serialized, r'2001-07-26T21:32:52.012679(?:Z|[+-]\d\d:\d\d)')

    def test_serialize_3(self) -> None:
        serialized = XsdDateTime.serialize(
            datetime(
                year=2001, month=10, day=26, hour=21, minute=32, second=52, microsecond=12679, tzinfo=timezone.utc
            )
        )
        self.assertEqual(serialized, '2001-10-26T21:32:52.012679+00:00')
