import numpy as np


def score(chem_protein_links, chem, tcm_chem_links, tcm):
    """
    计算化合物和中药的Importance Score
    :param chem_protein_links: pd.DataFrame类型，用于计算的的化合物-蛋白质（靶点）的连接信息
    :param chem: pd.DataFrame类型，需要计算Importance Score的化合物信息
    :param tcm_chem_links: pd.DataFrame类型，需要计算Importance Score的化合物的中药-成分信息
    :param tcm: pd.DataFrame类型，需要计算Importance Score的中药信息
    :return: chem: pd.DataFrame类型，化合物的Importance Score的计算结果
    :return: tcm: pd.DataFrame类型，中药的Importance Score的计算结果
    """

    # 计算化合物的Importance Score
    chem['Importance Score'] = chem.loc[:, 'HVCID'].apply(
        lambda x: 1 - (
                1 - np.array([*chem_protein_links.loc[chem_protein_links['HVCID'] == x]['Combined_score']])).prod())

    # 计算中药的Importance Score
    tcm['Importance Score'] = tcm.loc[:, 'HVMID'].apply(
        lambda x: 1 - (1 - np.array([*chem.loc[
            chem['HVCID'].isin(tcm_chem_links.loc[tcm_chem_links['HVMID'] == x]['HVCID'])][
            'Importance Score']])).prod())

    # 根据Importance Score降序排序
    tcm = tcm.sort_values(by='Importance Score', ascending=False)

    # 重新设置索引
    tcm.index = range(tcm.shape[0])

    return chem, tcm


if __name__ == '__main__':
    import get

    tcm_info1 = get.get_tcm('cn_name', ['柴胡'])
    tcm_chem_links_info1 = get.get_tcm_chem_links('HVMID', tcm_info1['HVMID'])
    chem_info1 = get.get_chemicals('HVCID', tcm_chem_links_info1['HVCID'])
    chem_protein_links1 = get.get_chem_protein_links('HVCID', chem_info1['HVCID'])
    chem_info1, tcm_info1 = score(chem_protein_links1, chem_info1, tcm_chem_links_info1, tcm_info1)

    chem_protein_links2 = get.get_chem_protein_links('Ensembl_ID',
                                                     {'ENSP0000026332': 'ACACA', 'ENSP00000398698': 'TNF'}, 0)
    chem_info2 = get.get_chemicals('HVCID', chem_protein_links2['HVCID'])
    tcm_chem_links_info2 = get.get_tcm_chem_links('HVCID', chem_info2['HVCID'])
    tcm_info2 = get.get_tcm('HVMID', tcm_chem_links_info2['HVMID'])
    chem_info2, tcm_info2 = score(chem_protein_links2, chem_info2, tcm_chem_links_info2, tcm_info2)
