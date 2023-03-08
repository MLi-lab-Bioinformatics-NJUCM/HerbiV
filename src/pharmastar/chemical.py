import pandas as pd
from tqdm import tqdm
import pubchempy as pcp
import numpy as np


def adme_filter(chem_info, filename='swissadme.csv', drug_likeness_num=3):
    r"""
    读入SwissADME的分析结果，筛选chem_info中GI absorption为High且类药性指标至少有drug_likeness_num个为Yes的化合物
    :param chem_info: pd.DataFrame类型，protein_chemical数据集中包含目标基因且combined_score大于等于score的记录中化合物的名称和SMILES表达式
    :param filename: SwissADME的分析结果（csv文件）的路径
    :param drug_likeness_num: int类型，筛选类药性指标时至少有多少个为Yes
    :return: filtered_chem: pd.DataFrame类型，过滤后的化合物的CID、名称和SMILES表达式
    """
    # 读入SwissADME的分析结果（csv文件）
    adme = pd.read_csv('data/' + filename,
                       usecols=['GI absorption', 'Lipinski #violations', 'Ghose #violations',
                                'Veber #violations', 'Egan #violations', 'Muegge #violations'])

    # 计算类药性指标为Yes的指标的数目
    adme['Drug likeness'] = adme.iloc[:, 1:6].apply(drug_likeness, axis=1)

    # 两数据框化合物的顺序一致，故直接合并
    adme = pd.concat([chem_info, adme], axis=1)

    # 筛选GI absorption为High且5个类药性指标至少有drug_likeness_num个为Yes的化合物
    filtered_chem = adme.loc[(adme['GI absorption'] == 'High') & (adme['Drug likeness'] >= drug_likeness_num)]

    # 返回符合筛选条件的化合物的CID、名称和SMILES表达式
    filtered_chem = filtered_chem.loc[:, ['chemical', 'name', 'SMILES_string']]

    # 重新设置索引
    filtered_chem.index = range(filtered_chem.shape[0])

    return filtered_chem


def load_washed_herb_ingredient_info():
    r"""读入清洗过的HERB_ingredient数据集"""
    return pd.read_csv('data/washed_HERB_ingredient.csv')


def combine_herb_and_stitch_chemical_info(filtered_chem, washed_herb_ingredient, try_num=3):
    r"""
    将filtered_chem中的SMILES表达式标准化，并按SMILES表达式横向合并filtered_chem和washed_herb_ingredient
    :param filtered_chem: pd.DataFrame类型，过滤后的化合物的CID、名称和SMILES表达式
    :param washed_herb_ingredient: pd.DataFrame类型，清洗过的HERB_ingredient数据集
    :param try_num: int类型，重复尝试的次数
    :return: filtered_chem: pd.DataFrame类型，过滤后的化合物的CID、名称、SMILES表达式和Ingredient_id
    """
    # 将filtered_chem中的SMILES表达式标准化
    print(str(len(filtered_chem)) + ' iterations in all', end='')
    for tup in tqdm(filtered_chem.itertuples()):
        smiles_normalized(filtered_chem, tup, 'SMILES_string', try_num)

    # 按SMILES表达式横向合并filtered_chem和washed_herb_ingredient
    filtered_chem = filtered_chem.merge(washed_herb_ingredient,
                                        left_on='SMILES_string',
                                        right_on='Ingredient_Smile',
                                        how='left').dropna().iloc[:, range(4)]

    # 重新设置索引
    filtered_chem.index = range(filtered_chem.shape[0])

    return filtered_chem


def drug_likeness(adme):
    r"""计算单个记录中类药性指标为Yes的指标的数目"""
    flag = 0
    for col in adme:
        # 数据框中为0代表Yes
        if col == 0:
            flag += 1
    return flag


def smiles_normalized(df, tup, colname, try_num=3):
    r"""
    归一化SMILES表达式
    :param df: pd.DataFrame类型，需要标准化的SMILES表达式所在的
    :param tup: pd.core.frame.Pandas类型，来自于于对df的itertuples()方法返回的迭代器
    :param colname: str类型，df中SMILES表达式所在的列的列名
    :param try_num: int类型，重复尝试的次数
    """
    # 提取tup对应的记录中的SMILES表达式
    smile = df.loc[tup[0], colname]

    # 得到smile表示的化合物在PubChem中的SMILES表达式
    pubchem_smile = try_pubchem(smile, 'smiles', try_num)

    if pubchem_smile:  # 若在PubChem中得到了smile表示的化合物的SMILES表达式，则修改df中对应的SMILES表达式
        df.loc[tup[0], colname] = pubchem_smile[0].canonical_smiles


def try_pubchem(identifier, namespace, try_num=3):
    r"""
    使用pubchempy的get_compounds多次尝试获取identifier的记录
    :param identifier: str类型，get_compounds的identifier参数，即在PubChem中检索使用的标识符
    :param namespace: str类型，get_compounds的namespace参数，cid, name, smiles, sdf, inchi, inchikey或formula.
    :param try_num: int类型，重复尝试的次数
    :return: list类型，使用pubchempy的get_compounds获取的identifier的记录；若没得到对应的记录，则返回一个空列表
    """
    for i in range(try_num):
        try:
            return pcp.get_compounds(identifier, namespace)
        except:
            continue
    print('get_compounds未找到'+identifier+'的信息')
    return []


def herb_ingredient_info_cleaner():
    # 读取HERB数据库的HERB_ingredient_info数据集
    col_names = ['Ingredient_id', 'Ingredient_Smile', 'CAS_id', 'PubChem_id', 'DrugBank_id']
    herb_ingredient = pd.read_csv('HERB_ingredient_info.txt',
                                  sep="\t",
                                  encoding='utf-8',
                                  skiprows=1,
                                  usecols=np.array([0, 4, 7, 12, 13]),
                                  names=col_names)

    # 类型转换
    herb_ingredient['Ingredient_Smile'] = herb_ingredient['Ingredient_Smile'].astype('str')
    herb_ingredient['CAS_id'] = herb_ingredient['CAS_id'].astype('str')
    herb_ingredient['DrugBank_id'] = herb_ingredient['DrugBank_id'].astype('str')
