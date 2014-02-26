# -*- coding: utf-8 -*-
"""Tests for the regex trigram extractor"""

from unittest import TestCase

from nose.tools import eq_, assert_raises
from parsimonious.exceptions import ParseError

from dxr.trigrammer import trigrams, regex_grammar


def test_trigrams():
    eq_(list(trigrams('')), [])
    eq_(list(trigrams('a')), [])
    eq_(list(trigrams('ab')), [])
    eq_(list(trigrams('abc')), ['abc'])
    eq_(list(trigrams('abcde')), ['abc', 'bcd', 'cde'])


#def test_something():
#    eq_(trigrams_from_regex('abc'), ['abc'])

# Make sure we don't have have both "ab" and "abc" both as possible prefixes. This is equivalent to just "ab".
# Make sure we do the right thing when the (?i) flag is set: either generate enough trigrams to cover the case insensitivity, or use a case-folder ES index. I guess we'll use a folded trigram index, like we do now. Be sure to have the query analyzer do the ucasing, because Python is not going to get that right for Unicode.
# Make sure we can parse (END||STOP) (empty branches).
# Parse \d, \t, \n, \s, etc. so they don't just come out as "d", etc.: AbBdDsSwWZ afnrtvx.
# class tests: []] [^]] [\d-] [a\]] [()[\]{}] []()[{}]
#  [] [^] should not be a valid class.

# prefixes: abc | cba
# suffixes: def
# exact: abcdef | cbadef
#
# prefixes: ab abcd abef
#              abcd abef
# suffixes: ef cdef abef
#              cdef abef
# exact: Ø


class RegexParserTests(TestCase):
    """Tests for our custom regex parser"""

def test_parse_classes():
    """Make sure we recognize character classes."""

    def parse_class(pattern):
        regex_grammar['class'].parse(pattern)

    def dont_parse_class(pattern):
        assert_raises(ParseError,
                      regex_grammar['class'].parse,
                      pattern)


    # These should match all the way to the end:
    for pattern in ['[]]', '[^]]', '[\d-]', '[a\]]', '[()[\]{}]', '[]()[{}]']:
        yield parse_class, pattern

    # These shouldn't match:
    for pattern in ['[]', '[^]']:
        yield dont_parse_class, pattern
