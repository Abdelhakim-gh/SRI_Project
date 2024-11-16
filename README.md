# A Xapian Search Demo for movies

### Installation

- There are two pieces of Xapian you need to follow this guide: the library itself, and support for the language you’re going to be using. This guide was originally written with examples in Python, and we’ve made a start on full translations into Java, Perl, PHP and C++ check the [guide](https://getting-started-with-xapian.readthedocs.io/en/latest/overview.html) for more informations.
- Use ubuntu for runtime environment
- Execute `setup/install-xapian.sh` to download & setup the environment

### Index Xapian Database

- clone the project
- `cd project`
- check the `note.md` for more informations
- Run `python index.py`

### Query the Search Engine

- Moives contain a simple keyword: `python query.py --keyword 'love'`
- Movies contain a phrase: `python query.py --keyword '"once again"'`
- Title of movies contain the word 'king': `python query.py --title 'king'`
- Show facets on result(movie's rating): `python query.py --keyword 'love' --show_facets`
- Moives directed by Steven Spielberg in 1990s `python query.py --keyword '"Steven Spielberg"' --year_range 1990..2000`
