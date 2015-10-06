from setuptools import setup


def file_read(file_name):
    with open(file_name, 'r') as fp:
        return fp.read()
    return False

file_name = "requirements.txt"
requires = [
    f.strip()
    for f in file_read(file_name).split("\n")
    if f.strip() != ''
]

setup(
    name="ps_query",
    version="0.1",
    packages=['ps_query'],
    install_requires=requires,
    entry_points={
        'console_scripts'   :   [
            'ps_query = ps_query.cli:ps_query'
        ]
    }
)
