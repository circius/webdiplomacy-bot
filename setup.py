import setuptools
from glob import glob
from os.path import basename
from os.path import splitext

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dipbot",
    version="0.1",
    author="circius",
    author_email="circius@posteo.de",
    description="webdiplomacy status reporter bot for discord",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/circius/webdiplomacy-bot",
    download_url="https://github.com/circius/webdiplomacy-bot/archive/0.1.tar.gz",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
    ],
    keywords=["webdiplomacy", "bot", "discord"],
    python_requires=">=3.6",
    setup_requires=["pytest-runner",],
    install_requires=[
        "discord.py",
        "requests",
        "bs4",
        "lxml",
        "Click"
    ],
    entry_points="""
    [console_scripts]
    dipbot=dipbot.cli:cli
""",
)

