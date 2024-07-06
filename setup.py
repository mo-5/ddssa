from setuptools import setup, find_packages


def read_requirements(filename):
    with open(filename) as f:
        return f.read().splitlines()


setup(
    name="ddssa",
    version="1.0.0",
    description="Data-Driven Software Security Assessment",
    author="Khalil Aalab, John Breton, Samuel Gamelin, Mohamed Radwan",
    author_email="khalil.aalab@carleton.ca, john.breton@carleton.ca, samuel.gamelin@carleton.ca, mohamed.radwan@carleton.ca",
    packages=find_packages(),
    install_requires=read_requirements("requirements.txt"),
    extras_require={"dev": read_requirements("requirements-dev.txt")},
    python_requires=">=3.9",
)
