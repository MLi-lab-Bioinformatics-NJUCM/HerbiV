<h1 align="center">
<img src="https://github.com/Eliseo1122/HerbiV/blob/main/Logo.svg" width="2000">
</h1>

[![Downloads](https://static.pepy.tech/personalized-badge/herbiv?period=total&units=international_system&left_color=green&right_color=blue&left_text=PyPI%20Downloads)](https://pepy.tech/project/herbiv)
[![Downloads](https://static.pepy.tech/personalized-badge/pharmastar?period=month&units=international_system&left_color=green&right_color=blue&left_text=Old%20Version(Pharmastar)%20Downloads)](https://pepy.tech/project/pharmastar)

HerbiV一个开发中的具有多种功能的中药网络药理学分析工具，可进行经典的网络药理学及反向网络药理学分析。

HerbiV is a multi-functional traditional chinese medicine network pharmacology analysis tool under development for classical network pharmacology and reverse network pharmacology.

<!-- toc -->

- [中文](#中文)
  - [安装](#安装)
  - [使用](#使用)
  - [更新日志](#更新日志)
  
- [English](#english)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Versions](#versions) 
 
<!-- tocstop -->

# 中文

## 安装

可以使用pip安装HerbiV。

`pip install herbiv`

## 使用

### 基本使用

`herbiv.analysis`中提供了进行网络药理学分析的pipeline函数。

- `reverse`函数: 反向网络药理学分析的pipeline函数。使用它仅需使用命令

```python
from herbiv import analysis
analysis.reverse(genes,
                 protein_chemical_links_path,
                 score,
                 save,
                 chemicals_path,
                 tcm_chemical_links_path,
                 tcm_path)
```

它需要一个必需形参`genes`，这是一个存储编码拟分析靶点的基因的Ensembl ID与其名称的字典，如`{'9606.ENSP00000265022': 'DGKG'}`。

它的可选形参有
- `protein_chemical_links_path`: 字符串类型，HerbiV_chemical_protein_links数据集的路径，默认为`data/HerbiV_chemical_protein_links.csv`；
- `score`: int类型，仅combined_score大于等于score的记录会被筛选出，默认为`900`；
- `save`: 布尔类型，是否保存原始分析结果，默认为`True`；
- `chemicals_path`: 字符串类型，HerbiV_chemicals数据集的路径，默认为`data/HerbiV_chemicals.csv`；
- `tcm_chemical_links_path`: 字符串类型，HerbiV_tcm_chemical_links数据集的路径，默认为`data/HerbiV_tcm_chemical_links.csv`；
- `tcm_path`: 字符串类型，HerbiV_tcm数据集的路径，默认为`data/HerbiV_tcm.csv`。

### 更新日志

#### 0.0.1a1

- 横空出世

#### 0.1a1(2323.3.28)

- 使用本项目自己的数据集进行分析，不再使用其他数据库的公共数据集，更新了整个分析架构，大大加快了分析速度；
- 加入了基于朴素贝叶斯的中药重要性评价模型。

# English
HerbiV is a multi-functional traditional chinese medicine network pharmacology analysis tool for classical network pharmacology and reverse network pharmacology.

## Installation

You can install HerbiV using pip.

`pip install herbiv`

## Usage

### Basic usage

`herbiv.analysis` provides pipeline function for network pharmacology analysis.

- `reverse` : pipeline function for reverse network pharmacology. To use it, please use command

```python
from herbiv import analysis
analysis.reverse(genes,
                 protein_chemical_links_path,
                 score,
                 save,
                 chemicals_path,
                 tcm_chemical_links_path,
                 tcm_path)
```

It needs a required parameter `genes`, which is a dictionary that stores the Ensembl ID(s) of the gene(s) encoding the target(s) to be analyzed along with their name(s), e.g. `{'9606.ENSP00000265022': 'DGKG'}`.

Its optional parameter includes
- `protein_chemical_links_path`: str, path of the dataset HerbiV_chemical_protein_links, `9606.protein_chemical.links.transfer.v5.0.tsv` by default;
- `score`: int, only when the combined_score is no less than it will be selected out, `900` by default;
- `save`: boolean，Whether to save the original analysis results, `True` by default;
- `chemicals_path`: str, path of the dataset HerbiV_chemicals, `data/HerbiV_chemicals.csv` by default;
- `tcm_chemical_links_path`: str, path of the dataset HerbiV_chemicals, `data/HerbiV_chemicals.csv` by default;
- `tcm_path`: str, path of the dataset HerbiV_tcm, `data/HerbiV_tcm.csv` by default.

### Versions

#### 0.0.1a1

- All start at here.

#### 0.1a1(2323.3.28)

- Using the project's own datasets for analysis, instead of using public datasets from other databases. Updated the entire analysis architecture and greatly accelerated the analysis speed;
- Added a naive Bayes model-based importance evaluation model for TCM.
