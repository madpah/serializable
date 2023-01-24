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
from datetime import date
from enum import Enum, unique
from typing import Iterable, List, Optional, Set
from uuid import UUID, uuid4

import serializable
from serializable import ViewType, XmlArraySerializationType
from serializable.helpers import Iso8601Date

"""
Model classes used in unit tests.

"""


class SchemaVersion1(ViewType):
    pass


class SchemaVersion2(ViewType):
    pass


class SchemaVersion3(ViewType):
    pass


@serializable.serializable_class
class Chapter:

    def __init__(self, *, number: int, title: str) -> None:
        self._number = number
        self._title = title

    @property
    def number(self) -> int:
        return self._number

    @property
    def title(self) -> str:
        return self._title

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Chapter):
            return hash(other) == hash(self)
        return False

    def __hash__(self) -> int:
        return hash((self.number, self.title))


@serializable.serializable_class
class Publisher:

    def __init__(self, *, name: str, address: Optional[str] = None, email: Optional[str] = None) -> None:
        self._name = name
        self._address = address
        self._email = email

    @property
    def name(self) -> str:
        return self._name

    @property  # type: ignore[misc]
    @serializable.view(SchemaVersion2)
    def address(self) -> Optional[str]:
        return self._address

    @property  # type: ignore[misc]
    @serializable.include_none(SchemaVersion2)
    @serializable.include_none(SchemaVersion3, "RUBBISH")
    def email(self) -> Optional[str]:
        return self._email

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Publisher):
            return hash(other) == hash(self)
        return False

    def __hash__(self) -> int:
        return hash((self.name, self.address))


@unique
class BookType(Enum):
    FICTION = 'fiction'
    NON_FICTION = 'non-fiction'


@serializable.serializable_class(name='edition')
class BookEdition:

    def __init__(self, *, number: int, name: str) -> None:
        self._number = number
        self._name = name

    @property  # type: ignore[misc]
    @serializable.xml_attribute()
    def number(self) -> int:
        return self._number

    @property  # type: ignore[misc]
    @serializable.xml_name('.')
    def name(self) -> str:
        return self._name

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BookEdition):
            return hash(other) == hash(self)
        return False

    def __hash__(self) -> int:
        return hash((self.number, self.name))


@serializable.serializable_class(name='bigbook',
                                 ignore_during_deserialization=['something_to_be_ignored', 'ignore_me', 'ignored'])
class Book:

    def __init__(self, title: str, isbn: str, publish_date: date, authors: Iterable[str],
                 publisher: Optional[Publisher] = None, chapters: Optional[Iterable[Chapter]] = None,
                 edition: Optional[BookEdition] = None, type_: BookType = BookType.FICTION,
                 id_: Optional[UUID] = None) -> None:
        self._id_ = id_ or uuid4()
        self._title = title
        self._isbn = isbn
        self._edition = edition
        self._publish_date = publish_date
        self._authors = set(authors)
        self._publisher = publisher
        self.chapters = list(chapters or [])
        self._type_ = type_

    @property  # type: ignore[misc]
    @serializable.xml_sequence(1)
    def id_(self) -> UUID:
        return self._id_

    @property  # type: ignore[misc]
    @serializable.xml_sequence(2)
    def title(self) -> str:
        return self._title

    @property  # type: ignore[misc]
    @serializable.json_name('isbn_number')
    @serializable.xml_attribute()
    @serializable.xml_name('isbn_number')
    def isbn(self) -> str:
        return self._isbn

    @property  # type: ignore[misc]
    @serializable.xml_sequence(3)
    def edition(self) -> Optional[BookEdition]:
        return self._edition

    @property  # type: ignore[misc]
    @serializable.xml_sequence(4)
    @serializable.type_mapping(Iso8601Date)
    def publish_date(self) -> date:
        return self._publish_date

    @property  # type: ignore[misc]
    @serializable.xml_array(XmlArraySerializationType.FLAT, 'author')
    @serializable.xml_sequence(5)
    def authors(self) -> Set[str]:
        return self._authors

    @property  # type: ignore[misc]
    @serializable.xml_sequence(7)
    def publisher(self) -> Optional[Publisher]:
        return self._publisher

    @property  # type: ignore[misc]
    @serializable.xml_array(XmlArraySerializationType.NESTED, 'chapter')
    @serializable.xml_sequence(8)
    def chapters(self) -> List[Chapter]:
        return self._chapters

    @chapters.setter
    def chapters(self, chapters: Iterable[Chapter]) -> None:
        self._chapters = list(chapters)

    @property  # type: ignore[misc]
    @serializable.xml_sequence(6)
    def type_(self) -> BookType:
        return self._type_


ThePhoenixProject_v1 = Book(
    title='The Phoenix Project', isbn='978-1942788294', publish_date=date(year=2018, month=4, day=16),
    authors=['Gene Kim', 'Kevin Behr', 'George Spafford'],
    publisher=Publisher(name='IT Revolution Press LLC'),
    edition=BookEdition(number=5, name='5th Anniversary Limited Edition'),
    id_=UUID('f3758bf0-0ff7-4366-a5e5-c209d4352b2d')
)

ThePhoenixProject_v1.chapters.append(Chapter(number=1, title='Tuesday, September 2'))
ThePhoenixProject_v1.chapters.append(Chapter(number=2, title='Tuesday, September 2'))
ThePhoenixProject_v1.chapters.append(Chapter(number=3, title='Tuesday, September 2'))
ThePhoenixProject_v1.chapters.append(Chapter(number=4, title='Wednesday, September 3'))

ThePhoenixProject_v2 = Book(
    title='The Phoenix Project', isbn='978-1942788294', publish_date=date(year=2018, month=4, day=16),
    authors=['Gene Kim', 'Kevin Behr', 'George Spafford'],
    publisher=Publisher(name='IT Revolution Press LLC', address='10 Downing Street'),
    edition=BookEdition(number=5, name='5th Anniversary Limited Edition'),
    id_=UUID('f3758bf0-0ff7-4366-a5e5-c209d4352b2d')
)

ThePhoenixProject_v2.chapters.append(Chapter(number=1, title='Tuesday, September 2'))
ThePhoenixProject_v2.chapters.append(Chapter(number=2, title='Tuesday, September 2'))
ThePhoenixProject_v2.chapters.append(Chapter(number=3, title='Tuesday, September 2'))
ThePhoenixProject_v2.chapters.append(Chapter(number=4, title='Wednesday, September 3'))

ThePhoenixProject = ThePhoenixProject_v2
