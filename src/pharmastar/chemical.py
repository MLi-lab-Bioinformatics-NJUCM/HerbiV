import os
import pandas as pd
import numpy as np


def get_chemicals(chem_protein_links,
                  save=True):
    r"""
    读取HerbiV_chemicals数据集，返回chem_protein_links中化合物的信息并计算其Importance Score
    :param chem_protein_links: pd.DataFrame类型，HerbiV_chemical_protein_links数据集数据集中包含目标基因且Combined_score大于等于score的记录
    :param save: 布尔类型，是否保存原始分析结果
    :return: chem: pd.DataFrame类型，chem_protein_links中化合物的信息及其Importance Score
    """
    # 读取数据集
    current_directory = os.path.dirname(os.path.abspath(__file__))
    chem_all = pd.read_csv(current_directory + r'/data/HerbiV_chemicals.csv')

    # 在HerbiV_chemicals中获取chem_protein_links中化合物的信息
    chem = chem_all.loc[chem_all['HVCID'].isin(chem_protein_links['HVCID'])].drop_duplicates(subset=['HVCID'])

    # 计算化合物的Importance Score
    chem['Importance Score'] = chem.loc[:, 'HVCID'].apply(
        lambda x: 1 - (1 - np.array([*chem_protein_links.loc[chem_protein_links['HVCID'] == x]['Combined_score']])).prod())

    # 重新设置索引
    chem.index = range(chem.shape[0])

    # 保存结果
    if save:
        chem.to_csv('result/chemicals.csv', index=False)

    return chem
