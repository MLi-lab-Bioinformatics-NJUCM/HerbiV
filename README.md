<h1 align="center">
<img src="https://github.com/Eliseo1122/pharmastar/blob/main/%E8%8D%AF%E7%90%86%E5%A4%A7%E5%B8%88.svg" width="300">
</h1><br>

药理大师是一个开发中的具有多种功能的中药网络药理学分析工具，可进行经典的网络药理学及反向网络药理学分析。

Pharmastar is a multi-functional traditional chinese medicine network pharmacology analysis tool under development for classical network pharmacology and reverse network pharmacology.

<!-- toc -->

- [中文](#中文)
  - [使用](#使用)
  
- [English](#english)
  - [Usage](#usage)
  
<!-- tocstop -->

# 中文

## 使用

### 基本使用

`pharmastar.analysis`中提供了进行网络药理学分析的pipeline函数。

- `reverse`函数: 反向网络药理学分析的pipeline函数。使用它仅需使用命令

```python
from pharmastar import analysis
analysis.reverse(genes,
                 protein_chemical_links_filename,
                 score,
                 chemicals_filename,
                 chunksize,
                 swiss_filename,
                 drug_likeness_num,
                 try_num)
```

它需要一个必需形参`genes`，这是一个存储编码拟分析靶点的基因的Ensembl ID与其名称的字典，如`{'9606.ENSP00000265022': 'DGKG'}`。

它的可选形参有
- `protein_chemical_links_filename`: 字符串类型，从STITCH数据库中下载的protein_chemical.links.transfer的文件名，默认为`9606.protein_chemical.links.transfer.v5.0.tsv`；
- `score`: int类型，仅combined_score大于等于score的记录会被筛选出，默认为`900`；
- `chemicals_filename`: 字符串类型，从STITCH数据库中下载的chemicals数据集的文件名，默认为`chemicals.v5.0.tsv.gz`；
- `param chunksize`: int类型，遍历chemicals数据集时的chunksize，该值过大可能耗尽计算机的内存，默认为`1000000`；
- `swiss_filename`: SwissADME的分析结果（csv文件）的路径，默认为`swissadme.csv`；
- `drug_likeness_num`: int类型，筛选类药性指标时至少有多少个为Yes，默认为`3`；
- `try_num`: int类型，pubchempy重复尝试的次数，默认为`3`。

# English
Pharmastar is a multi-functional traditional chinese medicine network pharmacology analysis tool for classical network pharmacology and reverse network pharmacology.

## Usage

### Basic usage

`pharmastar.analysis` provides pipeline function for network pharmacology analysis.

- `reverse` : pipeline function for reverse network pharmacology. To use it, please use command

```python
from pharmastar import analysis
analysis.reverse(genes,
                 protein_chemical_links_filename,
                 score,
                 chemicals_filename,
                 chunksize,
                 swiss_filename,
                 drug_likeness_num,
                 try_num)
```

It needs a required parameter `genes`, which is a dictionary that stores the Ensembl ID(s) of the gene(s) encoding the target(s) to be analyzed along with their name(s), e.g. `{'9606.ENSP00000265022': 'DGKG'}`.

Its optional parameter includes
- `protein_chemical_links_filename`: dict, filename of the dataset protein_chemical.links.transfer from STITCH database, `9606.protein_chemical.links.transfer.v5.0.tsv` by default;
- `score`: int, only when the combined_score is no less than it will be selected out, `900` by default;
- `chemicals_filename`: str, filename of the dataset chemicals from STITCH database, `chemicals.v5.0.tsv.gz` by default;
- `param chunksize`: int, chunksize of the traversal to the chemicals dataset，the computer's memory may be exhausted if it is too large, `1000000` by default;
- `swiss_filename`: pathway of the SwissADME result, `swissadme.csv` by default;
- `drug_likeness_num`: int, how many 'Yes' at least when processing ADME selection, `3` by default;
- `try_num`: int, the number of times pubchempy tries, `3` by default.
