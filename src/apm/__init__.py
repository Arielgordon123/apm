
import os
import requests
import shutil
import subprocess
from zipfile import ZipFile
from argparse import ArgumentParser

temp_folder = os.path.dirname("./.temp/")


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-i", "--install", dest="package",
                        help="the package that you want to install",
                        metavar="package Name", required=True)

    args = parser.parse_args()
    get_all_dependencies_recursive(args.package)
    install_from_local_req_file()


def get_dependencies(wheel_fname):
    global temp_folder
    inhouse = []
    # download if the file from the internet
    if wheel_fname.startswith("http"):
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
                    inhouse.append(l)

    return inhouse


def create_temp_folder():
    global temp_folder
    if not os.path.exists(temp_folder):
        os.makedir(temp_folder)


def install_from_local_req_file():
    subprocess.check_call(
        ["pipenv", "install", "-r", "requirements.inhouse.txt"])


def get_all_dependencies_recursive(dependencies):
    dependencies = get_dependencies(dependencies)
    lst = []
    with open("requirements.inhouse.txt", "a") as requirements:
        for sub_dep in dependencies:
            requirements.write(sub_dep+"\r\n")
            get_all_dependencies_recursive(sub_dep)
    return lst


def main():
    parse_args()


if __name__ == "__main__":
    main()
