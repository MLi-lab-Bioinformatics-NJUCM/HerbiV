<h1 align="center">
<img src="https://github.com/MLi-lab-Bioinformatics-NJUCM/HerbiV/blob/main/Logo.svg" width="2000">
</h1>

[![Downloads](https://static.pepy.tech/personalized-badge/herbiv?period=total&units=international_system&left_color=green&right_color=blue&left_text=Downloads)](https://pepy.tech/project/herbiv)
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

可以使用pip安装`herbiv`。

`pip install herbiv`

此外还需要安装依赖库`pandas`。

`pip install pandas`或`conda install pandas`

## 使用

### 基本使用

`herbiv.analysis`中提供了进行网络药理学分析的pipeline函数。

- `reverse`函数: 反向网络药理学分析的pipeline函数。使用它仅需使用命令

```python
from herbiv import analysis
analysis.reverse(genes, score, save)
```

它需要一个必需形参`genes`，这是一个存储编码拟分析靶点的基因的Ensembl ID与其名称的字典，如`{'9606.ENSP00000265022': 'DGKG'}`。

它的可选形参有
- `score`: int类型，仅combined_score大于等于score的记录会被筛选出，默认为`900`；
- `save`: 布尔类型，是否保存原始分析结果，默认为`True`。

分析结果存放在当前路径的`result`文件夹下（需先建立该文件夹）。

### 更新日志

#### 0.0.1a1

- 横空出世

#### 0.1a1(2323.3.28)

- 使用本项目自己的数据集进行分析，不再使用其他数据库的公共数据集，更新了整个分析架构，大大加快了分析速度；
- 加入了基于朴素贝叶斯的中药重要性评价模型。

####  0.1a2(2323.3.29)

- 数据集随herbiv库下载，无需指定数据集存放路径。

# English
HerbiV is a multi-functional traditional chinese medicine network pharmacology analysis tool for classical network pharmacology and reverse network pharmacology.

## Installation

You can install `herbiv` using pip.

`pip install herbiv`


In addition, you need to install the dependency `pandas`.

`pip install pandas` or `conda install pandas`

## Usage

### Basic usage

`herbiv.analysis` provides pipeline function for network pharmacology analysis.

- `reverse` : pipeline function for reverse network pharmacology. To use it, please use command

```python
from herbiv import analysis
analysis.reverse(genes, score, save)
```

It needs a required parameter `genes`, which is a dictionary that stores the Ensembl ID(s) of the gene(s) encoding the target(s) to be analyzed along with their name(s), e.g. `{'9606.ENSP00000265022': 'DGKG'}`.

Its optional parameter includes
- `score`: int, only when the combined_score is no less than it will be selected out, `900` by default;
- `save`: boolean，Whether to save the original analysis results, `True` by default.

The analysis results are stored in the result folder of the current path (need to create this folder first).

### Versions

#### 0.0.1a1

- All start at here.

#### 0.1a1(2323.3.28)

- Using the project's own datasets for analysis, instead of using public datasets from other databases. Updated the entire analysis architecture and greatly accelerated the analysis speed;
- Added a naive Bayes model-based importance evaluation model for TCM.

####  0.1a2(2323.3.29)

- The dataset is downloaded with herbiv, no need to specify the dataset storage path.
