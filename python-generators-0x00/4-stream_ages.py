#!/usr/bin/python3
seed = __import__('seed')


def stream_user_ages():
    """Generator that yields ages one by one from DB"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:  # Loop #1
        yield row["age"]

    cursor.close()
    connection.close()


def calculate_average_age():
    """Calculate average age in a memory-efficient way"""
    total_age = 0
    count = 0

    for age in stream_user_ages():  # Loop #2
        total_age += age
        count += 1

    if count > 0:
        avg = total_age / count
        print(f"Average age of users: {avg:.2f}")
    else:
        print("Average age of users: 0")
