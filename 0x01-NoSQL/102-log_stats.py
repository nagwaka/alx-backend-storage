#!/usr/bin/env python3
"""
Improve 12-log_stats.py by adding the top 10 of the most present IPs
in the collection nginx of the database logs
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

    # Get top 10 most present IPs
    top_ips = mongo_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    return total_logs, method_counts, status_count, top_ips


if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017/")
    db = client["logs"]
    collection = db["nginx"]

    # Get stats
    total_logs, method_counts, status_count, top_ips = get_logs_stats(
                                                                    collection)

    # Display stats
    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")
    print(f"{status_count} status check")

    print("IPs:")
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")
