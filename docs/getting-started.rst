..  # This file is part of py-serializable
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

Getting Started
====================================================

Let's work a simple example together.

I have a two Python classes that together I use to model Books. They are ``Book`` and ``Chapter``, and they are defined
as follows:

.. code-block:: python

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

    class Book:

        def __init__(self, *, title: str, isbn: str, edition: int, publish_date: date, authors: Iterable[str],
                     chapters: Optional[Iterable[Chapter]] = None) -> None:
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

To make a class serializable to/from JSON or XML, the class must be annotated with the decorator
:func:`serializable.serializable_class`.

By simply modifying the classes above, we make them (de-)serializable with this library (albeit with some default
behaviour implied!).

This makes our classes:

.. code-block:: python

    import serializable

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

    @serializable.serializable_class
    class Book:

        def __init__(self, *, title: str, isbn: str, edition: int, publish_date: date, authors: Iterable[str],
                     chapters: Optional[Iterable[Chapter]] = None) -> None:
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

At this point, we can serialize an instance of ``Book`` to JSON as follows:

.. code-block:: python

    book = Book(title="My Book", isbn="999-888777666555", edition=1, publish_date=datetime.utcnow(), authors=['me'])
    print(book.as_json())

which outputs:

.. code-block:: json

    {
        "title": "My Book",
        "isbn": "999-888777666555",
        "edition": 1,
        "publishDate": "2022-08-10",
        "authors": [
            "me"
        ]
    }

We could also serialized to XML as follows:

.. code-block:: python

    print(book.as_xml())

which outputs:

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <book>
        <title>My Book</title>
        <isbn>999-888777666555</isbn>
        <edition>1</edition>
        <publishDate>2022-08-10</publishDate>
        <author>me</author>
    </book>
