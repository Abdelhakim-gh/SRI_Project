# Project Overview

This project demonstrates how to create an Information Retrieval System (IRS) using Xapian, a search engine library. The project indexes and queries the IMDB Top 250 movies dataset. Here's a step-by-step explanation of how it works:

## 1. Fetching Data

The script `fetch_data.py` fetches movie data from the OMDB API and saves it locally:

- **`fetch_movies()`**: Checks if data is available locally in `data.json`. If not, it fetches data from the remote API using `fetch_remote()` and saves it using `save_to_cache()`.

## 2. Indexing Data

The script `index.py` indexes the fetched movie data into a Xapian database:

- **`main()` in `index.py`**:
  - Fetches movies using `fetch_movies()`.
  - Creates a Xapian database in the `./xdb/` directory.
  - For each movie, it creates a Xapian document and indexes various fields (e.g., title, plot, actors, directors, year, and rated).
  - Adds values for `year` and `rated` to support range queries and faceting.

## 3. Querying Data

The script `query.py` allows querying the indexed data:

- **`main(args)` in `query.py`**:
  - Parses command-line arguments to get query parameters (e.g., `keyword`, `title`, `rated`, `year_range`, `show_facets`).
  - Sets up a Xapian query parser and constructs a query based on the provided parameters.
  - Performs the query on the Xapian database and prints the results.
  - If `--show_facets` is enabled, it also prints facet counts for the rated field.

## Usage

### Indexing

Run the following command to fetch and index the movie data:

```sh
python index.py
```

### Querying

Use the `query.py` script with various options to query the indexed data. Examples:

```sh
python query.py --keyword 'love'
python query.py --title 'king'
python query.py --keyword 'love' --show_facets
```

## Example Usage

### Index the Data

```sh
python index.py
```

### Query the Data

```sh
python query.py --keyword 'love' --show_facets
```

This will search for movies containing the keyword "love" and display facet counts for the `rated` field.

## Detailed Steps to Test the Project

### 1. Clone the Repository

Clone the project repository to your local machine:

```sh
git clone <repository-url>
cd <repository-directory>
```

### 2. Install Dependencies

Ensure you have Python and the required libraries installed. Use `pip` to install the necessary packages:

```sh
pip install xapian
pip install requests
```

### 3. Fetch Data

Run the `fetch_data.py` script to fetch movie data from the OMDB API:

```sh
python fetch_data.py
```

### 4. Index Data

Run the `index.py` script to index the fetched movie data into a Xapian database:

```sh
python index.py
```

### 5. Query Data

Use the `query.py` script to query the indexed data. You can test various query parameters:

```sh
python query.py --keyword 'love'
python query.py --title 'king'
python query.py --keyword 'love' --show_facets
```

## Query Examples

### Basic Queries

- **Search for movies by keyword in the plot or description**:

  ```sh
  python query.py --keyword 'adventure'
  ```

- **Search for movies with a specific title**:

  ```sh
  python query.py --title 'inception'
  ```

- **Search for movies within a specific year range**:

  ```sh
  python query.py --year_range '2000..2010'
  ```

- **Search for movies with a specific rating**:

  ```sh
  python query.py --rated 'PG-13'
  ```

### Advanced Queries

- **Combine multiple parameters**:

  ```sh
  python query.py --keyword 'hero' --rated 'PG' --year_range '1990..2000'
  ```

- **Show facets (e.g., count of movies per rating)**:

  ```sh
  python query.py --keyword 'space' --show_facets
  ```

- **Use Boolean operators in keyword searches**:

  ```sh
  python query.py --keyword 'action AND comedy'
  python query.py --keyword 'drama NOT romance'
  ```

- **Search for movies directed by a specific director**:

  ```sh
  python query.py --director 'Christopher Nolan'
  ```

- **Search for movies featuring a specific actor**:

  ```sh
  python query.py --actor 'Leonardo DiCaprio'
  ```

- **Combine title and keyword searches**:

  ```sh
  python query.py --title 'star' --keyword 'war'
  ```

## Testing the Queries

### After Running the Queries:

1. **Verify Results**:

   - Ensure the movies returned match the search criteria.

2. **Check Facets**:

   - If you used `--show_facets`, ensure the facet counts are displayed correctly.

3. **Experiment**:

   - Try different combinations of parameters to understand how they affect the search results.

## Additional Notes and Considerations

### 1. Database Management

- **Location**:

  - The Xapian database is stored in the `./xdb/` directory by default.
  - You can customize the location by modifying the `index.py` and `query.py` scripts.

- **Rebuilding the Index**:

  - If you make changes to the dataset or indexing logic, you need to rebuild the index:
    ```sh
    python index.py
    ```

- **Clearing the Database**:

  - To clear the existing database, delete the `./xdb/` directory:
    ```sh
    rm -rf ./xdb/
    ```

### 2. Customizing Queries

- **Adding New Fields**:

  - Modify the `index.py` script to index additional fields (e.g., `genre`, `language`).
  - Use `add_term` to include new searchable fields.

- **Extending Query Functionality**:

  - Update the `query.py` script to support new parameters for advanced queries.
  - Example: Add support for searching by `genre` or `language`.

### 3. Debugging

- **Common Issues**:

  - **No Results Returned**: Ensure the query matches the indexed data.
  - **Database Not Found**: Verify the `./xdb/` directory exists and contains indexed data.
  - **Facets Not Displayed**: Ensure you indexed the field used for faceting (e.g., `rated`).

- **Logging**:

  - Add logging to the scripts for better debugging:
    ```python
    import logging
    logging.basicConfig(level=logging.DEBUG)
    ```

### 4. API Rate Limits

- The OMDB API may have rate limits depending on the plan you're using. To avoid issues:
  - Cache data locally in `data.json`.
  - Avoid unnecessary re-fetching of data.

## Future Improvements

### 1. Scalability

- **Distributed Indexing**:

  - Implement distributed indexing to handle larger datasets.
  - Use tools like Apache Kafka for data ingestion.

- **Sharding and Replication**:

  - Partition the Xapian database for scalability.

### 2. Search Features

- **Synonym Support**:

  - Add query expansion to include synonyms for keywords.

- **Autocomplete**:

  - Implement an autocomplete feature for user-friendly searches.

- **Spell Correction**:

  - Use libraries like `SymSpell` or integrate with third-party APIs to suggest corrections for misspelled queries.

### 3. User Interface

- Build a web-based or GUI interface to make the system accessible to non-technical users.
- Use frameworks like Flask or Django to create a front-end for querying and displaying results.

### 4. Advanced Analytics

- **Search Logs**:

  - Capture search logs to analyze query patterns and improve relevance.

- **Relevance Feedback**:

  - Implement mechanisms to learn from user interactions and refine result rankings.

## Conclusion

This project demonstrates the fundamentals of building an Information Retrieval System using Xapian. By following the provided steps, you can:

1. Fetch, index, and query data from an external API.
2. Implement a scalable and customizable search system.
3. Extend the system with advanced features like faceted search, range queries, and Boolean operators.

Feel free to enhance the system further to suit your specific needs or datasets. Happy coding!
