import os
from zipfile import ZipFile
from pkginfo import Wheel, SDist
import hashlib

import utils


class Package:
    def __init__(self, path, dependencies):
        self.dependencies = dependencies
        if path.startswith("http"):
            self.is_local = False
            self.path = utils.download_package(path)
        else:
            self.is_local = True
            self.path = os.path.abspath(path)
        self.hash = "sha256:"+self.get_digest(self.path)
        if self.path.endswith(".whl"):
            wheel = Wheel(self.path)
            self.version = wheel.version
            self.name = wheel.name
        elif self.path.endswith(".tar.gz"):
            sdist = SDist(self.path)
            self.version = sdist.version
            self.name = sdist.name

    def get_digest(self, file_path):
        h = hashlib.sha256()

        with open(file_path, 'rb') as file:
            while True:
                # Reading is buffered, so we can read smaller chunks.
                chunk = file.read(h.block_size)
                if not chunk:
                    break
                h.update(chunk)

        return h.hexdigest()

    def toJSON(self):
        return {
            "name": self.name,
            "hash": self.hash,
            'path': self.path,
            'version': self.version,
            'dependencies': self.dependencies
        }

    @classmethod
    def get_all_dependencies_recursive(cls, dependencies, lst=[]):
        dependencies = cls.get_dependencies(dependencies)
        with open("requirements.inhouse.txt", "w") as requirements:
            for sub_dep in dependencies:
                lst.append(sub_dep["package_name"])
                requirements.write(sub_dep["package_name"]+"\r\n")
                cls.get_all_dependencies_recursive(
                    sub_dep["package_name"], lst)
        return lst

    @classmethod
    def get_dependencies(cls, wheel_fname):
        inhouse = []
        # download if the file from the internet
        if wheel_fname.startswith("http"):
            wheel_fname = utils.download_package(wheel_fname)
        try:
            version = Wheel(wheel_fname).version
            archive = ZipFile(wheel_fname)
            for f in archive.namelist():
                if f.endswith("dependency_links.txt"):
                    for l in archive.open(f).read().decode("utf-8").split("\n"):
                        if len(l) > 0:
                            print("found {dependent} dependecy of {package}"
                                  .format(package=wheel_fname, dependent=l))
                            inhouse.append(
                                {"package_name": l, "version": version})
        except ValueError:
            print("ERROR: No such file or package")
            raise
        return inhouse

    # def get_version(self):
    #     if self.path.endswith(".whl"):
    #         return Wheel(self.path).version
    #     elif self.path.endswith(".tar.gz"):
    #         return SDist(self.path).version
