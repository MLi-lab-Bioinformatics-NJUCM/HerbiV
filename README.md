<h1 align="center">
<img src="https://github.com/MLi-lab-Bioinformatics-NJUCM/HerbiV/blob/main/logo.png" width="200">
</h1>

[![Downloads](https://static.pepy.tech/personalized-badge/herbiv?period=month&units=international_system&left_color=brightgreen&right_color=blue&left_text=Downloads)](https://pepy.tech/project/herbiv)

HerbiV一个开发中的具有多种功能的中药网络药理学分析工具，可进行经典的网络药理学及反向网络药理学分析。

HerbiV is a multifunctional traditional chinese medicine network pharmacology analysis tool 
under development for classical network pharmacology and reverse network pharmacology.

<!-- toc -->

- [中文](#中文)
  - [安装](#安装)
  - [使用](#使用)
    - [`from_tcm`](#from_tcm)
    - [`from_genes`](#from_genes)
  - [更新日志](#更新日志)
  
- [English](#english)
  - [Installation](#installation)
  - [Usage](#usage)
    - [`from_tcm`](#from_tcm)
    - [`from_genes`](#from_genes)
  - [Versions](#versions) 
 
<!-- tocstop -->

# 中文

## 安装

可以使用pip安装`herbiv`。

`pip install herbiv`

此外还需要安装依赖库`pandas`。

`pip install pandas`或`conda install pandas`

## 使用


`herbiv.analysis`中提供了两个进行网络药理学分析的pipeline函数。

### `from_tcm`

经典的正向网络药理学分析的pipeline函数。使用它仅需使用命令

```python
from herbiv import analysis
from_tcm(tcm, score, re)
```

它需要一个必需形参`tcm`，这是一个list或其他任何可以使用in判断一个元素是否在其中的组合数据类型，存放要查询的中药名，
如`['柴胡', '黄芩']`。

它的可选形参有

- `score`: int类型，仅combined_score大于等于score的记录会被筛选出，默认为`900`；
- `re`: boolean类型，是否返回原始分析结果，默认为`True`。若`re`为`True`，
则函数将返回运行结果`tcm`、`tcm_chem_links`、`chem_protein_links`，它们均为pd.DataFrame类型，
分别存储了中药信息、中药-成分信息、化合物-蛋白质（靶点）信息。

### `from_genes`

```python
from herbiv import analysis
analysis.from_genes(genes, score, out_for_cytoscape, re, path)
```

它需要一个必需形参`genes`，这是一个存储编码拟分析靶点的基因的Ensembl ID与其名称的dict，
如`{'9606.ENSP00000265022': 'DGKG'}`。

它的可选形参有
- `score`: int类型，仅combined_score大于等于score的记录会被筛选出，默认为`900`；
- `out_for_cytoscape`: boolean类型，是否输出用于Cytoscape绘图的文件，默认为`True`；
- `re`: boolean类型，是否返回原始分析结果，默认为`True`。若`re`为`True`，
则函数将返回运行结果`tcm`、`tcm_chem_links`、`chem_protein_links`，它们均为pd.DataFrame类型，
分别存储了中药信息、中药-成分信息、化合物-蛋白质（靶点）信息；
- `path`: str类型，存放结果的路径，默认为`result/`。若无此路径，将自动建立相应的目录。

### 更新日志

#### 0.0.1a1

- 横空出世

#### 0.1a1(2023.3.28)

- 使用本项目自己的数据集进行分析，不再使用其他数据库的公共数据集，更新了整个分析架构，大大加快了分析速度；
- 加入了基于朴素贝叶斯的中药重要性评价模型。

####  0.1a2(2023.3.29)

- 数据集随herbiv库下载，无需指定数据集存放路径。

####  0.1a3(2023.4.9)

- 重构了代码，增加了经典的正向网络药理学分析的功能。

####  0.1a4(2023.4.14)

- 增加了同时检索中药和靶点的功能;
- 增加HerbiV_proteins数据集。


# English

## Installation

You can install `herbiv` with pip.

`pip install herbiv`

In addition, you need to install the dependency `pandas`.

`pip install pandas` or `conda install pandas`

## Usage

`herbiv.analysis` provides two pipeline functions which are employed for network pharmacology analysis.

### `from_tcm`

The pipeline function that is used in the classic network pharmacology analysis. Nothing except for your command is required when using it.

```python
from herbiv import analysis
from_tcm(tcm, score, re)
```

It needs a required parameter `tcm`, which is a list or a combined data type in any other form that can judge whether an element lying in it, e.g. `['柴胡', '黄芩']`.

Its optional parameter includes
- `score`: int, which will not be picked out unless the combined_score is no less than it, `900` by default;
- `re`: boolean, decides whether to return to the original analysis results, `True` by default. If `re` is `true`, the function will turn to the result of `tcm`, `tcm_chem links`, `chem_protein_links`, all of which are in pd.DataFrame form, storing the information of the traditional chinese medicine, the information of traditional chinese medicine-ingredients and the information of compound-protein or the target, respectively.

### `from_genes`

```python
from herbiv import analysis
analysis.from_genes(genes, score, out_for_cytoscape, re, path)
```

It needs a required parameter `genes`, which is a dict that stores the Ensembl ID and name of certain genes which are encoding the target for analysis, e.g. `{'9606.ENSP00000265022': 'DGKG'}`.

Its optional parameter includes
- `score`: int, which will not be picked out unless the combined_score is no less than it, `900` by default;
- `out_for_cytoscape`: boolean, decides whether to output the file which will be used for Cytoscape mapping later, `True` by default;
- `re`: boolean, decides whether to return to the original analysis results, `True` by default. If `re` is `true`, the function will turn to the result of `tcm`, `tcm_chem links`, `chem_protein_links`, all of which are in pd.DataFrame form, storing the information of the traditional chinese medicine, the information of traditional chinese medicine-ingredients and the information of compound-protein or the target, respectively;
- `path`: str, which is the path to store the results, defaulted to `result/`. A corrsponding catalogue will be established automatically if the path can not be found.

### Versions

#### 0.0.1a1
- ROARING ACROSS THE HORIZON

#### 0.1a1(2023.3.28)
- From now on, the project's own data set can be utilized to run the analysis, which means the latest version will not rely on the public data set of other databases any more. Moreover, the whole analysis framework has been updated, which greatly accelerates the analysis speed;
- A traditional Chinese medicine importance evaluation model based on Naive Bayes was added.

#### 0.1a2(2023.3.29)

- The data set is downloaded with the herbiv database. There is no need to specify the storage path of the data set.

#### 0.1a3(2023.4.9)

- The code is refactored. The function of the classic network pharmacology analysis is added.
