from setuptools import setup
import pathlib

import skin


setup(
    name="skin",
    version=skin.__version__,
    description="Getitem-objects «skin» for attribute-like access",
    long_description=pathlib.Path("readme.md").read_text("utf-8"),
    author="pohmelie",
    author_email="multisosnooley@gmail.com",
    url="https://github.com/pohmelie/skin",
    license="Apache 2",
    tests_require=["pytest", "pytest-cov"],
    py_modules=["skin"],
    package_data={"": "readme.md"},
    python_requires=">= 3.4",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
)
