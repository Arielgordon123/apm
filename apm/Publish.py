import os
from .DB_conector import add_package, check_if_package_exist

from .utils import *


def publish(package):
    if check_if_package_exist(package):
        print("package exist in db")
    else:
        if package.is_local:
            utils.upload_package_to_cloud(package)
            package.path = "https://{bucket}.s3.amazonaws.com/{path}".format(
                bucket=os.getenv("bucket"),
                path=package.path.split("/")[-1])
        add_package(package)
