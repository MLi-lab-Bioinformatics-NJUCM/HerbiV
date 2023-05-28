import os
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Graph
from pyecharts.globals import ThemeType


def out_for_cyto(tcm, tcm_chem_links, chem, chem_protein_links, protein, path='result/'):
    r"""
    输出Cytoscape用于作图的网络文件和属性文件
    :param tcm: pd.DataFrame类型，中药信息
    :param tcm_chem_links: pd.DataFrame类型，中药-化合物（中药成分）连接信息
    :param chem: pd.DataFrame类型，化合物（中药成分）信息
    :param chem_protein_links: pd.DataFrame类型，化合物（中药成分）-蛋白质（靶点）连接信息
    :param path: 字符串类型，存放结果的目录
    """
    tcm_c = tcm.copy()
    tcm_chem_links_c = tcm_chem_links.copy()
    chem_c = chem.copy()
    chem_protein_links_c = chem_protein_links.copy()
    protein_c = protein.copy()

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
        lambda x: protein_c.loc[protein_c['Ensembl_ID'] == x]['gene_name'].iloc[0] if len(
            protein_c.loc[protein_c['Ensembl_ID'] == x]['gene_name']) > 0 else None)

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

    out_gene = protein_c.loc[:, ['gene_name']]
    out_gene.columns = ['Key']
    out_gene['Attribute'] = 'Proteins'

    # 输出Network文件
    pd.concat([out_chem_protein_links, out_tcm_chem]).to_csv(path + 'Network.csv', index=False)

    # 输出Type文件
    pd.concat([out_tcm, out_chem, out_gene]).to_csv(path + 'Type.csv', index=False)


def vis(tcm, tcm_chem_links, chem, chem_protein_links, protein, path='result/'):
    r"""
    使用NetworkX可视化分析结果
    :param tcm: pd.DataFrame类型，中药信息
    :param tcm_chem_links: pd.DataFrame类型，中药-化合物（中药成分）连接信息
    :param chem: pd.DataFrame类型，化合物（中药成分）信息
    :param chem_protein_links: pd.DataFrame类型，化合物（中药成分）-蛋白质（靶点）连接信息
    :param protein: pd.DataFrame类型，蛋白质（靶点）连接信息
    :param path: 字符串类型，存放结果的目录
    """
    # 若无path目录，先创建该目录
    if not os.path.exists(path):
        os.mkdir(path)

    #chem_protein_links = pd.DataFrame(chem_protein_links)
    #tcm_chem_links = pd.DataFrame(tcm_chem_links)

    tcm_chem_merged_1 = pd.merge(tcm_chem_links, tcm, on='HVMID', how='left')
    tcm_chem_links['HVMID'] = tcm_chem_merged_1['pinyin_name']

    tcm_chem_merged_2 = pd.merge(tcm_chem_links, chem, on='HVCID', how='left')
    tcm_chem_links['HVCID'] = tcm_chem_merged_2['Name']

    tcm_chem_links = tcm_chem_links[['HVMID', 'HVCID']]

    chem_protein_merged_1 = pd.merge(chem_protein_links, chem, on='HVCID', how='right')
    chem_protein_links['HVCID'] = chem_protein_merged_1['Name']
    chem_protein_merged_2 = pd.merge(chem_protein_links, protein, on='Ensembl_ID', how='left')
    chem_protein_links['Ensembl_ID'] = chem_protein_merged_2['gene_name']

    chem_protein_links = chem_protein_links[['HVCID', 'Ensembl_ID']]

    nodes = []
    edges = []

    for index, row in tcm_chem_links.iloc[1:].iterrows():
        chinese_medicine = row[0]
        chemical_component = row[1]
        nodes.append({'name': chinese_medicine, "symbolSize": 10})
        nodes.append({'name': chemical_component, "symbolSize": 20})
        edges.append({'source': chinese_medicine, 'target': chemical_component})

    for index, row in chem_protein_links.iloc[1:].iterrows():
        chemical_component = row[0]
        target = row[1]
        nodes.append({'name': chemical_component, "symbolSize": 20})
        nodes.append({'name': target, "symbolSize": 30})
        edges.append({'source': chemical_component, 'target': target})

    unique_list = list(set(tuple(item.items()) for item in nodes))
    nodes = [dict(item) for item in unique_list]

    unique_list = list(set(tuple(item.items()) for item in edges))
    edges = [dict(item) for item in unique_list]

    Graph(init_opts=opts.InitOpts(width="2500px", height="1200px", theme=ThemeType.LIGHT)).add(
        '', nodes, edges, repulsion=8000, layout="circular", is_rotate_label=True, linestyle_opts=opts.LineStyleOpts(
            color="source", curve=0.3), label_opts=opts.LabelOpts(position="right")).set_global_opts(
        title_opts=opts.TitleOpts(title=''), legend_opts=opts.LegendOpts(
            orient="vertical", pos_left="2%", pos_top="20%")).render(path=path + "Graph.html")


if __name__ == '__main__':
    import get

    formula_info = get.get_formula('HVPID', ['HVP1625'])
    formula_tcm_links_info = get.get_formula_tcm_links('HVPID', formula_info['HVPID'])
    tcm_info = get.get_tcm('HVMID', formula_tcm_links_info['HVMID'])
    tcm_chem_links_info = get.get_tcm_chem_links('HVMID', tcm_info['HVMID'])
    chem_info = get.get_chemicals('HVCID', tcm_chem_links_info['HVCID'])
    chem_protein_links_info = get.get_chem_protein_links('HVCID', chem_info['HVCID'], 990)
    protein_info = get.get_proteins('Ensembl_ID', chem_protein_links_info['Ensembl_ID'])

    chem_info = chem_info.loc[chem_info.loc[:, 'HVCID'].isin(chem_protein_links_info['HVCID'])]
    tcm_chem_links_info = tcm_chem_links_info.loc[tcm_chem_links_info.loc[:, 'HVCID'].isin(chem_info['HVCID'])]
    tcm_info = tcm_info.loc[tcm_info.loc[:, 'HVMID'].isin(tcm_chem_links_info['HVMID'])]
    # 重新编号（chem和tcm在计算score时会重新编号，此处不再重新编号）
    tcm_chem_links_info.index = range(tcm_chem_links_info.shape[0])

    vis(tcm_info, tcm_chem_links_info, chem_info, chem_protein_links_info, protein_info)
    out_for_cyto(tcm_info, tcm_chem_links_info, chem_info, chem_protein_links_info, protein_info)
