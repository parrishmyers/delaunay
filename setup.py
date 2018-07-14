import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="irp",
    version="0.0.1",
    author="Parrish Myers",
    author_email="parrishmyers@gmail.com",
    description="Algorithms to investigate route planning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/parrishmyers/irp",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)