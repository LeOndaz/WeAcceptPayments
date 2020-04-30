import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="weacceptpayments", # Replace with your own username
    version="2.1",
    author="Ahmed I.Elsayed",
    author_email="ahmeddark369@gmail.com",
    description="Make payments using weaccept.co API and Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LeOndaz/WeAcceptPayments",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)