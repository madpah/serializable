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
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

from serializable import AnySerializable, JsonSerializableObject, XmlArraySerializationType, XmlSerializableObject
from serializable.helpers import Iso8601Date

"""
Model classes used in unit tests.

"""


class Chapter(JsonSerializableObject, XmlSerializableObject):

    def __init__(self, *, number: int, title: str) -> None:
        super().__init__()
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


class Book(JsonSerializableObject, XmlSerializableObject):

    def __init__(self, title: str, isbn: str, edition: int, publish_date: date, authors: Iterable[str],
                 chapters: Optional[Iterable[Chapter]] = None) -> None:
        super().__init__()
        self._title = title
        self._isbn = isbn
        self._edition = edition
        self._publish_date = publish_date
        self._authors = set(authors)
        self.chapters = chapters or []

    @property
    def title(self) -> str:
        return self._title

    @property
    def isbn(self) -> str:
        return self._isbn

    @property
    def edition(self) -> int:
        return self._edition

    @property
    def publish_date(self) -> date:
        return self._publish_date

    @property
    def authors(self) -> Set[str]:
        return self._authors

    @property
    def chapters(self) -> List[Chapter]:
        return self._chapters

    @chapters.setter
    def chapters(self, chapters: Iterable[Chapter]) -> None:
        self._chapters = list(chapters)

    @staticmethod
    def get_property_data_class_mappings() -> Dict[str, AnySerializable]:
        return {
            "publish_date": Iso8601Date
        }

    @staticmethod
    def get_property_key_mappings() -> Dict[str, str]:
        """
        This method should return a `Dict[str, str]` that maps JSON property or key names to Python object property
        names.

        For example, in Python 'id' is a keyword and best practice is to suffix your property name with an underscore.
        Thus, your Python class might have a property named `id_` which when represented in JSON or XML should be 'id'.

        Therefor this method should return:
        ```
        {
           "id": "id_"
        }
        ```

        Returns:
            `Dict[str, str]`
        """
        return {
            "isbn": "isbn_number"
        }

    @classmethod
    def get_array_property_configuration(cls) -> Dict[str, Tuple[XmlArraySerializationType, str, Any]]:
        """

        :return:
        """
        return {
            'authors': (XmlArraySerializationType.FLAT, 'author', str),
            'chapters': (XmlArraySerializationType.NESTED, 'chapter', Chapter),
        }

    @classmethod
    def properties_as_attributes(cls) -> Set[str]:
        """
        A set of Property names that should be attributes on this class object when (de-)serialized as XML.

        Returns:
            `Set[str]`
        """
        return {'isbn'}


ThePhoenixProject = Book(
    title='The Phoenix Project', isbn='978-1942788294', edition=5, publish_date=date(year=2018, month=4, day=16),
    authors=['Gene Kim', 'Kevin Behr', 'George Spafford']
)

ThePhoenixProject.chapters.append(Chapter(number=1, title='Tuesday, September 2'))
ThePhoenixProject.chapters.append(Chapter(number=2, title='Tuesday, September 2'))
ThePhoenixProject.chapters.append(Chapter(number=3, title='Tuesday, September 2'))
ThePhoenixProject.chapters.append(Chapter(number=4, title='Wednesday, September 3'))
