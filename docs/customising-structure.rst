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

You can directly control mapping of property names for properties in a Class by adding the decorators
:func:`serializable.json_name()` or :func:`serializable.xml_name()`.

For example, you might have a property called **isbn** in your class, but when serialized to JSON it should be called
**isbn_number**.

To implement this mapping, you would alter your class as follows adding the :func:`serializable.json_name()`
decorator to the **isbn** property:

.. code-block:: python

    @serializable.serializable_class
    class Book:

        def __init__(self, title: str, isbn: str, publish_date: date, authors: Iterable[str],
            ...

        @property
        @serializable.json_name('isbn_number')
        def isbn(self) -> str:
            return self._isbn

Excluding Property from Serialization
----------------------------------------------------

Properties can be ignored during deserialization by including them in the :func:`serializable.serializable_class()`
annotation as per the following example.

A typical use case for this might be where a JSON schema is referenced, but this is not part of the constructor for the
class you are deserializing to.

.. code-block:: python

    @serializable.serializable_class(ignore_during_deserialization=['$schema'])
    class Book:
      ...


Handling ``None`` Values
----------------------------------------------------

By default, ``None`` values will lead to a Property being excluded from the serialization process to keep the output
as concise as possible. There are many cases (and schemas) where this is however not the required behaviour.

You can force a Property to be serialized even when the value is ``None`` by annotating as follows:

.. code-block:: python

    @serializable.include_none
    def email(self) -> Optional[str]:
        return self._email


Customised Property Serialization
----------------------------------------------------

This feature allows you to handle, for example, serialization of :class:`datetime.date` Python objects to and from
strings.

Depending on your use case, the string format could vary, and thus this library makes no assumptions. We have provided
an some example helpers for (de-)serializing dates and datetimes.

To define a custom serializer for a property, add the :func:`serializable.type_mapping()` decorator to the property.
For example, to have a property named *created* be use the :class:`serializable.helpers.Iso8601Date` helper you
would add the following method to your class:

.. code-block:: python

    @serializable.serializable_class
    class Book:

        def __init__(self, title: str, isbn: str, publish_date: date, authors: Iterable[str],
            ...

        @property
        @serializable.type_mapping(Iso8601Date)
        def publish_date(self) -> date:
            return self._publish_date

Writing Custom Property Serializers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can write your own custom property serializer. The only requirements are that it must extend
:class:`serializable.helpers.BaseHelper` and therefore implement the ``serialize()`` and ``deserialize()`` class methods.

For examples, see :mod:`serializable.helpers`.


Serializing Lists & Sets
----------------------------------------------------

Particularly in XML, there are many ways that properties which return Lists or Sets could be represented. We can handle
this by adding the decorator :func:`serializable.xml_array()` to the appropriate property in your class.

For example, given a Property that returns ``Set[Chapter]``, this could be serialized in one of a number of ways:


.. code-block:: json
   :caption: Example 1: Nested list under a property name in JSON

    {
        "chapters": [
            { /* chapter 1 here... */ },
            { /* chapter 2 here... */ },
            // etc...
        ]
    }

.. code-block:: xml
   :caption: Example 2: Nested list under a property name in XML

    <chapters>
        <chapter><!-- chapter 1 here... --></chapter>
        <chapter><!-- chapter 2 here... --></chapter>
        <!-- etc... -->
    </chapters>

.. code-block:: xml
   :caption: Example 3: Collapsed list under a (potentially singular of the) property name in XML

    <chapter><!-- chapter 1 here... --></chapter>
    <chapter><!-- chapter 2 here... --></chapter>

.. note:

    Other structures may also be possible, but only the above are considered by this library at the current time.

As we have only identified one possible structure for JSON at this time, the implementation of
only affects XML (de-)serialization at this time.

For *Example 2*, you would add the following to your class:

.. code-block:: python

    @property
    @serializable.xml_array(XmlArraySerializationType.NESTED, 'chapter')
    def chapters(self) -> List[Chapter]:
        return self._chapters

For *Example 3*, you would add the following to your class:

.. code-block:: python

    @property
    @serializable.xml_array(XmlArraySerializationType.FLAT, 'chapter')
    def chapters(self) -> List[Chapter]:
        return self._chapters

Further examples are available in our :ref:`unit tests <unit-tests>`.

Serializing special XML string types
----------------------------------------------------

In XML, are special string types, ech with defined set of allowed characters and whitespace handling.
We can handle this by adding the decorator :obj:`serializable.xml_string()` to the appropriate property in your class.

.. code-block:: python

    @property
    @serializable.xml_string(serializable.XmlStringSerializationType.TOKEN)
    def author(self) -> str:
        return self._author

Further examples are available in our :ref:`unit tests <unit-tests>`.

.. note::

   The actual transformation is done by :func:`serializable.xml.xs_normalizedString()`
   and :func:`serializable.xml.xs_token()`

Serialization Views
----------------------------------------------------

Many object models can be serialized to and from multiple versions of a schema or different schemas. In
``py-serialization`` we refer to these as Views.

By default all Properties will be included in the serialization process, but this can be customised based on the View.

Defining Views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A View is a class that extends :class:`serializable.ViewType` and you should create classes as required in your
implementation.

For example:

.. code-block:: python

   from serializable import ViewType

   class SchemaVersion1(ViewType):
      pass


Property Inclusion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Properties can be annotated with the Views for which they should be included.

For example:

.. code-block:: python

    @property
    @serializable.view(SchemaVersion1)
    def address(self) -> Optional[str]:
        return self._address


Handling ``None`` Values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Further to the above, you can vary the ``None`` value per View as follows:

.. code-block:: python

    @property
    @serializable.include_none(SchemaVersion2)
    @serializable.include_none(SchemaVersion3, "RUBBISH")
    def email(self) -> Optional[str]:
        return self._email

The above example will result in ``None`` when serializing with the View ``SchemaVersion2``, but the value ``RUBBISH``
when serializing to the View ``SchemaVersion3`` when ``email`` is not set.


Serializing For a View
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To serialized for a specific View, include the View when you perform the serialisation.

.. code-block:: python
   :caption: JSON Example

    ThePhoenixProject.as_json(view_=SchemaVersion1)


.. code-block:: python
   :caption: XML Example

    ThePhoenixProject.as_xml(view_=SchemaVersion1)

XML Element Ordering
----------------------------------------------------

Some XML schemas utilise `sequence`_ which requires elements to be in a prescribed order.

You can control the order properties are serialized to elements in XML by utilising the
:func:`serializable.xml_sequence()` decorator. The default sort order applied to properties is 100 (where lower is
earlier in the sequence).

In the example below, the ``isbn`` property will be output first.

.. code-block:: python

    @property
    @serializable.xml_sequence(1)
    def isbn(self) -> str:
        return self._isbn


.. _sequence: https://www.w3.org/TR/xmlschema-0/#element-sequence
