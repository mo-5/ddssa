from setuptools import setup, find_packages

with open("README.md") as readme:
    long_description = readme.read()

setup(
    name="setup-example",
    version="0.0.1",
    description="setup.py example",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="johnbreton",
    author_email="johnbreton@cmail.carleton.ca",
    license="The Unlicence",
    url="https://github.com/mo-5/ddssa",
    packages=find_packages(exclude=("tests*", "testing")),
    install_requires=["docutils", "jsonschema==4.1.*", "requests>=2"],
    python_requires="~=3.5",
    entry_points={"console_scripts": ["setup-example = ddssa.frontend.ui:main"]},
)
