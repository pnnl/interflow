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
    url='https://github.com/kmongird/interflow',
    license='BSD2-Clause',
    author='Kendall Mongird',
    author_email='kendall.mongird@pnnl.gov',
    description='An open-source Python package for calculating and organizing sectoral flows and interdependencies',
    long_description=readme(),
    long_description_content_type="text/markdown",
    python_requires='>=3.7.*, <4',
    include_package_data=True,
    install_requires=[
        'numpy>=1.19.4',
        'pandas>=1.3.4',
        'plotly>=5.5.0',
        'json5>=0.9.6'
    ]
)
