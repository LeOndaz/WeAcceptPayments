import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="weacceptpayments", # Replace with your own username
    version="2.0",
    author="Ahmed I.Elsayed",
    author_email="ahmeddark369@gmail.com",
    description="Make payments using weaccept.co API and Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
<<<<<<< HEAD
    url="https://github.com/LeOndaz/WeAcceptPayments",
=======
    url="https://github.com/pypa/sampleproject",
>>>>>>> 1200fc5c14c984607ffe59a7ec26984b0ed90581
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)