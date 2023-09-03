from pymongo import MongoClient, ASCENDING

def check_and_create_indexes():
    # Connect to MongoDB
    client = MongoClient(
        "mongodb+srv://jinyoonok:jinyoon981023@cmpsc487-jinyoon.vuymlgv.mongodb.net/?retryWrites=true&w=majority")
    db = client["CMPSC487-Project"]

    # Handle TTL index for accessLogs
    access_logs_collection = db["accessLogs"]

    # Check if the TTL index exists
    indexes = access_logs_collection.list_indexes()
    ttl_exists = False
    for index in indexes:
        if index['key'] == {'entryTime': 1} and 'expireAfterSeconds' in index:
            ttl_exists = True
            break

    # Create the TTL index if it doesn't exist
    if not ttl_exists:
        access_logs_collection.create_index([("entryTime", ASCENDING)],
                                            expireAfterSeconds=157680000)  # 5 years in seconds
        print("TTL index created successfully.")
    else:
        print("This type of TTL index already exists.")

    # Handle unique index for email in users collection
    users_collection = db["users"]

    # Check if the unique index on email exists
    indexes = users_collection.list_indexes()
    email_unique_exists = False
    for index in indexes:
        if index['key'] == {'email': 1} and index['unique']:
            email_unique_exists = True
            break

    # Create the unique index on email if it doesn't exist
    if not email_unique_exists:
        users_collection.create_index([("email", ASCENDING)], unique=True)
        print("Unique index on email created successfully.")
    else:
        print("Unique index on email already exists.")

    # Handle unique index for userId in accessLogs collection
    indexes = access_logs_collection.list_indexes()
    userId_unique_exists = False
    for index in indexes:
        if index['key'] == {'userId': 1} and index['unique']:
            userId_unique_exists = True
            break

    # Create the unique index on userId if it doesn't exist
    if not userId_unique_exists:
        access_logs_collection.create_index([("userId", ASCENDING)], unique=True)
        print("Unique index on userId created successfully.")
    else:
        print("Unique index on userId already exists.")


if __name__ == '__main__':
    check_and_create_indexes()
