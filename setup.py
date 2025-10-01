import os
from setuptools import setup


def get_dependencies():
    # If INSTALL_DEPS is set to 0, install only matharena itself (no deps)
    if os.getenv("INSTALL_DEPS") == "0":
        return []
    else:
        # Read dependencies from requirements.txt
        with open("requirements.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]


setup(
    name="matharena",
    version="0.1.0",
    description="Add your description here",
    author="Mislav Balunovic",
    author_email="mislav.balunovic@gmail.com",
    python_requires=">=3.10",
    packages=["matharena"],  # Adjust as needed
    package_dir={"": "src"},
    install_requires=get_dependencies(),
)
