"""An extractor of boolean trigram queries from a regex, such that a superset
of the docs matching the regex are returned. You can then run the actual regex
over just the returned docs, saving a lot of computation and IO.

Junghoo Ch and Sridhar Rajagopalan, in "A fast regular expression indexing
engine", descibe an intuitive method for accelerating regex searching with a
trigram index. Russ Cox, in http://swtch.com/~rsc/regexp/regexp4.html, refines
that to {(1) extract use from runs of less than 3 static chars and (2) extract
trigrams that cross the boundaries between subexpressions} by keeping track of
prefix and suffix information while chewing through a pattern and effectively
merging adjacent subpatterns. This is an implementation of his method.

"""
from parsimonious import Grammar


class TrigramQuery(object):
    """A query which matches a superset of the docs its corresponding regex
    does. Abstract.

    """
    def __init__(self, trigrams, subassertions):
        """I am a logical AND or OR of trigrams and subassertions.

        These are divided just for implementation ease.

        :arg trigrams: A list of trigram strings
        :arg subassertions: A list of Assertions

        """
        self.trigrams = trigrams
        self.subassertions = subassertions


class And(TrigramQuery):
    pass


class Or(TrigramQuery):
    pass


# class None?
# class Any?


class RegexSummary(object):
    """The digested result of analyzing a parsed regex

    :attr can_match_empty: Whether the regex can match the empty string
    :attr exacts: Set of exact strings which, unioned, exhaust the regex. For
        example (s?printf) would yield {sprintf, printf}.
    :attr prefixes: The set of prefixes of strings the regex can match
    :attr suffixes: The set of suffixes of strings the regex can match
    :attr query: An TrigramQuery that must be satisfied by any matching
        string, in addition to the restrictions expressed by the other
        attributes

    Prefixes, suffixes, and the rest are used only as intermediate values. The
    point is for them ultimately to become part of the query, which is itself a
    boolean combination of trigrams.

    """
    def __init__(self, regex):
        """Dispatch on the opcode of regex, and descend recursively, analyzing
        lower nodes and then pulling back up to finally summarize the whole.

        :arg regex: A parsed regex, as returned by ``sre_parse.parse()``

        """
        self.can_match_empty = can_match_empty
        self.exacts = exacts
        self.prefix = prefix  # This can probably be an actual set. The Go impl blows a lot of code removing dupes and such.
        self.suffix = suffix
        self.query = query
        
        # NEXT: Start by using this framework to implement the FREE method. I think it'll fit. Test that. Then go full-on GCS.


def trigrams(s):
    """Return an iterable of all trigrams contained in a string."""
    # Optimization: return indices rather than actual substrings to save
    # instantiation cost.
    return (s[i:i + 3] for i in xrange(0, len(s) - 2))


def summarize_regex(regex):
    """Return a RegexSummary of a regex.

    :arg regex: A string containing a regex pattern

    """


def trigram_query(regex):
    """Return an iterable of trigrams that will be found in any text matching
    the given regex.

    :arg regex: A string containing a regex pattern

    """
    # TODO: Veto patterns which are easy DOSes.

    # I suspect simplify(force=True) mashes everything down into `match` in
    # preparation for actually running `match` against a corpus.

    summary = RegexSummary(regex)
    summary.simplify(force=True)
    summary.add_exact()
    return summary.query


def trigrammify_tree(tree):
    """Explode the strings in a tree into trigrams. Return a tree whose leaves are trigrams and whose inner nodes are boolean operations. This can then be trivially turned into an ES query."""
    # Remember that Lucene regexes are always anchored. The caller will have to add a leading .*, etc.
    # Raise an exception somewhere, maybe in simplify_tree, if there are no trigrams.


def simplify_tree(tree):
    """Do the node reduction to collapse branches of a string tree that aren't
    useful. Remove strings that aren't long enough to generate any trigrams."""


def build_tree(regex):
    """Turn a parsed regex into a tree of ANDed and ORed literal strings."""
    op, param = regex
    if op == 'branch':
        mystery, alternatives = param
        return or_(string_tree(alternatives))
    elif op == 'literal':
        return param


# We should parse a regex. Then go over the tree and turn things like c+ into cc*, perhaps, as it makes it easier to see trigrams to extract.
# TODO: Parse normal regex syntax, but spit out Lucene-compatible syntax, with " escaped. And all special chars escaped even in character classes, in accordance with https://lucene.apache.org/core/4_6_0/core/org/apache/lucene/util/automaton/RegExp.html?is-external=true.
# one|two?|three?

# This recognizes a subset of Python's regex language, minus lookaround
# assertions, non-greedy quantifiers, and named and other special sorts of
# groups. Lucene doesn't support those, though we might be able to fake it
# later via some transformation.
regex_grammar = Grammar(r"""
    regexp = branch another_branch*
    branch = piece*
    another_branch = "|" branch
    piece = quantified / atom
    quantified = atom quantifier
    quantifier = "*" / "+" / "?" / repeat
    repeat = "{" number ("," number?)? "}"
    number = ~r"\d+"

    # By making each parenthesized subexpr just a "regexp", visit_regexp can
    # assign group numbers, starting from 0, and the top-level expression
    # conveniently ends up in the conventional group 0.
    atom = ("(" regexp ")") / class / "^" / "$" / "." / char  # Optimize: vacuum up any harmless sequence of chars in one regex, first: [^()[\]^$.?*+{}]+

    # Character classes are pretty complex little beasts, even though we're
    # just scanning right over them rather than trying to pull any info out:
    class = "[" (inverted_class_start / positive_class_start) initial_class_char class_char* "]"
    inverted_class_start = "^"
    positive_class_start = !"^"
    # An unescaped ] is treated as a literal when the first char of a positive
    # or inverted character class:
    initial_class_char = "]" / class_char
    class_char = backslash_escaped / ~r"[^\]]"

    #~r"\[\]?(?:[^\\\]]*(?:\\\]|\\)*)*\]"  # Grr, still matches []. #~r"\[\]?(?:[^\\\]]*(?:\\\]|\\))*\]"
    char = backslash_escaped / literal_char
    literal_char = ~r"[^^$?*+()[\]{}|.\\]"  # TODO: Exclude (^$+*?)[ and ]{} (even though these latter ones are tolerated unescaped by Python's re parser).
    backslash_escaped = ~r"\\."
    """)
