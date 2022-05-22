import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", encoding="utf-8") as f:
    requirements = []
    for _requirement in f.read().splitlines():
        requirements.append(_requirement)

setuptools.setup(
    name="kisapi",
    version="0.0.1",
    author="shephexd",
    author_email="shephexd@gmail.com",
    description="Korea Investment Open API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Shephexd/kisapi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    install_requires=requirements,
)
