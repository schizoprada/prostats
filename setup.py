from setuptools import setup, find_packages

# Read the content of your README file
try:
    with open("README.rst", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "A command-line tool to quantify files and directories contents"

setup(
    name='prostats',
    version='0.0.1',
    description='A command-line tool to quantify files and directories contents',
    long_description=long_description,  # Use the README content as the long description
    long_description_content_type="text/x-rst",  # Specify the content type as reStructuredText
    author='Joel Yisrael',
    author_email='joel@sss.bot',
    packages=find_packages(),
    install_requires=[
        'termcolor',
    ],
    entry_points={
        'console_scripts': [
            'prostats=prostats.main:main',
        ],
    },
    scripts=['scripts/setup_alias.sh'],
)
