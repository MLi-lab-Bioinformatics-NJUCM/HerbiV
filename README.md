[**中文**](./README.md) | [**English**](./README_EN.md)
<h1 align="center">
<img src="https://github.com/MLi-lab-Bioinformatics-NJUCM/HerbiV/blob/main/slogan.png" width="2000">
</h1>

[![Downloads](https://static.pepy.tech/personalized-badge/herbiv?period=total&units=international_system&left_color=brightgreen&right_color=blue&left_text=Downloads)](https://pepy.tech/project/herbiv)

HerbiV(Bidirectional and Visible Database of Herb)既是一个数据库，又是一个强大的数据分析平台，集成了50多万条方剂、中药、成分、靶点数据，
以及经过检验的中药和中药组合对疾病靶点潜在作用的评价模型和中药及复方组合的优化模型，旨在推动中医药现代化进程。
<h1 align="center">
<img src="https://github.com/MLi-lab-Bioinformatics-NJUCM/HerbiV/blob/main/gra_abstract.tif" width="2000">
</h1>
<!-- toc -->

- [安装](#安装)
- [使用](#使用)
  - [`from_tcm_or_formula`](#from_tcm_or_formula)
  - [`from_proteins`](#from_proteins)
  - [`from_tcm_or_formula_proteins`](#from_tcm_or_formula_proteins)
- [更新日志](#更新日志)
 
<!-- tocstop -->

# 安装

可以使用pip安装`herbiv`。

`pip install herbiv`

此外还需要安装依赖库`pandas`。

`pip install pandas`或`conda install pandas`

# 使用


`herbiv.analysis`中提供了3个进行网络药理学分析的pipeline函数。

## `from_tcm_or_formula`

经典的正向网络药理学分析的pipeline函数。使用它仅需使用命令

```python
from herbiv import analysis
analysis.from_tcm_or_formula(tcm_or_formula, score, out_graph, out_for_cytoscape, re, path)
```

它需要一个必需形参`tcm_or_formula`：任何可以使用in判断一个元素是否在其中的组合数据类型，存储拟分析的中药或复方的ID，
如`['HVM0367', 'HVM1695']`。

它的可选形参有

- `score`: int类型，HerbiV_chemical_protein_links数据集中仅combined_score大于等于score的记录会被筛选出，默认为`990`；
- `out_for_cytoscape`: boolean类型，是否输出用于Cytoscape绘图的文件，默认为`True`；
- `out_graph`: boolean类型，是否输出基于ECharts的html格式的网络可视化图，默认为`True`；
- `re`: boolean类型，是否返回原始分析结果（复方（仅输入的tcm_or_formula为HVPID时）、中药、化合物（中药成分）、蛋白（靶点）及其连接信息），
默认为`True`。若`re`为`True`，则函数将返回运行结果`formula`、`formula_tcm_links`、`tcm`、`tcm_chem_links`、`chem`、
`chem_protein_links`和`proteins`（`formula`、`formula_tcm_links`仅在输入的tcm_or_formula为HVPID时返回），
它们均为pd.DataFrame类型，分别存储了复方信息、复方-中药连接信息、中药信息、中药-化合物（中药成分）连接信息、化合物（中药成分）信息、
化合物（中药成分）-蛋白（靶点）连接信息和蛋白（靶点）信息；
- `path`: str类型，存放结果的路径，默认为`results/`。若无此路径，将自动建立相应的目录。

## `from_proteins`

逆向网络药理学分析的pipeline函数。使用它仅需使用命令

```python
from herbiv import analysis
analysis.from_proteins(proteins,
                       score,
                       random_state,
                       num, 
                       tcm_component, 
                       formula_component,
                       out_for_cytoscape,
                       re,
                       path)
```

它需要一个必需形参`proteins`，这是一个任何可以使用in判断一个元素是否在其中的组合数据类型，存储拟分析蛋白（靶点）在STITCH中的Ensembl_ID，
如`['ENSP00000381588', 'ENSP00000252519']`。

它的可选形参有
- `score`: int类型，HerbiV_chemical_protein_links数据集中仅combined_score大于等于score的记录会被筛选出，默认为`0`；
- `random_state`: int类型，指定优化模型使用的随机数种子，默认为`None`，即不指定随机数种子；
- `num`: int类型，指定优化时需生成的解的组数，默认为`1000`；
- `tcm_component`: boolean类型，是否进行中药组合优化，默认为`True`；
- `formula_component`: boolean类型，是否进行复方组合优化，默认为`True`；
- `out_for_cytoscape`: boolean类型，是否输出用于Cytoscape绘图的文件，默认为`True`；
- `re`: boolean类型，是否返回原始分析结果（复方、中药、化合物（中药成分）、蛋白（靶点）及其连接信息），默认为`True`。若`re`为`True`，
则函数将返回运行结果`formula`、`formula_tcm_links`、`tcm`、`tcm_chem_links`、`chem`、`chem_protein_links`、`proteins`、`tcms`和
`formulas`，它们均为pd.DataFrame类型，分别存储了复方信息、复方-中药连接信息、中药信息、中药-化合物（中药成分）连接信息、
化合物（中药成分）信息、化合物（中药成分）-蛋白（靶点）连接信息、蛋白（靶点）信息、优化模型得到的中药组合信息（中药组合中各中药的ID、
组合对疾病相关靶点集合的潜在作用、组合前后潜在作用的提升量）和优化模型得到的复方组合信息（复方组合中各复方的ID、组合对疾病相关靶点集合的潜在作用、
组合前后潜在作用的提升量）；
- `path`: str类型，存放结果的路径，默认为`result/`。若无此路径，将自动建立相应的目录。

## `from_tcm_or_formula_proteins`

同时对中药和靶点进行检索的pipeline函数。使用它仅需使用命令

```python
from herbiv import analysis
analysis.from_proteins(tcm_or_formula, proteins, score, out_for_cytoscape, out_graph, re, path)
```

它需要2个必需形参`tcm_or_formula`和`proteins`，它们都是任何可以使用in判断一个元素是否在其中的组合数据类型，分别存储拟分析的的中药或复方的ID 
（如`['HVP1625']`）和拟分析蛋白（靶点）在STITCH中的Ensembl_ID （如`['ENSP00000381588', 'ENSP00000252519']`）。

它的可选形参有
- `score`: int类型，HerbiV_chemical_protein_links数据集中仅combined_score大于等于score的记录会被筛选出，默认为`0`；
- `out_for_cytoscape`: boolean类型，是否输出用于Cytoscape绘图的文件，默认为`True`；
- `out_graph`: boolean类型，是否输出基于ECharts的html格式的网络可视化图，默认为`True`；
- `re`: boolean类型，是否返回原始分析结果（复方（仅输入的tcm_or_formula为HVPID时）、中药、化合物（中药成分）、蛋白（靶点）及其连接信息），
默认为`True`。若`re`为`True`，则函数将返回运行结果`formula`、`formula_tcm_links`、`tcm`、`tcm_chem_links`、`chem`、
`chem_protein_links`和`proteins`（`formula`、`formula_tcm_links`仅在输入的tcm_or_formula为HVPID时返回），
它们均为pd.DataFrame类型，分别存储了复方信息、复方-中药连接信息、中药信息、中药-化合物（中药成分）连接信息、化合物（中药成分）信息、
化合物（中药成分）-蛋白（靶点）连接信息和蛋白（靶点）信息；
- `path`: str类型，存放结果的路径，默认为`result/`。若无此路径，将自动建立相应的目录。

# 更新日志

## 0.0.1a1
- 横空出世

## 0.1a1(2023.3.28)
- 使用本项目自己的数据集进行分析，不再使用其他数据库的公共数据集，更新了整个分析架构，大大加快了分析速度；
- 加入了基于朴素贝叶斯的中药重要性评价模型。

##  0.1a2(2023.3.29)
- 数据集随herbiv库下载，无需指定数据集存放路径。

##  0.1a3(2023.4.9)
- 重构了代码，增加了经典的正向网络药理学分析的功能。

##  0.1a4(2023.4.14)
- 增加了pipline函数`from_tcm_protein`，可同时检索中药和靶点;
- 增加HerbiV_proteins数据集。

## 0.1a5(2023.4.19)
- 不会输出游离于网络的节点，提高了稳定性；
- 统一了函数的调用方法。

## 0.1a6(2023.5.27)
- output中增加了vis函数，可以输出基于ECharts的网络图；
- pipline函数也做了相应的修改。

## 0.1a7(2023.6.29)
- 增加过滤无效节点的函数，提高系统的稳定性。

## 0.1a8(2023.6.30)
- vis函数绘制的网络图可为不同类节点赋予不同颜色。
