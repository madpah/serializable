from io import StringIO
from typing import Optional
from unittest import TestCase

import py_serializable as serializable


@serializable.serializable_class
class RawText:
    def __init__(self, value: Optional[str] = None) -> None:
        self._value = value

    @property
    @serializable.xml_name('.')
    def value(self) -> Optional[str]:
        return self._value


@serializable.serializable_class
class NormalizedText:
    def __init__(self, value: Optional[str] = None) -> None:
        self._value = value

    @property
    @serializable.xml_name('.')
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def value(self) -> Optional[str]:
        return self._value


@serializable.serializable_class
class TokenText:
    def __init__(self, value: Optional[str] = None) -> None:
        self._value = value

    @property
    @serializable.xml_name('.')
    @serializable.xml_string(serializable.XmlStringSerializationType.TOKEN)
    def value(self) -> Optional[str]:
        return self._value


class TestTextWhitespace(TestCase):
    def test_raw_spaces(self) -> None:
        self.assertEqual(RawText.from_xml(StringIO('<RawText>  hello  </RawText>')).value, '  hello  ')

    def test_normalized_spaces(self) -> None:
        result = NormalizedText.from_xml(StringIO('<NormalizedText>  hello  </NormalizedText>'))
        self.assertEqual(result.value, '  hello  ')

    def test_normalized_whitespace_only(self) -> None:
        self.assertEqual(NormalizedText.from_xml(StringIO('<NormalizedText>   </NormalizedText>')).value, '   ')

    def test_normalized_tab_control(self) -> None:
        self.assertEqual(NormalizedText.from_xml(StringIO('<NormalizedText>a&#9;b</NormalizedText>')).value, 'a b')

    def test_token_control(self) -> None:
        self.assertEqual(TokenText.from_xml(StringIO('<TokenText>  hello   world  </TokenText>')).value, 'hello world')

    def test_plain_control(self) -> None:
        self.assertEqual(RawText.from_xml(StringIO('<RawText>hello</RawText>')).value, 'hello')
