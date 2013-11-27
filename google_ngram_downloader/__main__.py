import sys

from opster import command
from py.path import local

from .util import iter_google_store


@command()
def download(
    ngram_len=('n', 1, 'The length of ngrams to be downloaded.'),
    output=('o', 'downloads/google_ngrams/{ngram_len}', 'The destination folder for downloaded files.'),
    verbose=('v', False, 'Be verbose.'),
):
    """Download The Google Books Ngram Viewer dataset version 20120701."""
    output = local(output.format(ngram_len=ngram_len))
    output.ensure_dir()

    for fname, url, request in iter_google_store(ngram_len, verbose=verbose):
        with output.join(fname).open('wb') as f:

            for num, chunk in enumerate(request.iter_content(1024)):
                    if verbose and not divmod(num, 1024)[1]:
                        sys.stderr.write('.')
                        sys.stderr.flush()
                    f.write(chunk)
