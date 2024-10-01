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
from unittest import TestCase, mock

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
        """Test that less than 6 decimal places in the seconds field is padded to 6 and parsed correctly."""

        # Use mock wrapping datetime so we can check that it was given a correctly padded string
        with mock.patch('serializable.helpers.datetime', wraps=datetime) as datetime_mock:

            # Make sure the parsed datetime is what we expect
            self.assertEqual(
                XsdDateTime.deserialize('2001-10-26T21:32:52.12679'),
                datetime(year=2001, month=10, day=26, hour=21, minute=32, second=52, microsecond=126790, tzinfo=None)
            )

            # Make sure the string provided to fromisoformat was correctly padded (pre 3.11 it needs 0 or 6 decimals)
            datetime_mock.fromisoformat.assert_called_with('2001-10-26T21:32:52.126790')

    def test_deserialize_valid_7(self) -> None:
        """Test that exactly 6 decimal places in the seconds field is not altered and parsed correctly."""

        # Use mock wrapping datetime so we can check that the string was not altered
        with mock.patch('serializable.helpers.datetime', wraps=datetime) as datetime_mock:

            # Make sure the parsed datetime is what we expect
            self.assertEqual(
                XsdDateTime.deserialize('2024-09-23T08:06:09.185596Z'),
                datetime(year=2024, month=9, day=23, hour=8, minute=6,
                         second=9, microsecond=185596, tzinfo=timezone.utc)
            )

            # Make sure the string provided to fromisoformat was not altered (pre 3.11 it needs 0 or 6 decimals)
            datetime_mock.fromisoformat.assert_called_with('2024-09-23T08:06:09.185596+00:00')

    def test_deserialize_valid_8(self) -> None:
        """Test that more than 6 decimal places in the seconds field is truncated and parsed correctly."""

        # Use mock wrapping datetime so we can check that the string was truncated
        with mock.patch('serializable.helpers.datetime', wraps=datetime) as datetime_mock:

            # Make sure the parsed datetime is what we expect
            self.assertEqual(
                XsdDateTime.deserialize('2024-09-23T08:06:09.185596536Z'),
                datetime(year=2024, month=9, day=23, hour=8, minute=6,
                         second=9, microsecond=185597, tzinfo=timezone.utc)
            )

            # Make sure the string provided to fromisoformat was truncated (pre 3.11 it needs 0 or 6 decimals)
            datetime_mock.fromisoformat.assert_called_with('2024-09-23T08:06:09.185597+00:00')

    def test_deserialize_valid_9(self) -> None:
        """Test that a lot more than 6 decimal places in the seconds field is truncated and parsed correctly."""

        # Use mock wrapping datetime so we can check that the string was truncated
        with mock.patch('serializable.helpers.datetime', wraps=datetime) as datetime_mock:

            self.assertEqual(
                XsdDateTime.deserialize('2024-09-23T08:06:09.18559653666666666666666666666666'),
                datetime(year=2024, month=9, day=23, hour=8, minute=6, second=9, microsecond=185597, tzinfo=None)
            )

            # Make sure the string provided to fromisoformat was truncated (pre 3.11 it needs 0 or 6 decimals)
            datetime_mock.fromisoformat.assert_called_with('2024-09-23T08:06:09.185597')

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
