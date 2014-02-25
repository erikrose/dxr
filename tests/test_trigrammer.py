# -*- coding: utf-8 -*-
"""Tests for the regex trigram extractor"""

from dxr.trigrammer import trigrams

from nose.tools import eq_


def test_trigrams():
    eq_(list(trigrams('')), [])
    eq_(list(trigrams('a')), [])
    eq_(list(trigrams('ab')), [])
    eq_(list(trigrams('abc')), ['abc'])
    eq_(list(trigrams('abcde')), ['abc', 'bcd', 'cde'])


#def test_something():
#    eq_(trigrams_from_regex('abc'), ['abc'])

# Make sure we don't have have both "ab" and "abc" both as possible prefixes. This is equivalent to just "ab".

# prefixes: abc | cba
# suffixes: def
# exact: abcdef | cbadef
#
# prefixes: ab abcd abef
#              abcd abef
# suffixes: ef cdef abef
#              cdef abef
# exact: Ø
