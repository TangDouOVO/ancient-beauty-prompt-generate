from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ancient-beauty-prompt-generate",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="古风图片生成提示词生成器",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ancient-beauty-prompt-generate",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "prompt-gen=scripts.generate_prompt:main",
        ],
    },
)
