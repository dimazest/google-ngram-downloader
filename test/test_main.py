import gzip
import zlib
from itertools import chain
from contextlib import contextmanager

from requests import Session

from google_ngram_downloader.__main__ import download, cooccurrence
from google_ngram_downloader import util

import pytest


@pytest.fixture
def compressobj():
    return zlib.compressobj()


@pytest.fixture
def urls():
    return []


@pytest.fixture
def data():
    return (
        b'analysis is often described as\t1991\t1\t1\n',
        b'analysis', b' is often described as\t1992\t2\t1\n',
        b'analysis', b' is often', b' described as\t1993\t3\t1\n',
        b'c1 c2 WORD c3 c4\t1987\t100\t2\n'
    )


@pytest.fixture
def compressed_data(compressobj, data):
    return tuple(map(compressobj.compress, data)) + (compressobj.flush(), )


@pytest.fixture(autouse=True)
def fake_request(urls, compressed_data, monkeypatch):
    def mocked_get(self, url, **kwargs):
        urls.append(url)

        class FakeRequest:
            def iter_content(self, chunk_size):
                return iter(compressed_data)

            status_code = 200

        return FakeRequest()

    monkeypatch.setattr(Session, 'get', mocked_get)


@pytest.mark.parametrize(
    ('verbose', 'err_len'),
    (
        (False, 1),
        (True, 725),
    ),
)
def test_download(capsys, tmpdir, verbose, err_len, urls):
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


def test_cooccurrence(tmpdir, monkeypatch):
    objects = []

    def modked_open(obj, *args, **kwargs):
        @contextmanager
        def _open(*args, **kwargs):
            class MockedGzipFile(object):
                def writelines(self, lines):
                    objects.extend(list(lines))
            yield MockedGzipFile()

        return _open()

    monkeypatch.setattr(gzip, 'open', modked_open)
    monkeypatch.setattr(util, 'get_indices', lambda ngram_len: ['a'])

    cooccurrence.command(
        '-o {tmpdir} -n 5 --records-in-file 3'
        ''.format(
            tmpdir=tmpdir,
        ).split()
    )

    assert len(objects) == 8
    assert '\n'.join(objects) == (
        'often\tanalysis\t6\n'
        'often\tdescribed\t6\n'
        'often\tis\t6\n'
        'often\tas\t6\n'
        'WORD\tc1\t100\n'
        'WORD\tc3\t100\n'
        'WORD\tc2\t100\n'
        'WORD\tc4\t100'
    )
