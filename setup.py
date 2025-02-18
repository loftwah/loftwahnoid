from setuptools import setup, find_packages

setup(
    name="loftwahnoid",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pygame>=2.6.1",
        "pygame-menu>=4.5.1",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "loftwahnoid=loftwahnoid.__main__:main_menu",
        ],
    },
) 