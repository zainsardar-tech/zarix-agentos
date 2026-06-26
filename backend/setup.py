# ============================================================
#  Zarix AgentOS — Python Package Setup
# ============================================================
from setuptools import find_packages, setup

setup(
    name="zarix-agentos",
    version="1.0.0",
    description="The Autonomous AI Workforce Operating System",
    author="Zain Sardar",
    author_email="contact@zarix.dev",
    url="https://github.com/zainsardar-tech/zarix-agentos",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "sqlalchemy[asyncio]",
        "asyncpg",
        "redis",
        "celery",
        "pydantic",
        "pydantic-settings",
        "openai",
        "anthropic",
        "google-generativeai",
        "mistralai",
        "httpx",
        "chromadb",
        "langgraph",
        "click",
        "rich",
        "python-jose",
        "passlib",
    ],
    entry_points={
        "console_scripts": [
            "zarix=app.cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
