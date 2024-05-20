[**中文**](./README.md) | [**English**](./README_EN.md)
<h1 align="center">
<img src="https://github.com/MLi-lab-Bioinformatics-NJUCM/HerbiV/blob/main/slogan.png" width="2000" alt="slogan">
</h1>

[![Downloads](https://static.pepy.tech/personalized-badge/herbiv?period=total&units=international_system&left_color=brightgreen&right_color=blue&left_text=Downloads)](https://pepy.tech/project/herbiv)

HerbiV(Bidirectional and Visible Database of Herb)既是一个数据库，又是一个强大的数据分析平台，集成了50多万条方剂、中药、成分、靶点数据，
以及经过检验的中药和中药组合对疾病靶点潜在作用的评价模型和中药及复方组合的优化模型，旨在推动中医药现代化进程。
<!-- toc -->

- [安装](#安装)
- [使用](#使用)
  - [`from_tcm_or_formula`](#from_tcm_or_formula)
  - [`from_proteins`](#from_proteins)
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

# CLI(Command Line Interface)

herbiv-cli 是对 herbiv 的命令行封装，用法如下

- 查看帮助文档
```shell
python herbiv-cli.py -h
```

- 给定 tcm 分析
```shell
python herbiv-cli.py --function tcm --tcms HVM0367 HVM1695 --path result
```

- 给定 formula 分析
```shell
python herbiv-cli.py --function formula --formulas HVP1625 --path result
```

- 给定 tcm 和 protein 分析
```shell
python herbiv-cli.py --function tcm_protein --tcms HVM0367 HVM1695 --proteins ENSP00000043402 --path result
```

- 给定 formula 和 protein 分析
```shell
python herbiv-cli.py --function formula_protein --formulas HVP1625 --protein ENSP00000043402 ENSP00000223366 --path result
```

- 给定 protein 分析
```shell
python herbiv-cli.py --function protein --proteins ENSP00000381588 --score 600
```

