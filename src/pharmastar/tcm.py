import os
import pandas as pd
import numpy as np


def get_tcm(tcm_chem_links,
            save=True):
    r"""
    读取HerbiV_tcm数据集，返回tcm_chem_links中中药的信息并计算其Importance Score
    :param tcm_chem_links: pd.DataFrame类型，包含filtered_chem中化合物的名称、STITCH数据库中的CID和HERB数据库中对应的中药
    :param save: 布尔类型，是否保存原始分析结果
    :return: tcm: pd.DataFrame类型，tcm_chem_links中中药的信息及其Importance Score
    """

    # 读取数据集
    current_directory = os.path.dirname(os.path.abspath(__file__))
    tcm_all = pd.read_csv(current_directory + r'/data/HerbiV_tcm.csv')

    # 在HerbiV_tcm中获取chem_protein_links中化合物的信息
    tcm = tcm_all.loc[tcm_all['HVMID'].isin(tcm_chem_links['HVMID'])].copy()

    # 计算中药的Importance Score
    tcm['Importance Score'] = tcm.loc[:, 'HVMID'].apply(
        lambda x: 1 - (1 - np.array([*tcm_chem_links.loc[tcm_chem_links['HVMID'] == x]['Importance Score']])).prod())

    # 根据Importance Score降序排序
    tcm = tcm.sort_values(by='Importance Score', ascending=False)

    # 重新设置索引
    tcm.index = range(tcm.shape[0])

    # 保存结果
    if save:
        tcm.to_csv('result/TCM.csv', index=False)

    return tcm
