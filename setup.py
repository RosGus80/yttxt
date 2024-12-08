from setuptools import setup, find_packages

setup(
    name='YTTXT',
    version='0.0.1',
    packages=find_packages(exclude=["tests*"]),
    install_requires=[],
    entry_points={'console_scripts': ['yttxt=downloader.main:main']},
)
