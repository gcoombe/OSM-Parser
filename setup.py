from setuptools import setup

version = "0.2.0"

setup(
    name='osmparser',
    packages= ['osmparser'],
    version=version,
    author='Graham Coombe',
    author_email='gscoombe@gmail.com',
    install_requires=[
        "requests==2.10.0"
    ]
)
