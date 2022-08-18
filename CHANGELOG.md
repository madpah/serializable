# Changelog

<!--next-version-placeholder-->

## v0.1.7 (2022-08-15)
### Fix
* Support for Objects that when represented in XML may just be simple elements with attributes ([`1369d7d`](https://github.com/madpah/serializable/commit/1369d7d755d9e50273b72e2fdd7d2967442e5bde))

## v0.1.6 (2022-08-15)
### Fix
* Temporarilty add `Any` as part of `AnySerializable` type ([`d3e9beb`](https://github.com/madpah/serializable/commit/d3e9bebd7b8dc78d4eb36447ad0b1ee46e2745e0))

## v0.1.5 (2022-08-13)
### Fix
* Direct support for Python `Enum` ([`50148cc`](https://github.com/madpah/serializable/commit/50148cc98a26e4e51479b491acb58451ea5b42b6))

## v0.1.4 (2022-08-13)
### Fix
* Added missing `py.typed` marker ([`ee3169f`](https://github.com/madpah/serializable/commit/ee3169f466353a88922174b40f5b29cb98998be9))

## v0.1.3 (2022-08-12)
### Fix
* Added helpers for serializing XML dates and times (xsd:date, xsd:datetime) ([`c309834`](https://github.com/madpah/serializable/commit/c3098346abf445876d99ecb768d7a4a08b12a291))

## v0.1.2 (2022-08-12)
### Fix
* Support for properties whose value is an `Type[SerializableObject]` but are not `List` or `Set` ([`bf6773c`](https://github.com/madpah/serializable/commit/bf6773c40f3f45dbe2821fdbe785b369f0b3b71c))

## v0.1.1 (2022-08-11)
### Fix
* Handle nested objects that are not list or set ([`4bc5252`](https://github.com/madpah/serializable/commit/4bc525258d0ee655beabace18e41323b4b67ae1b))

## v0.1.0 (2022-08-10)
### Feature
* First alpha release ([`c95a772`](https://github.com/madpah/serializable/commit/c95a7724186b6e45554624b5238c719d172ffc9f))
* First working draft of library for (de-)serialization to/from JSON and XML ([`7af4f9c`](https://github.com/madpah/serializable/commit/7af4f9c4a100f1ce10502ecef228f42ea61e9c22))

