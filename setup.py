"""Setup script for cloud-diagram-mcp package."""
from setuptools import setup, find_packages

# Read version from __init__.py
version = {}
with open("cloud_diagram_mcp/__init__.py") as f:
    exec(f.read(), version)

# Read README for long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="cloud-diagram-mcp",
    version=version["__version__"],
    description="MCP server that visualizes cloud infrastructure and Terraform plan changes as interactive MCP App diagrams",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Aviv Eldan",
    url="https://github.com/aviveldan/cloud-diagram-mcp",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "fastmcp>=3.0.0b2",
        "diagrams>=0.23.0",
        "pillow>=10.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cloud-diagram-mcp=cloud_diagram_mcp.server:main",
        ],
    },
    keywords=["mcp", "mcp-apps", "terraform", "infrastructure", "visualization", "diagrams"],
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
    ],
)
