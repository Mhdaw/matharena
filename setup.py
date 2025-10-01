import os
from setuptools import setup


def get_dependencies():
    # If INSTALL_DEPS is set to 0, install only matharena itself (no deps)
    if os.getenv("INSTALL_DEPS") == "0":
        return []
    else:
        return [
            "anthropic>=0.49.0",
            "beautifulsoup4>=4.13.1",
            "google-genai>=1.11.0",
            "loguru>=0.7.3",
            "openai>=1.102.0",
            "python-fasthtml>=0.12.1",
            "regex>=2024.11.6",
            "requests>=2.32.3",
            "together>=1.3.14",
            "antlr4-python3-runtime==4.11",
            "sympy>=1.13.1",
            "pandas>=2.2.3",
            "seaborn>=0.13.2",
            "matplotlib>=3.9.3",
            "json5>=0.10.0",
            "datasets>=3.5.0",
            "modal>=1.0.0",
            "pytest>=8.3.5",
            "playwright>=1.52.0",
            "python-dotenv>=1.1.1",
            "thefuzz>=0.22.1",
            "sentence_transformers>=5.0.0",
            "transformers>=4.55.0",
            "pyyaml>=6.0",
            "openai-harmony>=0.0.4",
            "vllm>=0.10.1"
        ]


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
