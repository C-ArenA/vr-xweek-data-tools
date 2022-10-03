from setuptools import setup

setup(
    name="xweekdatatools",
    description="Small App to help us extract the data from the event's folders as a JSON file and others",
    version="1.0",
    author="Carlos Arena",
    entry_points={
        'console_scripts': [
            'start = xweekdatatools.py'
        ]
    }
)
