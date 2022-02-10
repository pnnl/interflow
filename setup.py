import re
from setuptools import setup, find_packages


def readme():
    """Return the contents of the project README file."""
    with open('README.md') as readme:
        return readme.read()


# get version from __init__ of package
version = re.search(r"__version__ = ['\"]([^'\"]*)['\"]", open('flow/__init__.py').read(), re.M).group(1)

setup(
    name='flow',
    version=version,
    packages=find_packages(),
    url='https://github.com/kmongird/flow',
    license='BSD2-Clause',
    author='Kendall Mongird',
    author_email='kendall.mongird@pnnl.gov',
    description='An open-source Python package for calculating multi-sectoral '
                'and multi-unit flows and interdependencies',
    long_description=readme(),
    long_description_content_type="text/markdown",
    python_requires='>=3.7.*, <4',
    include_package_data=True,
    install_requires=[
        'pandas>=1.3.4',
        'PyYAML>=5.4.1',
        'matplotlib>=3.3.3'
        'plotly>=5.5'
    ]
)
