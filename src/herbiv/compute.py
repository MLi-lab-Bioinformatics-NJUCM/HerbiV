import numpy as np


def score(tcm, tcm_chem_links, chem, chem_protein_links):
    """
    计算化合物和中药的Importance Score
    :param tcm: pd.DataFrame类型，中药信息
    :param tcm_chem_links: pd.DataFrame类型，中药-化合物（中药成分）连接信息
    :param chem: pd.DataFrame类型，化合物（中药成分）信息
    :param chem_protein_links: pd.DataFrame类型，化合物（中药成分）-蛋白质（靶点）连接信息
    :return: chem: pd.DataFrame类型，化合物的Importance Score的计算结果
    :return: tcm: pd.DataFrame类型，中药的Importance Score的计算结果
    """

    tcm_c = tcm.copy()
    chem_c = chem.copy()

    # 计算化合物的Importance Score
    chem_c['Importance Score'] = chem_c.loc[:, 'HVCID'].apply(
        lambda x: 1 - (
                1 - np.array([*chem_protein_links.loc[chem_protein_links['HVCID'] == x]['Combined_score']])).prod())

    # 计算中药的Importance Score
    tcm_c['Importance Score'] = tcm_c.loc[:, 'HVMID'].apply(
        lambda x: 1 - (1 - np.array([*chem_c.loc[
            chem_c['HVCID'].isin(tcm_chem_links.loc[tcm_chem_links['HVMID'] == x]['HVCID'])][
            'Importance Score']])).prod())

    # 根据Importance Score降序排序
    tcm_c = tcm_c.sort_values(by='Importance Score', ascending=False)

    # 重新设置索引
    tcm_c.index = range(tcm_c.shape[0])
    chem_c.index = range(chem_c.shape[0])

    return tcm_c, chem_c


if __name__ == '__main__':
    import get

    chem_protein_links_info = get.get_chem_protein_links('Ensembl_ID', ['ENSP0000026332', 'ENSP00000398698'])
    chem_info = get.get_chemicals('HVCID', chem_protein_links_info['HVCID'])
    tcm_chem_links_info = get.get_tcm_chem_links('HVCID', chem_info['HVCID'])
    tcm_info = get.get_tcm('HVMID', tcm_chem_links_info['HVMID'])
    tcm_info, chem_info = score(tcm_info, tcm_chem_links_info, chem_info, chem_protein_links_info)
