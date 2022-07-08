import os
from importlib.machinery import SourceFileLoader

from pkg_resources import parse_requirements
from setuptools import find_packages, setup


module_name = 'lxd'

module = SourceFileLoader(
    module_name, os.path.join(module_name, '__init__.py')
).load_module()


def load_requirements(fname) -> list:
    with open(fname) as fp:
        return [str(req) for req in parse_requirements(fp.read())]

setup(
    name=module_name.replace('_', '-'),
    version=module.__version__,
    author=module.__author__,
    author_email=module.authors_email,
    license=module.__license__,
    description=module.__doc__,
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    platforms='all',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: Russian',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    python_requires='>=3.10',
    packages=find_packages(exclude=['tests']),
    install_requires=load_requirements('requirements.txt'),
    extras_require={'dev': load_requirements('requirements.dev.txt')},
    include_package_data=True,
    project_urls={
        'Source': 'https://github.com/alvassin/lxd',
    },
)
