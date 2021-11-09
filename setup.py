import re
from setuptools import setup, find_packages


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
    description='Flow package',
    python_requires='>=3.7.*, <4',
    include_package_data=True,
    install_requires=[
        'numpy>=1.21.3',
        'pandas>=1.3.4',
        'openpyxl>=3.0.9'
    ]
)
