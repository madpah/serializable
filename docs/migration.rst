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

Migration
=========

.. _v1_v2:

From v1 to v2
-------------

The package was renamed from ``serializable`` to ``py_serializable``.
Therefore, you need to adjust your imports.

The following shows a quick way to adjust imports in the most efficient way.

.. code-block:: python
   :caption: OLD imports

   import serializable
   from serializable import ViewType, XmlArraySerializationType, XmlStringSerializationType
   from serializable.helpers import BaseHelper, Iso8601Date


.. code-block:: python
   :caption: ADJUSTED imports

   import py_serializable as serializable
   from py_serializable import ViewType, XmlArraySerializationType, XmlStringSerializationType
   from py_serializable.helpers import BaseHelper, Iso8601Date

