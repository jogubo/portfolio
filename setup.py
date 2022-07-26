from setuptools import find_packages
from setuptools import setup


setup(
    name='Portfolio',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'sqlalchemy',
    ],
)
