from google_ngram_downloader.util import (
    get_indices,
    ngram_to_cooc,
    count_coccurrence,
)

import pytest


def test_get_indices_1grams(unigram_indices):
    indices = list(get_indices(1))
    assert len(set(indices)) == len(indices)

    assert set(indices) == unigram_indices


def test_get_indices_manygrams(bigrams_indices):
    indices = list(get_indices(2))
    assert len(set(indices)) == len(indices)

    assert set(indices) == bigrams_indices


@pytest.mark.parametrize(
    ('ngram', 'expected_result', 'index'),
    (
        (
            b'aa_SOME_GARBAGE ab BB zz yz',
            (
                ((0, 1), 3),
                ((0, 2), 3),
                ((0, 3), 3),
                ((0, 4), 3),
            ),
            {'BB': 0, 'aa': 1, 'ab': 2, 'zz': 3, 'yz': 4},
        ),
        (
            b'aa yz BB yz yz',
            (
                ((0, 1), 3),
                ((0, 2), 3),
                ((0, 2), 3),
                ((0, 2), 3),
            ),
            {'BB': 0, 'aa': 1},
        ),
    ),
)
def test_ngrams_to_cooc(ngram, expected_result, index):
    result = ngram_to_cooc(ngram, 3, index)
    assert result == expected_result


def test_count_coccurrence(records):
    index = {}
    assert count_coccurrence(records, index) == {
        (index['BB'], index['a']): 1110,
        (index['BB'], index['z']): 1110,
        (index['ABCDEFG'], index['a']): 222,
        (index['ABCDEFG'], index['z']): 222,
    }
