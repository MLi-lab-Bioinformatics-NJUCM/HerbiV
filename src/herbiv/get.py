import os
import pandas as pd


def get_tcm(by, items):
    """
    读取HerbiV_tcm数据集，返回items中中药的信息
    :param by: str类型，数据集中与items相匹配的列的列名
    :param items: pd.DataFrame或其他任何可以使用in判断一个元素是否在其中的组合数据类型，存放要查询的中药
    :return: pd.DataFrame类型，items中中药的信息
    """

    # 读取数据集
    current_directory = os.path.dirname(os.path.abspath(__file__))
    tcm_all = pd.read_csv(current_directory + r'/data/HerbiV_tcm.csv')

    # 在HerbiV_tcm中获取items中中药的信息
    tcm = tcm_all.loc[tcm_all[by].isin(items)].copy()

    # 重新设置索引
    tcm.index = range(tcm.shape[0])

    return tcm


def get_tcm_chem_links(by, items):
    """
    读取HerbiV_tcm_chemical_links数据集，返回items中中药/化合物的中药-成分信息
    :param by: str类型，数据集中与items相匹配的列的列名
    :param items: pd.DataFrame或其他任何可以使用in判断一个元素是否在其中的组合数据类型，存放要查询的中药/化合物
    :return: pd.DataFrame类型，items中中药/化合物的中药-成分信息
    """
    # 读取数据集
    current_directory = os.path.dirname(os.path.abspath(__file__))
    tcm_chem_links_all = pd.read_csv(current_directory + r'/data/HerbiV_tcm_chemical_links.csv')

    # 在HerbiV_tcm_chemical_links中获取items中中药/化合物的中药-成分连接信息
    tcm_chem_links = tcm_chem_links_all.loc[tcm_chem_links_all[by].isin(items)].copy()

    # 重新设置索引
    tcm_chem_links.index = range(tcm_chem_links.shape[0])

    return tcm_chem_links


def get_chemicals(by, items):
    """
    读取HerbiV_chemicals数据集，返回items中化合物的信息
    :param by: str类型，数据集中与items相匹配的列的列名
    :param items: pd.DataFrame或其他任何可以使用in判断一个元素是否在其中的组合数据类型，存放要查询的化合物
    :return: pd.DataFrame类型，items中化合物的信息
    """
    # 读取数据集
    current_directory = os.path.dirname(os.path.abspath(__file__))
    chem_all = pd.read_csv(current_directory + r'/data/HerbiV_chemicals.csv')

    # 在HerbiV_chemical_protein_links中获取items中化合物的信息
    chem = chem_all.loc[chem_all[by].isin(items)].drop_duplicates(subset=['HVCID'])

    # 重新设置索引
    chem.index = range(chem.shape[0])

    return chem


def get_chem_protein_links(by, items, score=900):
    """
    读取HerbiV_chemicals数据集，返回items中化合物/蛋白质的combined_score大于等于score的化合物-蛋白质（靶点）连接信息
    :param by: str类型，数据集中与items相匹配的列的列名
    :param items: pd.DataFrame或其他任何可以使用in判断一个元素是否在其中的组合数据类型，存放要查询的化合物/蛋白质
    :param score: int类型，仅combined_score大于等于score的记录会被筛选出
    :return: pd.DataFrame类型，items中化合物/蛋白质的combined_score大于等于score的化合物-蛋白质（靶点）连接信息
    """
    # 读取数据集
    current_directory = os.path.dirname(os.path.abspath(__file__))
    chem_protein_links_all = pd.read_csv(current_directory + r'/data/HerbiV_chemical_protein_links.csv')

    # 在HerbiV_chemical_protein_links中获取items中化合物/蛋白质的combined_score大于等于score的化合物-蛋白质（靶点）连接信息
    chem_protein_links = chem_protein_links_all.loc[
        (chem_protein_links_all[by].isin(items)) &
        (chem_protein_links_all['Combined_score'] >= score)].copy()

    # 将Combined_score变换为0-1的浮点数
    chem_protein_links.loc[:, 'Combined_score'] = chem_protein_links.loc[:, 'Combined_score'].apply(
        lambda x: x / 1000)

    # 重新设置索引
    chem_protein_links.index = range(chem_protein_links.shape[0])

    return chem_protein_links


if __name__ == '__main__':
    tcm_info1 = get_tcm('cn_name', ['柴胡'])
    tcm_chem_links_info1 = get_tcm_chem_links('HVMID', tcm_info1['HVMID'])
    chem_info1 = get_chemicals('HVCID', tcm_chem_links_info1['HVCID'])
    chem_protein_links1 = get_chem_protein_links('HVCID', chem_info1['HVCID'])

    chem_protein_links2 = get_chem_protein_links('Ensembl_ID', {'ENSP0000026332': 'ACACA', 'ENSP00000398698': 'TNF'}, 0)
    chem_info2 = get_chemicals('HVCID', chem_protein_links2['HVCID'])
    tcm_chem_links_info2 = get_tcm_chem_links('HVCID', chem_info2['HVCID'])
    tcm_info2 = get_tcm('HVMID', tcm_chem_links_info2['HVMID'])