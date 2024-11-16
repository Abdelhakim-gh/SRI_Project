# IMDB Top 250: A Xapian Search Demo 

### Installation
1. Download Xapian
  - Get the latest stable tar ball from [its download page](http://xapian.org/download) 
  - Install its Python bindings
    - `pip install xapian`
2. Installing Xapian
  - Follow the steps in its [install page](http://xapian.org/docs/install.html)


### Index Xapian Database
- `git clone git@github.com:jingle3276/imdb250.git`
- `cd imdb250`
- Run `python index.py`


### Query the Search Engine
- Moives contain a simple keyword: `python query.py --keyword 'love'`
- Movies contain a phrase: `python query.py --keyword '"once again"'`
- Title of movies contain the word 'king': `python query.py --title 'king'`
- Show facets on result(movie's rating): `python query.py --keyword 'love' --show_facets`
- Moives directed by Steven Spielberg in 1990s `python query.py --keyword '"Steven Spielberg"' --year_range 1990..2000`
