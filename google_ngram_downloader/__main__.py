import gzip
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
    lang=(
        'l',
        'eng',
        'Language. [eng|eng-us|eng-gb|eng-fiction|chi-sim|fre|ger|heb|ita|rus|spa]',
    ),
):
    """Download The Google Books Ngram Viewer dataset version 20120701."""
    output = local(output.format(ngram_len=ngram_len))
    output.ensure_dir()

    for fname, url, request in iter_google_store(ngram_len, verbose=verbose, lang=lang):
        with output.join(fname).open('wb') as f:
            for num, chunk in enumerate(request.iter_content(1024)):
                if verbose and not divmod(num, 1024)[1]:
                    sys.stderr.write('.')
                    sys.stderr.flush()
                f.write(chunk)


@command()
def cooccurrence(
    ngram_len=('n', 2, 'The length of ngrams to be downloaded.'),
    output=('o', 'downloads/google_ngrams/{ngram_len}_cooccurrence', 'The destination folder for downloaded files.'),
    verbose=('v', False, 'Be verbose.'),
    rewrite=('r', False, 'Always rewrite existing files.'),
    records_in_file=(
        '',
        50000000,
        'The number of records to be read from the Google store to store in a .json.gz file.',
    ),
    lang=(
        'l',
        'eng',
        'Language. [eng|eng-us|eng-gb|eng-fiction|chi-sim|fre|ger|heb|ita|rus|spa]',
    ),
):
    """Write the cooccurrence frequencies of a word and its contexts."""
    assert ngram_len > 1
    output_dir = local(output.format(ngram_len=ngram_len))
    output_dir.ensure_dir()

    for fname, _, all_records in readline_google_store(ngram_len, lang=lang,  verbose=verbose):
        postfix = 0
        while (True):
            records = islice(all_records, records_in_file)
            output_file = output_dir.join(
                '{fname}_{postfix}.gz'.format(
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
            items = (u'{}\t{}\t{}\n'.format(id2word[i], id2word[c], str(v)) for (i, c), v in cooccurrence.items())

            with gzip.open(str(output_file), 'wb') as f:
                if verbose:
                    print('Writing {}'.format(output_file))
                for item in items:
                    f.write(item.encode('utf8'))

            postfix += 1


@command()
def readline(
    ngram_len=('n', 2, 'The length of ngrams to be downloaded.'),
    lang=(
        'l',
        'eng',
        'Language. [eng|eng-us|eng-gb|eng-fiction|chi-sim|fre|ger|heb|ita|rus|spa]',
    ),
):
    """Print the raw content."""

    for _, _, records in readline_google_store(ngram_len, lang=lang):
        for record in records:
            print(u'{ngram}\t{year}\t{match_count}\t{volume_count}'.format(**record._asdict()))
