#!/usr/bin/env python3
"""
Script that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def get_logs_stats(mongo_collection):
    """
    Provide some stats about Nginx logs stored in MongoDB
    """
    total_logs = mongo_collection.count_documents({})

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: mongo_collection.count_documents(
                    {"method": method}) for method in methods}

    # Number of documents with method=GET and path=/status
    status_count = mongo_collection.count_documents(
                    {"method": "GET", "path": "/status"})

    return total_logs, method_counts, status_count


if __name__ == "__main__":
    # Connect to MongoDB

    client = MongoClient("mongodb://localhost:27017/")
    db = client["logs"]
    collection = db["nginx"]

    # Get stats
    total_logs, method_counts, status_count = get_logs_stats(collection)

    # Display stats
    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")
    print(f"{status_count} status check")
