# Changelog

<!--next-version-placeholder-->

## v0.16.0 (2023-11-29)

### Feature

* More controll over XML attribute serialization ([#34](https://github.com/madpah/serializable/issues/34)) ([`38f42d6`](https://github.com/madpah/serializable/commit/38f42d64e556a85206faa50459a9ce3e889bd3ae))

## v0.15.0 (2023-10-10)

### Feature

* Allow custom (de)normalization ([#32](https://github.com/madpah/serializable/issues/32)) ([`aeecd6b`](https://github.com/madpah/serializable/commit/aeecd6b2e8c4e8febc84ebfa24fe7ec96fd9cb10))

## v0.14.1 (2023-10-08)

### Fix

* JSON deserialize `Decimal` ([#31](https://github.com/madpah/serializable/issues/31)) ([`b6dc66a`](https://github.com/madpah/serializable/commit/b6dc66acfb7fdc82b3dd18caf4ad79ec0e87eef0))

## v0.14.0 (2023-10-06)

### Feature

* Enhanced typehints and typing ([#27](https://github.com/madpah/serializable/issues/27)) ([`410372a`](https://github.com/madpah/serializable/commit/410372a0fa2713c5a36d790f08d2d4b52a6a187c))

## v0.13.1 (2023-10-06)

### Fix

* Protect default value for `serialization_types` from unintended downstream modifications ([#30](https://github.com/madpah/serializable/issues/30)) ([`0e814f5`](https://github.com/madpah/serializable/commit/0e814f5248176e02a7f96480e54320dde781f8b2))

### Documentation

* Add examples to docs ([#28](https://github.com/madpah/serializable/issues/28)) ([`4eddb24`](https://github.com/madpah/serializable/commit/4eddb242e51194694474748acdecd38b317b791e))
* Remove unnecessary type-ignores ([`26c561d`](https://github.com/madpah/serializable/commit/26c561dc0bf9f5755899a8fa0d0a37aba6275074))
* Remove unnecessary type-ignores ([`11b5896`](https://github.com/madpah/serializable/commit/11b5896057fd61838804ea5b52dc3bd0810f6c88))

## v0.13.0 (2023-10-01)

### Feature

* Format specific (de)serialize ([#25](https://github.com/madpah/serializable/issues/25)) ([`dc998df`](https://github.com/madpah/serializable/commit/dc998df37a2ba37fa43d10c8a1ce044a5b9f5b1e))

## v0.12.1 (2023-10-01)

### Fix

* Xml defaultNamespace serialization and detection ([#20](https://github.com/madpah/serializable/issues/20)) ([`59eaa5f`](https://github.com/madpah/serializable/commit/59eaa5f28eb2969e9d497669ef0436eb87b7525d))

### Documentation

* Render only public API ([#19](https://github.com/madpah/serializable/issues/19)) ([`fcc5d8e`](https://github.com/madpah/serializable/commit/fcc5d8e6c49e8b8c199cb55f855d09e4259a075a))
* Set codeblock language and caption ([#15](https://github.com/madpah/serializable/issues/15)) ([`5d5cf7b`](https://github.com/madpah/serializable/commit/5d5cf7bc29ed70f4024c714b2326012a9db54cea))

## v0.12.0 (2023-03-07)
### Feature
* Bump dev dependencies to latest (including `mypy` fixes) ([`06dcaa2`](https://github.com/madpah/serializable/commit/06dcaa28bfebb4505ddc67b287dc6f416822ffb6))
* Bump dev dependencies to latest (including `mypy` fixes) ([`6d70287`](https://github.com/madpah/serializable/commit/6d70287640c411d33823e9188b0baa81fba80c24))

## v0.11.1 (2023-03-03)
### Fix
* Use `defusedxml` whenever we load XML to prevent XEE attacks ([`ae3d76c`](https://github.com/madpah/serializable/commit/ae3d76c31ab8af81d20acaaba45fd4bb9aad9305))
* Use `defusedxml` whenever we load XML to prevent XEE attacks ([`32fd5a6`](https://github.com/madpah/serializable/commit/32fd5a698b41b489b4643bcbe795e24a1e0db423))
* Use `defusedxml` whenever we load XML to prevent XEE attacks ([`72e0127`](https://github.com/madpah/serializable/commit/72e01279274246313170e5e7c9d32afec16edf7c))
* Use `defusedxml` whenever we load XML to prevent XEE attacks ([`de61deb`](https://github.com/madpah/serializable/commit/de61deb5c2447a656ca6a111194b2b0ceeab9278))
* Use `defusedxml` whenever we load XML to prevent XEE attacks ([`de26dc3`](https://github.com/madpah/serializable/commit/de26dc3d0eaab533dac9b1db40f0add56dd67754))

## v0.11.0 (2023-03-03)
### Feature
* Disabled handling to avoid class attributes that clash with `keywords` and `builtins` ([`4439227`](https://github.com/madpah/serializable/commit/44392274628ddec4aaaeae89a8387d435e3cf002))

## v0.10.1 (2023-03-02)
### Fix
* Handle empty XML elements during deserialization ([`f806f35`](https://github.com/madpah/serializable/commit/f806f3521f0afd8978f94f5ec355f47d9a538b91))

## 0.10.0 (2023-02-21)
### Feature
* Ability for custom `type_mapping` to take lower priority than `xml_array` ([`fc0bb22`](https://github.com/madpah/serializable/commit/fc0bb22f395498be42394af5f70addb9f63f0b3a))
* Handle `ForwardRef` types ([`a66e700`](https://github.com/madpah/serializable/commit/a66e700eeb5a80447522b8112ecdeff0345f0608))

## v0.9.3 (2023-01-27)
### Fix
* Deserializing JSON with custom JSON name was incorrect ([`7d4aefc`](https://github.com/madpah/serializable/commit/7d4aefc98dfe39ae614227601369e9fd25c12faa))

## v0.9.2 (2023-01-27)
### Fix
* Nested array of Enum values in `from_json()` failed ([`ea4d76a`](https://github.com/madpah/serializable/commit/ea4d76a64c8c97f7cb0b16687f300c362dfe7623))
* Output better errors when deserializing JSON and we hit errors ([`1699c5b`](https://github.com/madpah/serializable/commit/1699c5b96bb6a8d4f034b29a6fe0521e3d650d53))

## v0.9.1 (2023-01-26)
### Fix
* Nested array of Enum values in `from_xml()` failed ([`393a425`](https://github.com/madpah/serializable/commit/393a4256abb69228a9e6c2fc76b508e370a39d93))

## v0.9.0 (2023-01-24)
### Feature
* Bring library to BETA state ([`c6c36d9`](https://github.com/madpah/serializable/commit/c6c36d911ae401af477bcc98633f10a87140d0a4))

## v0.8.2 (2023-01-23)
### Fix
* Typing for `@serializable.view` was incorrect ([`756032b`](https://github.com/madpah/serializable/commit/756032b543a2fedac1bb61f57796eea438c0f9a7))
* Typing for `@serializable.serializable_enum` decorator was incorrect ([`84e7826`](https://github.com/madpah/serializable/commit/84e78262276833f507d4e8a1ce11d4a82733f395))

## v0.8.1 (2023-01-23)
### Fix
* Specific None value per View - support for XML was missing ([`5742861`](https://github.com/madpah/serializable/commit/5742861728d1b371bc0a819fed0b12e9da5829e1))

## v0.8.0 (2023-01-20)
### Feature
* Support for specific None values for Properties by View ([`a80ee35`](https://github.com/madpah/serializable/commit/a80ee3551c5e23f9c0491f48c3f98022317ddd99))

### Fix
* Minor typing and styling ([`b728c4c`](https://github.com/madpah/serializable/commit/b728c4c995076cd18317c878c6f5900c6b266425))
* Minor typing and styling ([`b2ebcfb`](https://github.com/madpah/serializable/commit/b2ebcfb53cd640eb70a51a9f637db24e0d7b367e))

## v0.7.3 (2022-09-22)
### Fix
* None value for JSON is now `None` (`null`) ([`8b7f973`](https://github.com/madpah/serializable/commit/8b7f973cd96c861c4490c50553c880e88ebf33dc))

## v0.7.2 (2022-09-22)
### Fix
* Missing namespace for empty XML elements ([`f3659ab`](https://github.com/madpah/serializable/commit/f3659ab9ea651dcd65168aa22fa838d35ee189d5))

## v0.7.1 (2022-09-15)
### Fix
* Support forced inclusion of array properties by using `@serializable.include_none` ([`7ad0ecf`](https://github.com/madpah/serializable/commit/7ad0ecf08c5f56de4584f4f081bfc0f667d2f477))
* Support for deserializing to objects from a primitive value ([`12f9f97`](https://github.com/madpah/serializable/commit/12f9f9711a5fd924898a0afb50a24c8d360ab3ff))

## v0.7.0 (2022-09-14)
### Feature
* Support for including `None` values, restricted to certain Views as required ([`614068a`](https://github.com/madpah/serializable/commit/614068a4955f99d8fce5da341a1fd74a6772b775))

## v0.6.0 (2022-09-14)
### Feature
* Implement views for serialization to JSON and XML ([`db57ef1`](https://github.com/madpah/serializable/commit/db57ef13fa89cc47db074bd9be4b48232842df07))

### Fix
* Support for `Decimal` in JSON serialization ([`cc2c20f`](https://github.com/madpah/serializable/commit/cc2c20fe8bce46e4854cb0eecc6702459cd2f99a))
* Better serialization to JSON ([`e8b37f2`](https://github.com/madpah/serializable/commit/e8b37f2ee4246794c6c0e295bcdf32cd58d5e52d))

## v0.5.0 (2022-09-12)
### Feature
* Support for string formatting of values ([`99b8f3e`](https://github.com/madpah/serializable/commit/99b8f3e7ab84f087a87b330928fc598c96a0e682))
* Support string formatting for values ([`3fefe22`](https://github.com/madpah/serializable/commit/3fefe2294130b80f05e219bd655514a0956f7f93))
* Support for custom Enum implementations ([`c3622fc`](https://github.com/madpah/serializable/commit/c3622fcb0019de794b1cbd3ad6333b6044d8392a))

## v0.4.0 (2022-09-06)
### Feature
* Add support for defining XML element ordering with `@serializable.xml_sequence()` decorator ([`c1442ae`](https://github.com/madpah/serializable/commit/c1442aeb1776243922fbaa6b5174db5a54f71920))

### Fix
* Removed unused dependencies ([`448a3c9`](https://github.com/madpah/serializable/commit/448a3c9f0de897cf1ee6d7c46af377c2f389730d))
* Handle python builtins and keywords during `as_xml()` for element names ([`3bbfb1b`](https://github.com/madpah/serializable/commit/3bbfb1b4a7808f4cedd3b2b15f31aaaf8e35d60a))
* Handle python builtins and keywords during `as_xml()` for attributes ([`8d6a96b`](https://github.com/madpah/serializable/commit/8d6a96b0850d4993c96cbc7d532d848ba9c5e8b3))

## v0.3.9 (2022-08-24)
### Fix
* Support declaration of XML NS in `as_xml()` call ([`19b2b70`](https://github.com/madpah/serializable/commit/19b2b7048fdd7048d62f618987c13f2d3a457726))

## v0.3.8 (2022-08-24)
### Fix
* Deserialization of XML boolean values ([`799d477`](https://github.com/madpah/serializable/commit/799d4773d858fdf8597bef905302a373ca150db8))

## v0.3.7 (2022-08-23)
### Fix
* Fixed deferred parsing for Properties ([`833e29b`](https://github.com/madpah/serializable/commit/833e29b8391c85931b12c98f87a2faf3a68d388e))

## v0.3.6 (2022-08-23)
### Fix
* Support for cyclic dependencies ([`911626c`](https://github.com/madpah/serializable/commit/911626c88fb260049fdf2931f6ea1b0b05d7166a))

## v0.3.5 (2022-08-22)
### Fix
* Support for non-primitive types when XmlSerializationType == FLAT ([`7eff15b`](https://github.com/madpah/serializable/commit/7eff15bbb8d20760418071c005d65d2623b44eab))

## v0.3.4 (2022-08-22)
### Fix
* Support ENUM in XML Attributes ([`f2f0922`](https://github.com/madpah/serializable/commit/f2f0922f2d0280185f6fc7f96408d6647588c8d2))

## v0.3.3 (2022-08-19)
### Fix
* Handle Array types where the concrete type is quoted in its definition ([`b6db879`](https://github.com/madpah/serializable/commit/b6db879d72822ada74a41362594b009f09349da9))

## v0.3.2 (2022-08-19)
### Fix
* Work to support `sortedcontainers` as a return type for Properties ([`805a3f7`](https://github.com/madpah/serializable/commit/805a3f7a10e41f63b132ac0bb234497d5d39fe2b))

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

