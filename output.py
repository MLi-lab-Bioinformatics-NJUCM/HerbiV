import os
import pandas as pd


def out_for_cyto(chem_protein_links, chem, genes, tcm_chem_links, tcm, path='result/'):
    r"""
    输出Cytoscape用于作图的网络文件和属性文件
    :param chem_protein_links: pd.DataFrame类型，HerbiV_chemical_protein_links数据集数据集中包含目标基因且Combined_score大于等于score的记录
    :param chem: pd.DataFrame类型，chem_protein_links中化合物的信息及其Importance Score
    :param genes: pd.DataFrame类型，存储拟分析蛋白（基因）在STITCH中的ID与其名称的对应关系
    :param tcm_chem_links: pd.DataFrame类型，包含filtered_chem中化合物的名称、STITCH数据库中的CID和HERB数据库中对应的中药
    :param tcm: pd.DataFrame类型，tcm_chem_links中中药的信息及其Importance Score
    :param path: 字符串类型，存放结果的目录
    """

    chem_protein_links_c = chem_protein_links.copy()
    chem_c = chem.copy()
    genes_c = genes.copy()
    tcm_chem_links_c = tcm_chem_links.copy()
    tcm_c = tcm.copy()

    # 若无path目录，先创建该目录
    if not os.path.exists(path):
        os.mkdir(path)
    out_chem_protein_links = chem_protein_links_c.iloc[:, 0:2]
    out_chem_protein_links.columns = ['SourceNode', 'TargetNode']

    out_chem_protein_links.loc[:, 'SourceNode'] = out_chem_protein_links.loc[:, 'SourceNode'].apply(
        lambda x: chem_c.loc[chem_c['HVCID'] == x]['Name'].iloc[0] if len(
            chem_c.loc[chem_c['HVCID'] == x]['Name']) > 0 else None)

    out_chem_protein_links.dropna(subset=['SourceNode'], inplace=True)

    out_chem_protein_links.loc[:, 'TargetNode'] = out_chem_protein_links.loc[:, 'TargetNode'].apply(
        lambda x: genes_c.loc[genes_c['Ensembl_ID'] == x]['gene_name'].iloc[0] if len(
            genes_c.loc[genes_c['Ensembl_ID'] == x]['gene_name']) > 0 else None)

    out_chem_protein_links.dropna(subset=['TargetNode'], inplace=True)

    out_tcm_chem = tcm_chem_links_c.iloc[:, 0:2]
    out_tcm_chem.columns = ['SourceNode', 'TargetNode']

    out_tcm_chem.loc[:, 'SourceNode'] = out_tcm_chem.loc[:, 'SourceNode'].apply(
        lambda x: tcm_c.loc[tcm_c['HVMID'] == x]['cn_name'].iloc[0] if len(
            tcm_c.loc[tcm_c['HVMID'] == x]['cn_name']) > 0 else None)

    out_tcm_chem.dropna(subset=['SourceNode'], inplace=True)

    out_tcm_chem.loc[:, 'TargetNode'] = out_tcm_chem.loc[:, 'TargetNode'].apply(
        lambda x: chem_c.loc[chem_c['HVCID'] == x]['Name'].iloc[0] if len(
            chem_c.loc[chem_c['HVCID'] == x]['Name']) > 0 else None)

    out_tcm_chem.dropna(subset=['TargetNode'], inplace=True)

    out_chem = chem_c.loc[:, ['Name']]
    out_chem.columns = ['Key']
    out_chem['Attribute'] = 'Chemicals'

    out_tcm = tcm_c.loc[:, ['cn_name']]
    out_tcm.columns = ['Key']
    out_tcm['Attribute'] = 'TCM'

    out_gene = genes_c.loc[:, ['gene_name']]
    out_gene.columns = ['Key']
    out_gene['Attribute'] = 'gene'

    # 输出Network文件
    pd.concat([out_chem_protein_links, out_tcm_chem]).to_csv(path + 'Network.csv', index=False)

    # 输出Type文件
    pd.concat([out_tcm, out_chem, out_gene]).to_csv(path + 'Type.csv', index=False)


if __name__ == '__main__':
    import analysis

    tcm, tcm_chem_links, chem, chem_protein_links, protein =  analysis.from_tcm_protein(tcm=['柴胡', '黄芩'],
                                                                                        protein=['ENSP00000381588','ENSP00000252519'],
                                                                                        score=0,
                                                                                        out_for_cytoscape=False,
                                                                                        re=True)

    out_for_cyto(chem_protein_links, chem, protein, tcm_chem_links, tcm, path='result/')
