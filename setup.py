from setuptools import find_packages, setup

setup(
    name='philly_transit_data',
    packages=find_packages(),
    version='0.0.1',
    description='Download SEPTA, NJ Transit, and PATCO data from the web',
    author='Aaron Fraint, AICP',
    license='MIT',
    # entry_points="""
    #     [console_scripts]
    #     transit=philly_transit_data.cli:main
    # """,
)