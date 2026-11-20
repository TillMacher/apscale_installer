import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apscale_installer",
    version="1.0.4",
    author="Till-Hendrik Macher",
    author_email="macher@uni-trier.de",
    description="Advanced Pipeline for Simple yet Comprehensive AnaLysEs of DNA metabarcoding data - Conda installer (workaround)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TillMacher/apscale_installer",
    packages=setuptools.find_packages(),
    license='MIT',
    install_requires=[
                    'Requests>=2.32.3',
                    'tqdm>=4.70.1'
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

