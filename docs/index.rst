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

py-serializable Documentation
====================================================

This Pythonic-library can be used to magically handle serialization of your Python Objects to JSON or XML and
de-serialization from JSON or XML back to Pythonic Object instances.

This library relies upon your Python Classes utilising the `@property`_ decorator and can optionally take additional
configuration which allows you to control how a class is (de-)serialized.

See also:

- Python's `property()`_ function/decorator

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting-started
   customising-structure
   formatters
   examples
   support
   changelog


.. _@property: https://realpython.com/python-property/
.. _property(): https://docs.python.org/3/library/functions.html#property