import codecs
import gzip
import json
import sys
from collections import OrderedDict
from itertools import islice

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
    rewrite=('r', False, 'Always rewrite existing files.'),
    records_in_file=('', 10 ** 9, 'The number of records to be read from the Google store to store in a .json.gz file.')
):
    """Build a cooccurrence matrix based on ngram data."""
    assert ngram_len > 1
    output_dir = local(output.format(ngram_len=ngram_len))
    output_dir.ensure_dir()

    for fname, _, all_records in readline_google_store(ngram_len, verbose=verbose):
        postfix = 0
        while (True):
            records = islice(all_records, records_in_file)
            output_file = output_dir.join(
                '{fname}_{postfix}.json.gz'.format(
                    fname=fname,
                    postfix=postfix,
                )
            )

            if not rewrite and output_file.check():
                if verbose:
                    print('Skipping {} and the rest...'.format(output_file))
                break

            index = OrderedDict()
            cooccurrence = count_coccurrence(records, index)

            if not cooccurrence:
                break

            id2word = list(index)
            items = [((id2word[i], id2word[c]), v) for (i, c), v in cooccurrence.items()]
            with gzip.open(str(output_file), 'wt') as f:
                if verbose:
                    print('Writing {}'.format(output_file))
                json.dump(items, f, indent=True)

            postfix += 1


@command()
def readline(
    ngram_len=('n', 2, 'The length of ngrams to be downloaded.'),
):
    """Print the raw content."""

    # Always write utf8
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)

    for _, _, records in readline_google_store(ngram_len):
        for record in records:
            print(record)
            print('{ngram}\t{year}\t{match_count}\t{volume_count}'.format(**record._asdict()))
