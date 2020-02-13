import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient


_db = None


def _DB():
    global _db
    if not _db:
        load_dotenv()
        CONNECTION_STRING = os.getenv("REGISTRY_DB")
        _db = MongoClient(CONNECTION_STRING)

    return _db.apm_package_registry


def check_if_package_exist(package):
    p = _DB().packages.find_one({"name": package.name, "version": package.version})
    return p is not None


def add_package(package):
    _DB().packages.insert_one(package.toJSON())
    print("package {name} version: {version} was added to db succesfully".format(
        name=package.name, version=package.version))
