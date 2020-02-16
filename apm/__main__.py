
import os
import subprocess
# from dotenv import load_dotenv
from argparse import ArgumentParser
from .Package import Package
from .Publish import publish

temp_folder = None


def parse_args():
    try:
        parser = ArgumentParser()
        subparsers = parser.add_subparsers()

        # Publish parser
        publish_parser = subparsers.add_parser("publish", help='package')
        publish_parser.set_defaults(cmd='publish')

        publish_parser.add_argument(dest="package",
                                    metavar="package to publish")

        # Install parser
        install_parser = subparsers.add_parser("install",  help='package name')
        install_parser.set_defaults(cmd='install')

        install_parser.add_argument(dest="package",
                                    help="Install package",
                                    metavar="package Name")
        install_parser.add_argument("-C", "--command",
                                    dest="pip_command",
                                    help="package manger to use",
                                    default="pipenv",
                                    metavar="command (pip or pipenv)")
        args = parser.parse_args()
        if args.cmd == "install":
            try:
                Package.get_all_dependencies_recursive(args.package)
                install_from_local_req_file(command=args.pip_command)
            except ValueError:
                pass  # Handeled in get_dependencies function
        elif args.cmd == "publish":
            package = Package(path=args.package)
            publish(package)
    except AttributeError as e:
        print(e)
        # print the help and exit
        parser.print_help()
    except Exception as e:
        print("an error accurd")
        print(type(e))
        print(e)


def search_db(package_name, version="latest"):
    pass


def install_from_local_req_file(command):
    subprocess.check_call(
        [command, "install", "-r", "requirements.inhouse.txt"])


def main():
    global temp_folder
    # load_dotenv()
    temp_folder = os.getenv("temp_folder")
    parse_args()


if __name__ == "__main__":
    main()
