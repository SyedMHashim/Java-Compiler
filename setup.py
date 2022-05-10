import setuptools

with open("requirements.txt", "r") as f:
    required = f.read().splitlines()
    setuptools.setup(
        name="java-compiler",
        version="0.0.1",
        author="Muhammad Hashim",
        author_email="hashim.muhammad9@gmail.com",
        packages=setuptools.find_packages(),
        install_requires=required,
        scripts=["bin/java-console"],
    )
