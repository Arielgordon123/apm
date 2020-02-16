
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='APM',  # Required
    version='0.0.20',  # Required
    description='Package manager',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    package_dir={'apm': 'apm'},
    packages=['apm'],  # Required
    python_requires='>=3.5',
    install_requires=['requests', 'pkginfo', "pymongo", "dnspython",
                      "python-dotenv", "boto3"],  # Optional
    entry_points={  # Optional
        'console_scripts': [
            'apm=apm.__main__:main',
        ],
    },
)
