import unicodedata
from codecs import IncrementalDecoder
from re import findall
from typing import Optional, Tuple, Union, List, Set
import importlib
from _multibytecodec import MultibyteIncrementalDecoder  # type: ignore

from encodings.aliases import aliases
from functools import lru_cache

from charset_normalizer.constant import UNICODE_RANGES_COMBINED, UNICODE_SECONDARY_RANGE_KEYWORD, \
    RE_POSSIBLE_ENCODING_INDICATION, ENCODING_MARKS, UTF8_MAXIMAL_ALLOCATION, IANA_SUPPORTED_SIMILAR


@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_accentuated(character: str) -> bool:
    try:
        description = unicodedata.name(character)  # type: str
    except ValueError:
        return False
    return "WITH GRAVE" in description or "WITH ACUTE" in description or "WITH CEDILLA" in description


@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def remove_accent(character: str) -> str:
    decomposed = unicodedata.decomposition(character)  # type: str
    if not decomposed:
        return character

    codes = decomposed.split(" ")  # type: List[str]

    return chr(
        int(
            codes[0],
            16
        )
    )


@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def unicode_range(character: str) -> Optional[str]:
    """
    Retrieve the Unicode range official name from a single character.
    """
    character_ord = ord(character)  # type: int

    for range_name, ord_range in UNICODE_RANGES_COMBINED.items():
        if character_ord in ord_range:
            return range_name

    return None


@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_latin(character: str) -> bool:
    try:
        description = unicodedata.name(character)  # type: str
    except ValueError:
        return False
    return "LATIN" in description


@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_punctuation(character: str) -> bool:
    character_category = unicodedata.category(character)  # type: str

    if "P" in character_category:
        return True

    character_range = unicode_range(character)  # type: Optional[str]

    if character_range is None:
        return False

    return "Punctuation" in character_range


@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_symbol(character: str) -> bool:
    character_category = unicodedata.category(character)  # type: str

    if "S" in character_category or "N" in character_category:
        return True

    character_range = unicode_range(character)  # type: Optional[str]

    if character_range is None:
        return False

    return "Forms" in character_range


@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_separator(character: str) -> bool:
    if character.isspace() or character in ["｜", "+"]:
        return True

    character_category = unicodedata.category(character)  # type: str

    return "Z" in character_category


def is_private_use_only(character: str) -> bool:
    character_category = unicodedata.category(character)  # type: str

    return "Co" == character_category


def is_cjk(character: str) -> bool:
    try:
        character_name = unicodedata.name(character)
    except ValueError:
        return False

    return "CJK" in character_name


@lru_cache(maxsize=len(UNICODE_RANGES_COMBINED))
def is_unicode_range_secondary(range_name: str) -> bool:
    for keyword in UNICODE_SECONDARY_RANGE_KEYWORD:
        if keyword in range_name:
            return True

    return False


def any_specified_encoding(sequence: bytes, search_zone: int = 4096) -> Optional[str]:
    """
    Extract using ASCII-only decoder any specified encoding in the first n-bytes.
    """
    if not isinstance(sequence, bytes):
        raise TypeError

    seq_len = len(sequence)  # type: int

    results = findall(
        RE_POSSIBLE_ENCODING_INDICATION,
        sequence[:seq_len if seq_len <= search_zone else search_zone].decode('ascii', errors='ignore')
    )  # type: List[str]

    if len(results) == 0:
        return None

    for specified_encoding in results:
        specified_encoding = specified_encoding.lower().replace('-', '_')

        for encoding_alias, encoding_iana in aliases.items():
            if encoding_alias == specified_encoding:
                return encoding_iana
            if encoding_iana == specified_encoding:
                return encoding_iana

    return None


@lru_cache(maxsize=128)
def is_multi_byte_encoding(name: str) -> bool:
    """
    Verify is a specific encoding is a multi byte one based on it IANA name
    """
    return name in {"utf_8", "utf_8_sig", "utf_16", "utf_16_be", "utf_16_le", "utf_32", "utf_32_le", "utf_32_be", "utf_7"} or issubclass(
        importlib.import_module('encodings.{}'.format(name)).IncrementalDecoder,  # type: ignore
        MultibyteIncrementalDecoder
    )


def identify_sig_or_bom(sequence: bytes) -> Tuple[Optional[str], bytes]:
    """
    Identify and extract SIG/BOM in given sequence.
    """

    for iana_encoding in ENCODING_MARKS:
        marks = ENCODING_MARKS[iana_encoding]  # type: Union[bytes, List[bytes]]

        if isinstance(marks, bytes):
            marks = [marks]

        for mark in marks:
            if sequence.startswith(mark):
                return iana_encoding, mark

    return None, b""


def should_strip_sig_or_bom(iana_encoding: str) -> bool:
    return iana_encoding not in {"utf_16", "utf_32"}


def iana_name(cp_name: str, strict: bool = True) -> str:
    cp_name = cp_name.lower().replace('-', '_')

    for encoding_alias, encoding_iana in aliases.items():
        if cp_name == encoding_alias or cp_name == encoding_iana:
            return encoding_iana

    if strict:
        raise ValueError("Unable to retrieve IANA for '{}'".format(cp_name))

    return cp_name


def range_scan(decoded_sequence: str) -> List[str]:
    ranges = set()  # type: Set[str]

    for character in decoded_sequence:
        character_range = unicode_range(character)  # type: Optional[str]

        if character_range is None:
            continue

        ranges.add(
            character_range
        )

    return list(ranges)


def cp_similarity(iana_name_a: str, iana_name_b: str) -> float:

    if is_multi_byte_encoding(iana_name_a) or is_multi_byte_encoding(iana_name_b):
        return 0.

    decoder_a = importlib.import_module('encodings.{}'.format(iana_name_a)).IncrementalDecoder  # type: ignore
    decoder_b = importlib.import_module('encodings.{}'.format(iana_name_b)).IncrementalDecoder  # type: ignore

    id_a = decoder_a(errors="ignore")  # type: IncrementalDecoder
    id_b = decoder_b(errors="ignore")  # type: IncrementalDecoder

    character_match_count = 0  # type: int

    for i in range(0, 255):
        to_be_decoded = bytes([i])  # type: bytes
        if id_a.decode(to_be_decoded) == id_b.decode(to_be_decoded):
            character_match_count += 1

    return character_match_count / 254


def is_cp_similar(iana_name_a: str, iana_name_b: str) -> bool:
    """
    Determine if two code page are at least 80% similar. IANA_SUPPORTED_SIMILAR dict was generated using
    the function cp_similarity.
    """
    return iana_name_a in IANA_SUPPORTED_SIMILAR and iana_name_b in IANA_SUPPORTED_SIMILAR[iana_name_a]
