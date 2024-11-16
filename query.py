import sys
import argparse
from contextlib import closing
import json
import xapian as _x
from index import RATED, SLOT_RATED, SLOT_YEAR


def _query_parser(x_db):
    '''setup and return a QueryParser object'''
    qp = _x.QueryParser()
    qp.set_stemmer(_x.Stem("english"))
    qp.set_database(x_db)
    qp.set_stemming_strategy(_x.QueryParser.STEM_SOME)
    return qp


def _joinq(op, first, sec):
    '''join two queries with an operator'''
    if not first:
        return sec
    return _x.Query(op, first, sec)


def get_parser():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--keyword', type=str, help='search keyword')
    parser.add_argument('--title', type=str, help='search title only')
    parser.add_argument('--rated', nargs='*', choices=RATED)
    parser.add_argument('--year_range', type=str, help='release year range(e.g: 1950..1975)')
    parser.add_argument('--show_facets', dest='show_facets', action='store_true', default=False)
    return parser


def main(args):
    keyword = args.get('keyword')
    title = args.get('title')
    rated_list = args.get('rated')
    year_range = args.get('year_range')
    show_facets = args.get('show_facets')
    
    with closing(_x.Database('./xdb/movies.db')) as x_db:
        # get a query parser
        qp = _query_parser(x_db)

        if keyword:
            x_query = qp.parse_query(keyword)
        else:
            x_query = _x.Query.MatchAll

        if title:
            title_query = qp.parse_query(title, 0, 'S')
            x_query = _joinq(_x.Query.OP_FILTER, x_query, title_query)

        if rated_list:
            rated_queries = [_x.Query('XRATED:{}'.format(rated)) for rated in rated_list]
            rated_query = _x.Query(_x.Query.OP_OR, rated_queries)
            x_query = _joinq(_x.Query.OP_FILTER, x_query, rated_query)

        if year_range:
            qp.add_valuerangeprocessor(
                _x.NumberValueRangeProcessor(SLOT_YEAR)
            )
            year_range_query = qp.parse_query(year_range)
            x_query = _joinq(_x.Query.OP_FILTER, x_query, year_range_query)

        # setup the enquire object to perform the query
        enq = _x.Enquire(x_db)
        print(str(x_query))
        enq.set_query(x_query)

        # Set up a spy to inspect value slots on matched documents
        spy = _x.ValueCountMatchSpy(SLOT_RATED)
        enq.add_matchspy(spy)

        # iterate through the matched set and display the stored json dup
        for res in enq.get_mset(0, x_db.get_doccount(), None, None):
            print(json.dumps(json.loads(res.document.get_data()), indent=4, sort_keys=True))

        # Fetch and display the spy values
        if show_facets:
            facets = {item.term: int(item.termfreq) for item in spy.values()}
            print("Facets:{}, Total:{} ".format(facets, sum(facets.values())))


if __name__ == '__main__':
    sys.exit(main(vars(get_parser().parse_args())))
