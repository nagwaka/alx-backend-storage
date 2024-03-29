#!/usr/bin/env python3
"""
A function that lists all documents in a collection
"""
import pymongo


def list_all(mongo_collection):
    """
    Lists all documents in a collection
    """
    doc_collection = []

    cursor = mongo_collection.find({})
    for doc in cursor:
        doc_collection.append(doc)

    return doc_collection
