from setuptools import setup, find_packages

setup(
    name='prostats',
    version='0.0.1',
    description='A command-line tool to quantify  files and directories contents',
    author='joel yisrael',
    author_email='joel@sss.bot',
    packages=find_packages(),
    install_requires=[
        'termcolor',
    ],
    entry_points={
        'console_scripts': [
            'prostats = prostats.main:main',
        ],
    },
    scripts=['scripts/setup_alias.sh'],
)
