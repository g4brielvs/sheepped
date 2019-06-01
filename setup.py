import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="sheepped",
    author="Gabriel Stefanini",
    author_email="g4brielvs@gbrielvs.me",
    description="A Python wrapper for tracking delivery!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/g4brielvs/sheepped",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ],
    keywords='shipping, usps',
    install_requires=[
        'lxml', 
        'requests', 
        'xmltodict'],
    version="0.1.1",
)