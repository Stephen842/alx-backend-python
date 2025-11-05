#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):
    """Fetch a page of users from the DB"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """Generator: Lazily load data one page at a time"""
    offset = 0
    while True:  # Only one loop allowed
        page = paginate_users(page_size, offset)
        if not page:
            break  # Stop when no more data
        yield page  # Generator requirement met
        offset += page_size  # Move to next page
