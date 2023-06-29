from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="herbiv",
    version="0.1a7",
    description="HerbiV(Bidirectional and Visible Database of Herb)既是一个数据库，又是一个强大的数据分析平台，集成了50多万条方剂、中药、成分、靶点数据，以及经过检验的数据挖掘模型。HerbiV is far more than a database, which is also a powerful data analysis platform that integrates more than 500,000 prescriptions, traditional Chinese medicine, ingredients and target data. Moreover, two tested data mining models are contained in HerbiV.",
    # Optional
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MLi-lab-Bioinformatics-NJUCM/HerbiV",
    author="王皓阳",
    author_email="Wesady@qq.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Information Analysis"
    ],
    keywords="network pharmacology",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
                      "numpy",
                      "pandas",
                      "tqdm",
                      "pyecharts"
                      ],
    project_urls={
        "Bug Reports": "https://github.com/MLi-lab-Bioinformatics-NJUCM/pharmastar/issues",
        "Source": "https://github.com/MLi-lab-Bioinformatics-NJUCM/pharmastar",
    },
)
