from requests import Session

from google_ngram_downloader.util import (
    get_indices,
    ngram_to_cooc,
    count_coccurrence,
)
from google_ngram_downloader.__main__ import download

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
    ('verbose', 'err_len'),
    (
        (False, 1),
        (True, 725),
    ),
)
def test_download(capsys, tmpdir, monkeypatch, verbose, err_len):
    urls = []

    def mocked_get(self, url, **kwargs):
        urls.append(url)

        class FakeRequest:

            def iter_content(self, buffer):
                yield b'some data'

        return FakeRequest()

    monkeypatch.setattr(Session, 'get', mocked_get)

    download.command(
        '-o {tmpdir} -n 2 {verbose}'
        ''.format(
            tmpdir=tmpdir,
            verbose='-v' if verbose else '',
        ).split()
    )

    assert len(urls) == len(tmpdir.listdir()) == 724

    out, err = capsys.readouterr()
    assert not out
    assert len(err.split('\n')) == err_len


@pytest.mark.parametrize(
    ('ngram', 'result'),
    (
        (
            'aa_SOME_GARBAGE ab BB zz yz',
            (
                (('BB', 'aa'), 3),
                (('BB', 'ab'), 3),
                (('BB', 'zz'), 3),
                (('BB', 'yz'), 3),
            ),
        ),
    ),
)
def test_ngrams_to_cooc(ngram, result):
    assert ngram_to_cooc(ngram, 3, 2) == result


def test_count_coccurrence(records):
    assert count_coccurrence(records, 1) == {
        ('BB', 'a'): 1110,
        ('BB', 'z'): 1110,
        ('ABCDEFG', 'a'): 222,
        ('ABCDEFG', 'z'): 222,
    }
