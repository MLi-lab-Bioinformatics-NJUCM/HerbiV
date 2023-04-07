import os
import pandas as pd


def get_chem_protein_links(genes,
                           score=900,
                           save=True):
    r"""
    读取HerbiV_chemical_protein_links数据集，返回包含目标基因且combined_score大于等于score的记录
    :param genes: 字典类型，存储拟分析蛋白（基因）在STITCH中的ID与其名称的对应关系
    :param score: int类型，仅combined_score大于等于score的记录会被筛选出
    :param save: 布尔类型，是否保存原始分析结果
    :return: chem_protein_links: pd.DataFrame类型，HerbiV_chemical_protein_links数据集数据集中包含目标基因且Combined_score大于等于score的记录
    """

    # 读取数据集
    current_directory = os.path.dirname(os.path.abspath(__file__))
    chem_protein_links_all = pd.read_csv(current_directory + r'/data/HerbiV_chemical_protein_links.csv')

    # 选取HerbiV_chemical_protein_links数据集中Ensembl_ID为拟分析蛋白（基因）的ID、combined_score大于等于score的记录
    chem_protein_links = chem_protein_links_all.loc[
        (chem_protein_links_all['Ensembl_ID'].isin(genes)) &
        (chem_protein_links_all['Combined_score'] >= score)].copy()

    # 将Combined_score变换为0-1的浮点数
    chem_protein_links.loc[:, 'Combined_score'] = chem_protein_links.loc[:, 'Combined_score'].apply(
        lambda x: x / 1000)

    # 重新设置索引
    chem_protein_links.index = range(chem_protein_links.shape[0])

    # 保存结果
    if save:
        chem_protein_links.to_csv('result/chemical_protein_links.csv', index=False)

    return chem_protein_links
