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

Customising Serialization
====================================================

There are various scenarios whereby you may want to have more control over the structure (particularly in XML) that is
generated when serializing an object, and thus understanding how to deserialize JSON or XML back to an object.

This library provides a number of *meta methods* that you can override in your Python classes to achieve this.

Property Name Mappings
----------------------------------------------------

You can directly control mapping of property names for certain properties in a Class by implementing the
:obj:`serializable.SerializableObject.get_property_key_mappings()` static method.

For example, you might have a property called **isbn** in your class, but when serialized it should be called
**isbn_number**.

To implement this mapping, you would add the following method to your class:

.. code-block::

    @staticmethod
    def get_property_key_mappings() -> Dict[str, str]:
        return {
            "isbn": "isbn_number"
        }

Excluding Property from Serialization
----------------------------------------------------

You can exclude a Property from serialization by implementing
:obj:`serializable.SerializableObject.get_json_key_removals()` in your class. For example, the below example would
prevent the property ``cost_price`` from being included in serialization output.

.. code-block::

    @staticmethod
    def get_json_key_removals() -> List[str]:
        return ["cost_price"]


Customised Property Serialization
----------------------------------------------------

This feature allows you to handle, for example, serialization of :obj:`datetime.date` native Python objects to and
from strings.

Depending on your use case, the string format could vary, and thus this library makes no assumptions. We have provided
an example helper for (de-)serializing ISO-8601 compliant date strings.

To define a custom serializer for a property, implement the
:obj:`serializable.SerializableObject.get_property_data_class_mappings()` method in your
class. For example, to have a property named *created* be use the :obj:`serializable.helpers.Iso8601Date` helper you
would add the following method to your class:

.. code-block::

    @staticmethod
    def get_property_data_class_mappings() -> Dict[str, AnySerializable]:
        return {
            "created": Iso8601Date
        }

Writing Custom Property Serializers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can write your own custom property serializer by subclassing :obj:`serializable.SimpleSerializable`.


Serializing Lists & Sets
----------------------------------------------------

Particularly in XML, there are many ways that properties which return Lists or Sets could be represented. We can handle
this by implementing the :obj:`serializable.SerializableObject.get_array_property_configuration()` method in your
class.

For example, given a Property that returns ``Set[Chapter]``, this could be serialized in one of a number of ways:

*Example 1: Nested list under a property name in JSON*

.. code-block::

    {
        "chapters": [
            { chapter 1 here... },
            { chapter 2 here... },
            etc...
        ]
    }

*Example 2: Nested list under a property name in XML*

.. code-block::

    <chapters>
        <chapter>chapter 1 here</chapter>
        <chapter>chapter 2 here</chapter>
        etc...
    </chapters>

*Example 3: Collapsed list under a (potentially singular of the) property name in XML*

.. code-block::

    <chapter>chapter 1 here</chapter>
    <chapter>chapter 2 here</chapter>

.. note:

    Other structures may also be possible, but only the above are considered by this library at the current time.

As we have only identified one possible structure for JSON at this time, the implementation of
only affects XML (de-)serialization at this time.

For *Example 2*, you would add the following to your class:

.. code-block::

    @classmethod
    def get_array_property_configuration(cls) -> Dict[str, Tuple[XmlArraySerializationType, str, Any]]:
        return {
            "chapters": (XmlArraySerializationType.NESTED, 'chapter', Chapter)
        }

For *Example 3*, you would add the following to your class:

.. code-block::

    @classmethod
    def get_array_property_configuration(cls) -> Dict[str, Tuple[XmlArraySerializationType, str, Any]]:
        return {
            "chapters": (XmlArraySerializationType.FLAT, 'chapter', Chapter)
        }

Further examples are available in our unit tests.