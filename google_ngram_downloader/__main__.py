import json
import sys
import gzip
from collections import OrderedDict

from opster import Dispatcher
from py.path import local

from .util import iter_google_store, readline_google_store, count_coccurrence


dispatcher = Dispatcher()
command = dispatcher.command


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


@command()
def cooccurrence(
    ngram_len=('n', 2, 'The length of ngrams to be downloaded.'),
    output=('o', 'downloads/google_ngrams/{ngram_len}_cooccurrence_matrix/', 'The destination folder for downloaded files.'),
    verbose=('v', False, 'Be verbose.'),
    n_jobs=('j', 0, 'The number of paralles jobs. Set to 0 to use all CPUs.'),
    rewrite=('r', False, 'Always rewrite existing files.')
):
    """Build a cooccurrence matrix based on ngram data."""
    assert ngram_len > 1
    output_dir = local(output.format(ngram_len=ngram_len))
    output_dir.ensure_dir()

    for fname, _, records in readline_google_store(ngram_len, verbose=verbose):
        output_file = output_dir.join(fname + '.json.gz')

        if not rewrite and output_file.check():
            if verbose:
                print('Skipping {}'.format(output_file))
            continue

        index = OrderedDict()
        cooccurrence = count_coccurrence(records, index)

        id2word = list(index)
        items = [((id2word[i], id2word[c]), v) for (i, c), v in cooccurrence.items()]
        with gzip.open(str(output_file), 'wt') as f:
            json.dump(items, f, indent=True)
