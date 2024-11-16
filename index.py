import sys
import os
import re
import errno
import json
from contextlib import closing
import xapian as _x
from fetch_data import fetch_movies


FIELDS = ['Title', 'Plot', "Actors", "Director", "Year", "Rated"]
RATED = ["G", "PG", "PG-13", "R", "N/A"]
SLOT_YEAR = 0
SLOT_RATED = 1


def _format_rated(rated):
    if rated not in RATED:
        return "N/A"
    return rated

def main():
    movies = fetch_movies()

    # try to make a db in pwd
    try:
        os.mkdir('./xdb/')
    except (OSError, IOError) as e:
        if e.errno != errno.EEXIST:
            raise

    with closing(_x.WritableDatabase('./xdb/movies.db',
                                     _x.DB_CREATE_OR_OPEN)) as x_db:
        for rank, mov in movies:
            # make a new document
            x_doc = _x.Document()

            # setup indexer
            indexer = _x.TermGenerator()
            indexer.set_stemmer(_x.Stem("english"))
            indexer.set_document(x_doc)

            title = mov.get(u"Title")
            plot = mov.get(u"Plot")
            actors = mov.get(u'Actors')
            directors = mov.get(u"Director")
            year = mov.get(u'Year')
            rated = mov.get(u'Rated')

            # index terms
            indexer.index_text(plot)
            indexer.index_text(title, 1, "S")
            indexer.index_text(title)
            indexer.index_text(actors)
            indexer.index_text(directors)

            # index year as value(serizlized) for range query
            x_doc.add_value(SLOT_YEAR, _x.sortable_serialise(int(year)))
            rated_value = _format_rated(rated)
            # add a boolean term for filtering on rated
            x_doc.add_boolean_term("XRATED:{}".format(rated_value))
            # index rated as value for faceting
            x_doc.add_value(SLOT_RATED, rated_value)

            # store the data blob to the document
            data = {sel: mov[sel] for sel in FIELDS}
            data['rank'] = rank
            x_doc.set_data(json.dumps(data, encoding='utf8'))

            # save
            x_db.replace_document(rank, x_doc)

        print("indexing done")

if __name__ == '__main__':
    sys.exit(main())
