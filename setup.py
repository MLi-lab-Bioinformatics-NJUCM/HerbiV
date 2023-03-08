from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="pharmastar",
    version="0.0.1a1",
    description="药理大师是一个具有多种功能的中药网络药理学分析工具，可进行经典的网络药理学及反向网络药理学分析。Pharmastar is a multi-functional traditional chinese medicine network pharmacology analysis tool for classical network pharmacology and reverse network pharmacology.",
    # Optional
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MLi-lab-Bioinformatics-NJUCM/pharmastar",
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
    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/discussions/install-requires-vs-requirements/
    install_requires=["beautifulsoup4",
                      "numpy",
                      "pandas",
                      "pubchempy",
                      "selenium",
                      "tqdm",
                      "webdriver-manager",
                      "typing-extensions",
                      "requests",
                      ],
    project_urls={  # Optional
        "Bug Reports": "https://github.com/MLi-lab-Bioinformatics-NJUCM/pharmastar/issues",
        "Source": "https://github.com/MLi-lab-Bioinformatics-NJUCM/pharmastar",
    },
)
