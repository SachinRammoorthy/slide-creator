"""
Package configuration.
"""

from setuptools import setup

setup(
    name='slideCreator',
    version='0.1.0',
    packages=['slideCreator'],
    include_package_data=True,
    install_requires=[
        'Flask',
    ],
    python_requires='>=3.8',
)
