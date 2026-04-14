from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aegisscan-strategic",
    version="4.0.0",
    author="Imposter-zx",
    author_email="contact@aegisscan.example",
    description="A mission-aware adversarial simulation framework for defensive security research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Imposter-zx/AegisScan-OpenCore",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.25.1",
        "httpx>=0.23.0",
        "PyYAML>=5.4.1",
        "jinja2>=3.0.0",
        "colorama>=0.4.4",
        "tabulate>=0.8.9",
        "flask>=2.0.0",
    ],
    extras_require={
        "advanced": [
            "scapy>=2.4.5",
            "python-nmap>=0.7.1",
        ],
        "api": [
            "PyJWT>=2.6.0",
            "bcrypt>=4.0.0",
        ],
        "dev": [
            "pytest>=6.2.4",
            "black>=21.9b0",
            "flake8>=3.9.2",
        ],
    },
    entry_points={
        "console_scripts": [
            "aegisscan=main:main",
        ],
    },
)
