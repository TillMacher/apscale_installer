import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apscale_installer",
    version="0.4",
    author="Till-Hendrik Macher",
    author_email="macher@uni-trier.de",
    description="Advanced Pipeline for Simple yet Comprehensive AnaLysEs of DNA metabarcoding data - Conda installer (workaround)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/apscale_installer/",
    packages=setuptools.find_packages(),
    license='MIT',
    install_requires=[
                    'Requests==2.32.3'
                      ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    entry_points={
        "console_scripts": [
            "apscale_installer = apscale_installer.__main__:main",
        ]
    },
)

