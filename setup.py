import setuptools

with open("README.md", "r") as f:
    README = f.read()

setuptools.setup(
    name="smguseres",
    version="1.0.0",
    author="Aurum",
    url="https://github.com/SunakazeKun/pyjkernel",
    description="Python tool to generate UseResource files for Super Mario Galaxy 2 using Dolphin logs.",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords=["nintendo", "super-mario-galaxy", "archive", "modding"],
    packages=setuptools.find_packages(),
    install_requires=[
        "pyjmap", "pyjkernel"
    ],
    python_requires=">=3.6",
    license="gpl-3.0",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3 :: Only"
    ]
)
