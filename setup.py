from setuptools import setup, find_packages

install_reqs = [
    "requests",
    "lxml",
    "cssselect",
]

setup(
    name="fa2wzl",
    version="0.0.0",
    packages=find_packages(),

    install_requires=install_reqs,
)
