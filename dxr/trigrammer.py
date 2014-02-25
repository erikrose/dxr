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
import sre_parse


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


def ands_and_ors(regex):
    