import os
import pandas as pd


def get_tcm_chem_links(chem,
                       save=True):
    r"""
    读取HerbiV_tcm_chemical_links数据集
    :param chem: pd.DataFrame类型，chem_protein_links中化合物的信息及其Importance Score
    :param save: 布尔类型，是否保存原始分析结果
    :return tcm_chem_links: pd.DataFrame类型，包含filtered_chem中化合物的名称、STITCH数据库中的CID和HERB数据库中对应的中药
    """

    # 读取数据集
    current_directory = os.path.dirname(os.path.abspath(__file__))
    tcm_chem_links_all = pd.read_csv(current_directory + r'/data/HerbiV_tcm_chemical_links.csv')

    # 获取含chem中化合物的中药-成分信息
    tcm_chem_links = tcm_chem_links_all.loc[tcm_chem_links_all['HVCID'].isin(chem['HVCID'])].copy()

    # 计算tcm_chemical_links的Importance Score
    tcm_chem_links.loc[:, 'Importance Score'] = tcm_chem_links.loc[:, 'HVCID'].apply(
        lambda x: chem.loc[chem['HVCID'] == x]['Importance Score'].iloc[0])

    # 重新设置索引
    tcm_chem_links.index = range(tcm_chem_links.shape[0])

    # 保存结果
    if save:
        tcm_chem_links.to_csv('result/tcm_chemical_links.csv', index=False)

    return tcm_chem_links
