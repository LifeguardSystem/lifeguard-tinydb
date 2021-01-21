from setuptools import find_packages, setup

setup(
    name="lifeguard-tinydb",
    version="0.0.3",
    url="https://github.com/LifeguardSystem/lifeguard-tinydb",
    author="Diego Rubin",
    author_email="contact@diegorubin.dev",
    license="GPL2",
    scripts=[],
    include_package_data=True,
    description="Lifeguard integration with TinyDB",
    install_requires=["lifeguard", "tinydb"],
    classifiers=["Development Status :: 3 - Alpha"],
    packages=find_packages(),
)
