from setuptools import setup
import pathlib

import suit


setup(
    name="suit",
    version=suit.__version__,
    description="Getitem-objects «suit» for attribute-like access",
    long_description=pathlib.Path("readme.md").read_text("utf-8"),
    author="pohmelie",
    author_email="multisosnooley@gmail.com",
    url="https://github.com/pohmelie/suit",
    license="Apache 2",
    tests_require=["pytest", "pytest-cov"],
    scripts=["suit.py"],
    python_requires=">= 3.4",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
)
