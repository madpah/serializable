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

"""
XML-specific functionality.
"""

__all__ = ['xs_normalizedString', 'xs_token']

from enum import Enum, unique
from re import compile as re_compile
from typing import Callable, Dict, Optional

# region normalizedString

__NORMALIZED_STRING_FORBIDDEN_SEARCH = re_compile(r'\r\n|\t|\n|\r')
__NORMALIZED_STRING_FORBIDDEN_REPLACE = ' '


def xs_normalizedString(s: str) -> str:
    """Make a 'normalizedString', adhering XML spec.

    See http://www.w3.org/TR/xmlschema-2/#normalizedString

    Quote from the XML schema spec:
    > *normalizedString* represents white space normalized strings.
    > The [·value space·](https://www.w3.org/TR/xmlschema-2/#dt-value-space) of normalizedString is the set of strings
    > that do not contain the carriage return (#xD), line feed (#xA) nor tab (#x9) characters.
    > The [·lexical space·](https://www.w3.org/TR/xmlschema-2/#dt-lexical-space) of normalizedString is the set of
    > strings that do not contain the carriage return (#xD), line feed (#xA) nor tab (#x9) characters.
    > The [·base type·](https://www.w3.org/TR/xmlschema-2/#dt-basetype) of normalizedString is
    > [string](https://www.w3.org/TR/xmlschema-2/#string).
    """
    return __NORMALIZED_STRING_FORBIDDEN_SEARCH.sub(
        __NORMALIZED_STRING_FORBIDDEN_REPLACE,
        s)


# endregion

# region token


__TOKEN_MULTISTRING_SEARCH = re_compile(r' {2,}')
__TOKEN_MULTISTRING_REPLACE = ' '


def xs_token(s: str) -> str:
    """Make a 'token', adhering XML spec.

    See http://www.w3.org/TR/xmlschema-2/#token

    Quote from the XML schema spec:
    > *token* represents tokenized strings.
    > The [·value space·](https://www.w3.org/TR/xmlschema-2/#dt-value-space) of token is the set of strings that do not
    > contain the carriage return (#xD), line feed (#xA) nor tab (#x9) characters, that have no leading or trailing
    > spaces (#x20) and that have no internal sequences of two or more spaces.
    > The [·lexical space·](https://www.w3.org/TR/xmlschema-2/#dt-lexical-space) of token is the set of strings that do
    > not contain the carriage return (#xD), line feed (#xA) nor tab (#x9) characters, that have no leading or trailing
    > spaces (#x20) and that have no internal sequences of two or more spaces.
    > The [·base type·](https://www.w3.org/TR/xmlschema-2/#dt-basetype) of token is
    > [normalizedString](https://www.w3.org/TR/xmlschema-2/#normalizedString).
    """
    return __TOKEN_MULTISTRING_SEARCH.sub(
        __TOKEN_MULTISTRING_REPLACE,
        xs_normalizedString(s).strip())

# endregion
