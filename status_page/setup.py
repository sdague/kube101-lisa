from setuptools import setup, find_packages

setup(
    name='status_page',
    version='1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'status-page=status_page:run'
        ],
    },
    install_requires=[
        'flask',
        'redis',
        'voluptuous'
    ],
)
