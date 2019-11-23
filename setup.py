from setuptools import setup, find_packages


setup(
    name="sentimeter",

    version="0.0.1",

    description="Library built for measuring sentiment values of tweets",

    url="http://example.com",

    author="Aleksandra Wacławek",
    author_email="awaclawe@mion.elka.pw.edu.pl",

    license="MIT",

    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7"
    ],

    keywords="twitter tweet sentiment machine learning ",

    packages=find_packages(),

    install_requires=['numpy', 'vaderSentiment', 'tweepy'],

    python_requires=">=3.7",

    include_package_data=True,

    entry_points={"console_scripts": []}

)
