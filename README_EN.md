[**中文**](./README.md) | [**English**](./README_EN.md)
<h1 align="center">
<img src="https://github.com/MLi-lab-Bioinformatics-NJUCM/HerbiV/blob/main/logo.png" width="200">
</h1>

[![Downloads](https://static.pepy.tech/personalized-badge/herbiv?period=total&units=international_system&left_color=brightgreen&right_color=blue&left_text=Downloads)](https://pepy.tech/project/herbiv)

HerbiV (Bidirectional and Visible Database of Herb) is a leader in the field of traditional Chinese medicine in the new era, deepening the study and development of prime medical literature. It is far more than a database, which is also a powerful data analysis platform that integrates more than 500,000 prescriptions, traditional Chinese medicine, ingredients and target data. Moreover, two tested models: the evaluation model of potential effects of TCM and TCM combinations on disease targets and the optimization model of TCM and prescription, are contained in HerbiV. All these efforts are aimed at promoting the modernization of traditional Chinese medicine.

<!-- toc -->

 - [Installation](#installation)
 - [Usage](#usage)
   - [`from_tcm`](#from_tcm)
   - [`from_proteins`](#from_proteins)
   - [`from_tcm_proteins`](#from_tcm_proteins)
 - [Versions](#versions) 
 
<!-- tocstop -->

# Installation

You can install `herbiv` with pip.

`pip install herbiv`

In addition, you need to install the dependency `pandas`.

`pip install pandas` or `conda install pandas`

# Usage

`herbiv.analysis` provides three pipeline functions which are employed for network pharmacology analysis.


## `from_tcm`

The pipeline function that is used in the classic network pharmacology analysis. Nothing except for your command is required when using it.

```python
from herbiv import analysis
from_tcm(tcm, score, ut_for_cytoscape, re, path)
```

It needs a required parameter `tcm`, which is a combined data type that can judge whether an element lies in it using in, storing the chinese name of tcm that is supposed to be inquired, e.g. `['柴胡', '黄芩']`.

Its optional parameter includes
- `score`: int, which will not be picked out unless the combined_score is no less than it, `900` by default;
- `out_for_cytoscape`: boolean, decides whether to output the file which will be used for Cytoscape mapping, `True` by default;
- `re`: boolean, decides whether to return to the original analysis results, `True` by default. If `re` is `True`, the function will turn to the result of `tcm`, `tcm_chem links`, `chem`, `chem_protein_links` and `proteins`, all of which are in pd.DataFrame form, storing the information of tcm, the information of tcm-componds or ingredients connection, the information of the compounds or the ingredients, the information of the compounds or ingredients-proteins or the targets connection and the information of the proteins or targets, respectively;
- `path`: str, which is the path to store the results, defaulted to `result/`. A corrsponding catalogue will be established automatically if the path can not be found.

## `from_proteins`

The pipeline function that is utilized for reverse network pharmacology. Only a few commands are needed to use it

```python
from herbiv import analysis
analysis.from_proteins(proteins, score, out_for_cytoscape, re, path)
```

It needs a required parameter `proteins`,  which is a combined data type that can judge whether an element lies in it using in, storing the Ensembl_ID in STITCH of the proteins or targets which are supposed to be analyzed, e.g. `['ENSP00000381588', 'ENSP00000252519']`.

Its optional parameter includes
- `score`: int, which will not be picked out unless the combined_score is no less than it, `0` by default;
- `out_for_cytoscape`: boolean, decides whether to output the file which will be used for Cytoscape mapping later, `True` by default;
- `re`: boolean, decides whether to return to the original analysis results, `True` by default. If `re` is `true`, the function will turn to the result of `tcm`, `tcm_chem links`, `chem`, `chem_protein_links` and `proteins`, all of which are in pd.DataFrame form, storing the information of tcm, the information of tcm-componds or ingredients connection, the information of the compounds or the ingredients, the information of the compounds or ingredients-proteins or the targets connection and the information of the proteins or targets, respectively;
- `path`: str, which is the path to store the results, defaulted to `result/`. A corrsponding catalogue will be established automatically if the path can not be found.

## `from_tcm_protein`

The pipeline function that searches for tcm and the targets at the same time. Only a few commands are needed to use it

```python
from herbiv import analysis
analysis.from_proteins(tcm, proteins, score, out_for_cytoscape, re, path)
```

It needs two required parameters `tcm` and `proteins`, either of which is a combined data type that can judge whether an element lies in it using in, storing the chinese name of tcm that is supposed to be inquired, e.g. `['柴胡', '黄芩']` and the Ensembl_ID in STITCH of the proteins or targets which are supposed to be analyzed, e.g. `['ENSP00000381588', 'ENSP00000252519']`.

Its optional parameter includes
- `score`: int, which will not be picked out unless the combined_score is no less than it, `0` by default;
- `out_for_cytoscape`: boolean, decides whether to output the file which will be used for Cytoscape mapping later, `True` by default;
- `re`: boolean, decides whether to return to the original analysis results, `True` by default. If `re` is `true`, the function will turn to the result of `tcm`, `tcm_chem links`, `chem`, `chem_protein_links` and `proteins`, all of which are in pd.DataFrame form, storing the information of tcm, the information of tcm-componds or ingredients connection, the information of the compounds or the ingredients, the information of the compounds or ingredients-proteins or the targets connection and the information of the proteins or targets, respectively;
- `path`: str, which is the path to store the results, defaulted to `result/`. A corrsponding catalogue will be established automatically if the path can not be found.

## Versions

### 0.0.1a1
- ROARING ACROSS THE HORIZON

### 0.1a1(2023.3.28)
- From now on, the project's own data set can be utilized to run the analysis, which means the latest version will not rely on the public data set of other databases any more. Moreover, the whole analysis framework has been updated, which greatly accelerates the analysis speed;
- A traditional Chinese medicine importance evaluation model based on Naive Bayes was added.

### 0.1a2(2023.3.29)
- The data set is downloaded with the herbiv database. There is no need to specify the storage path of the data set.

### 0.1a3(2023.4.9)
- The code is refactored. The function of the classic network pharmacology analysis is added.

### 0.1a4(2023.4.14)
- The pipline function `from_tcm_protein` is added, which allows searching for the tcm and the targets at the same time;
- The data set Herbiv_proteins is added.

### 0.1a5(2023.4.19)
- The stability increases, which means it will not output nodes that are isolated from the network;
- The calling method of the functions is unified.

### 0.1a6(2023.5.27)
- The vis function is added in output, which can output network graphics based on ECharts.
-  The pipline function is modified accordingly.
