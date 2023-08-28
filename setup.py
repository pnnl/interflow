import re
from setuptools import setup, find_packages


def readme():
    """Return the contents of the project README file."""
    with open('README.md') as readme:
        return readme.read()


# get version from __init__ of package
version = re.search(r"__version__ = ['\"]([^'\"]*)['\"]", open('interflow/__init__.py').read(), re.M).group(1)

setup(
    name='interflow',
    version=version,
    packages=find_packages(),
    url='https://github.com/pnnl/interflow',
    license='BSD2-Clause',
    author='Kendall Mongird',
    author_email='kendall.mongird@pnnl.gov',
    description='An open-source Python package for calculating and organizing sectoral flows and interdependencies',
    long_description=readme(),
    long_description_content_type="text/markdown",
    python_requires='>=3.7',
    include_package_data=False,
    install_requires=[
        'numpy>=1.19.4',
        'pandas>=1.3.4',
        'plotly>=5.5.0',
        'json5>=0.9.6'
    ],
    extras_require={
        'dev': ['build>=0.7.0',
                'setuptools>=58.2.0',
                'sphinx>=4.4.0',
                'twine>=3.8.0',
                'sphinxemoji>=0.2.0']}
)
