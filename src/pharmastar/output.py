import os
import pandas as pd


def out_for_cytoscape(chem_herb, chem_protein_links_with_cheminfo):
    r"""
    输出Cytoscape用于作图的网络文件和属性文件
    :param chem_herb: pd.DataFrame类型，包含filtered_chem中化合物的名称、STITCH数据库中的CID和HERB数据库中对应的中药
    :param chem_protein_links_with_cheminfo: pd.DataFrame类型，protein_chemical数据集中包含目标基因、combined_score大于等于score且SMILES表达式长度小于等于200（可选）的记录及化合物信息
    """

    if not os.path.exists('result'):  # 若无result目录，先创建该目录
        os.mkdir('result')

    # 提取out_herb_to_chem中中药和化合物的名称并重命名列名
    out_herb_to_chem = chem_herb.loc[:, ['herb', 'name']]
    out_herb_to_chem.columns = ['SourceNode', 'TargetNode']

    # 提取chem_protein_links_with_cheminfo中在chem_herb中的化合物的名称及蛋白的名称并重命名列名
    out_chem_to_gene = chem_protein_links_with_cheminfo.loc[:, ['chemical_name', 'protein_name_of_gene']]
    out_chem_to_gene = out_chem_to_gene[out_chem_to_gene.loc[:, 'chemical_name'].isin(chem_herb.loc[:, 'name'])]
    out_chem_to_gene.columns = ['SourceNode', 'TargetNode']

    # 将out_herb_to_chem和out_chem_to_gene输出为Cytoscape的网络文件
    pd.concat([out_herb_to_chem, out_chem_to_gene]).to_csv('result/Network.csv', index=False)

    # 提取chem_herb中中药的名称并重命名列名
    out_herb = chem_herb.loc[:, ['herb']]
    out_herb.columns = ['Key']

    # 删除重复值
    out_herb = out_herb.drop_duplicates()

    for tup in out_herb.itertuples():  # 遍历out_herb中的每个中药
        if len(out_herb_to_chem.loc[out_herb_to_chem['SourceNode'] == tup[1]]) == 1:  # 若该中药只含1种out_herb_to_chem中的成分
            # 则将其属性命名为”have 其所含的成分 only“
            out_herb.loc[out_herb['Key'] == tup[1], 'Attribute'] = 'have ' + out_herb_to_chem.loc[
                out_herb_to_chem['SourceNode'] == tup[1]]['TargetNode'].all() + ' only'
        else:  # 若含多种out_herb_to_chem中的成分
            # 将其属性命名为"have many chemicals"
            out_herb.loc[out_herb['Key'] == tup[1], 'Attribute'] = 'have many chemicals'

    # 提取chem_herb中化合物的名称并重命名列名
    out_chem = chem_herb.loc[:, ['name']]
    out_chem.columns = ['Key']

    # 将其属性命名为chemical并删除重复值
    out_chem['Attribute'] = 'chemical'
    out_chem = out_chem.drop_duplicates()

    # 提取out_gene中蛋白质的名称并重命名列名
    out_gene = chem_protein_links_with_cheminfo.loc[:, ['protein_name_of_gene']]
    out_gene.columns = ['Key']

    # 将其属性命名为gene并删除重复值
    out_gene['Attribute'] = 'gene'
    out_gene = out_gene.drop_duplicates()

    # 将out_herb、out_chem和out_gene输出为Cytoscape的属性文件
    pd.concat([out_herb, out_chem, out_gene]).to_csv('result/Type.csv', index=False)
