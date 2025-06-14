from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="instagram-downloader",
    version="0.1.0",
    author="Instagram Downloader Contributors",
    author_email="example@example.com",
    description="A Python library for downloading and processing Instagram content using gallery-dl",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eloktev/instagram-downloader",
    packages=find_packages(include=['instagram_downloader', 'instagram_downloader.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Video",
    ],
    python_requires=">=3.6",
    install_requires=[
        "gallery-dl>=1.29.0",
        "httpx>=0.23.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "black>=20.8b1",
            "isort>=5.7.0",
            "flake8>=3.8.4",
        ],
    },
)
