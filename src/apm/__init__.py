
import os
import errno
import requests
import shutil
import subprocess
import sys

from zipfile import ZipFile
from argparse import ArgumentParser

temp_folder = os.path.dirname("./.temp/")

def parse_args():
    parser = ArgumentParser()
    
    # parser.add_argument("-p", "--publish", dest="filename",
    #     help="Sets the package you want to publish", metavar="FILE")
    # parser.add_argument("-r", "--requirements", dest="requirements", metavar="requirements",
    #     help="Sets the `requirements` list", default="requirements.txt")
    # parser.add_argument("-t", "--tag", dest="tag",
        # help="Sets tag `latest` if no --tag specified", default="latest")   
    parser.add_argument("-i", "--install", dest="package",
        help="the package that you want to install", metavar="package Name", required=True)

    # parser.add_argument("-q", "--quiet",
    #     action="store_false", dest="verbose", default=True,
    #     help="don't print status messages to stdout")

    args = parser.parse_args()
    get_all_dependencies_recursive(args.package)
    install_from_local_req_file()


def get_dependencies(wheel_fname):
    global temp_folder
    packages = {'inhouse': []}
    if wheel_fname.startswith("http"): # download if the file from the internet
        create_temp_folder()
        temp_file = os.path.join(temp_folder, wheel_fname.split("/")[-1])
        response = requests.get(wheel_fname, stream=True)
        with open(temp_file, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        wheel_fname = temp_file

    archive = ZipFile(wheel_fname)
    for f in archive.namelist():
        if f.endswith("dependency_links.txt"):
            for l in archive.open(f).read().decode("utf-8").split("\n"):
                if len(l) > 0:
                    packages['inhouse'].append(l)

    return packages

def create_temp_folder():
    global temp_folder
    if not os.path.exists(temp_folder):
        try:
            os.makedirs(temp_folder)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def install_from_local_req_file():
    subprocess.check_call(["pipenv", "install", "-r", "local_requirements.txt"])

def get_all_dependencies_recursive(dependencies):  
    dependencies = get_dependencies(dependencies)
    lst = []  
    with open("local_requirements.txt", "a") as req:
        for sub_dep in dependencies['inhouse']:
            req.write(sub_dep+"\r\n")
            get_all_dependencies_recursive(sub_dep)
    return lst

def main():
    parse_args()
    


if __name__ == "__main__":
    main()