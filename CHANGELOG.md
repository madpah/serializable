# Changelog

<!--next-version-placeholder-->

## v0.3.1 (2022-08-19)
### Fix
* Better support for Properties that have a Class type that is not a Serializable Class (e.g. UUID) ([`95d407b`](https://github.com/madpah/serializable/commit/95d407b4456d8f106cf54ceb650cbde1aab69457))

## v0.3.0 (2022-08-19)
### Feature
* Support ignoring elements/properties during deserialization ([`6319d1f`](https://github.com/madpah/serializable/commit/6319d1f9e632a941b1d79a63083c1ecb194105be))

## v0.2.3 (2022-08-19)
### Fix
* Update `helpers` to be properly typed ([`d924dc2`](https://github.com/madpah/serializable/commit/d924dc2d3b5f02c61ff6ac36fa10fa6adaac7022))

## v0.2.2 (2022-08-19)
### Fix
* Change to helpers to address typing issues ([`1c32ba1`](https://github.com/madpah/serializable/commit/1c32ba143504a605a77df4908422a95d0bd07edf))
* Remove `/` from method signature so we work on Python < 3.8 ([`c45864c`](https://github.com/madpah/serializable/commit/c45864cd6c90ed38d8cedd944adcfe43b32326b2))

## v0.2.1 (2022-08-18)
### Fix
* Update to work on python < 3.10 ([`91df8cb`](https://github.com/madpah/serializable/commit/91df8cbb718db15ea182888aa796db32b8015004))

## v0.2.0 (2022-08-18)
### Feature
* Library re-write to utilise decorators ([`957fca7`](https://github.com/madpah/serializable/commit/957fca757d89dc1b8ef9b13357a5a9380dbe94ff))

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

