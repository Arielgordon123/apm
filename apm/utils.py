import os
import requests
import shutil
import logging
import boto3
import hashlib
import re
from botocore.exceptions import ClientError
# from dotenv import load_dotenv

# load_dotenv()
temp_folder = os.getenv("temp_folder")
bucket = os.getenv("bucket")


def upload_file_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    print(file_name)
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name.split("/")[-1]

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def create_temp_folder(folder=temp_folder):
    if not os.path.exists(folder):
        os.makedir(folder)


def download_package(wheel_fname, folder=temp_folder):
    create_temp_folder(folder)
    temp_file = os.path.join(folder, wheel_fname.split("/")[-1])
    response = requests.get(wheel_fname, stream=True)
    with open(temp_file, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    return temp_file


def upload_package_to_cloud(package, cloud="s3"):
    if cloud == "s3":  # if more cloud are needed
        upload_file_s3(package.path, bucket)


def get_digest(file_path):
    h = hashlib.sha256()

    with open(file_path, 'rb') as file:
        while True:
            # Reading is buffered, so we can read smaller chunks.
            chunk = file.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()


#  TODO: update regex to something like
#  https://regex101.com/r/Ly7O1x/3/
def regex_generator(term=None, version=None):
    if not version or not any(x in term for x in ["^", "~", "="]):
        return "latest"  # get latest by default
    major, minor, patch = version.split(".")
    if term == "~":
        #  Example ~=3.1.2:
        #  version 3.1.2 or later, but not version 3.2.0 or later
        return r"^{major}.{minor}.[{patch}-9]$".format(major=major,
                                                       minor=minor,
                                                       patch=patch)
    elif term == "^":
        return r"^{major}.[{minor}-9].[0-9]$".format(major=major,
                                                     minor=minor,
                                                     patch=patch)
    elif term == "=":
        return r"^{major}.{minor}.{patch}$".format(major=major,
                                                   minor=minor,
                                                   patch=patch)
