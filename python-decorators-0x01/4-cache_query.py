import time
import sqlite3 
import functools


query_cache = {}

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

"""your code goes here"""
# Cache decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Get query string either kwarg or first positional argument after conn
        query = kwargs.get("query") if "query" in kwargs else args[0]

        # Check if query already cached
        if query in query_cache:
            print("Returning cached result")
            return query_cache[query]

        # Otherwise execute query and save to cache
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        print("Query executed and cached")
        return result

    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
