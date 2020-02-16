import os
import re
# from dotenv import load_dotenv
from pymongo import MongoClient


from .utils import *


_db = None


def _DB():
    global _db
    if not _db:
        # load_dotenv()
        CONNECTION_STRING = os.getenv("REGISTRY_DB")
        _db = MongoClient(CONNECTION_STRING)

    return _db.apm_package_registry


def check_if_package_exist(package):
    p = _DB().packages.find_one(
        {"name": package.name, "version": package.version})
    return p is not None


def add_package(package):
    _DB().packages.insert_one(package.toJSON())
    print("package {name} version: {version} was added to db succesfully".format(
        name=package.name, version=package.version))


def get_package_dependecies(package):
    packages = []
    if any(x in package for x in ["^", "~", "="]):
        name, term, version = re.split(r"(~|\^|=)", package)
        regex_pattern = utils.regex_generator(term, version)
        packages = _DB().packages.find({"name": name, "version": {
            "$regex": regex_pattern
        }}).sort("version", -1).limit(1)

    else:
        packages = _DB().packages.find(
            {"name": package}).sort("version", -1).limit(1)

    for package in packages:
        return {"dependencies": package['dependencies'],
                "path": package['path']}
