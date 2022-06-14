import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="resume parser",
    version="1.0.0",
    author="jspw",
    author_email="mhshifat757@gmail.com",
    description="It is a script to parse information from a cv or resume.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jspw/Resume-Parser",
    license="MIT License",
    packages=setuptools.find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "resume_parser=resume_parser.__main__:main",
        ]
    },
)
