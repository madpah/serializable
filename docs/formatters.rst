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

Property Name Formatting
====================================================

By default, ``py-serializable`` uses it's :class:`serializable.formatters.CamelCasePropertyNameFormatter` formatter for
translating actual Python property names to element names in either JSON or XML.

``py-serializable`` includes a number of name formatters out of the box, but you can also create your own if required.

Included Formatters
----------------------------------------------------

``py-serializable`` includes three common formatters out of the box.

1. Camel Case Formatter: :class:`serializable.formatters.CamelCasePropertyNameFormatter` (the default)
2. Kebab Case Formatter: :class:`serializable.formatters.KebabCasePropertyNameFormatter`
3. Snake Case Formatter: :class:`serializable.formatters.SnakeCasePropertyNameFormatter`

A summary of how these differ is included in the below table.

+----------------------------+---------------+----------------+-----------------+
| Python Property Name       | Camel Case    | Kebab Case     | Snake Case      |
+============================+===============+================+=================+
| books                      | books         | books          | books           |
+----------------------------+---------------+----------------+-----------------+
| big_book                   | bigBook       | big-book       | big_book        |
+----------------------------+---------------+----------------+-----------------+
| a_very_big_book            | aVeryBigBook  | a-very-big-book| a_very_big_book |
+----------------------------+---------------+----------------+-----------------+

Changing the Formatter
----------------------

You can change the formatter being used by easily. The example below changes the formatter to be Snake Case.

.. code-block:: python

    from serializable.formatters import CurrentFormatter, SnakeCasePropertyNameFormatter

    CurrentFormatter.formatter = SnakeCasePropertyNameFormatter

Custom Formatters
-----------------

If none of the included formatters work for you, why not write your own?

The only requirement is that it extends :class:`serializable.formatters.BaseNameFormatter`!
