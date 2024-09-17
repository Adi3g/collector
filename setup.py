from setuptools import setup, find_packages

# Read the contents of the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="collector",
    version="0.1.0",
    author="Adib Grouz",
    author_email="contact@adib-grouz.com",
    description="A flexible Python library for collecting, transforming, and unifying data from diverse sources into a standardized format using customizable configurations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Adi3g/collector", 
    packages=find_packages(include=["collector", "collector.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "requests>=2.25.1",
        "pandas>=1.2.0",
        "pyyaml>=5.4",
        "pyarrow>=4.0.0",
        "sqlalchemy>=1.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "flake8>=3.8",
            "black>=21.0",
            "sqlalchemy>=2.0.35",
            "pandas>=2..0.0"
        ],
    },
    entry_points={
        "console_scripts": [
            "collector=collector.scripts.run_collector:main"
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
