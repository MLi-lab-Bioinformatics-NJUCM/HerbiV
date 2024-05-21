import os
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Graph


def re_name(tcm, tcm_chem_links, chem, chem_protein_links, protein):
    """
    :param tcm: pd.DataFrame类型，中药信息
    :param tcm_chem_links: pd.DataFrame类型，中药-化合物（中药成分）连接信息
    :param chem: pd.DataFrame类型，化合物（中药成分）信息
    :param chem_protein_links: pd.DataFrame类型，化合物（中药成分）-蛋白质（靶点）连接信息
    :param protein: pd.DataFrame类型，靶点信息
    :return: 返回清洗过的数据
    """
    tcm_c = tcm.copy()
    tcm_chem_links_c = tcm_chem_links.copy()
    chem_c = chem.copy()
    chem_protein_links_c = chem_protein_links.copy()
    protein_c = protein.copy()

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

    return out_tcm, out_tcm_chem, out_chem, out_chem_protein_links, out_gene


def out_for_cyto(tcm, tcm_chem_links, chem, chem_protein_links, protein, path='result'):
    """
    输出Cytoscape用于作图的网络文件和属性文件
    :param protein:
    :param tcm: pd.DataFrame类型，中药信息
    :param tcm_chem_links: pd.DataFrame类型，中药-化合物（中药成分）连接信息
    :param chem: pd.DataFrame类型，化合物（中药成分）信息
    :param chem_protein_links: pd.DataFrame类型，化合物（中药成分）-蛋白质（靶点）连接信息
    :param path: 字符串类型，存放结果的目录
    """
    # 若无path目录，先创建该目录
    if not os.path.exists(path):
        os.mkdir(path)

    tcm, tcm_chem_links, chem, chem_protein_links, protein = \
        re_name(tcm, tcm_chem_links, chem, chem_protein_links, protein)

    # 输出Network文件
    pd.concat([chem_protein_links, tcm_chem_links]).to_csv(os.path.join(path, 'Network.csv'), index=False)

    # 输出Type文件
    pd.concat([tcm, chem, protein]).to_csv(os.path.join(path, "Type.csv"), index=False)


def vis(tcm, tcm_chem_links, chem, chem_protein_links, protein, path='result'):
    """
    使用pyecharts可视化分析结果
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

    tcm, tcm_chem_links, chem, chem_protein_links, protein = \
        re_name(tcm, tcm_chem_links, chem, chem_protein_links, protein)

    nodes = []
    edges = []

    categories = [
        {"name": "中药", "color": "#61a0a8"},
        {"name": "化学成分", "color": "#f47920"},
        {"name": "靶点", "color": "#ca8622"},
    ]

    for index, row in tcm_chem_links.iloc[0:].iterrows():
        chinese_medicine = row[0]
        chemical_component = row[1]
        nodes.append({'name': chinese_medicine, "symbolSize": 20, 'category': 0, "color": "#1FA9E9"})
        nodes.append({'name': chemical_component, "symbolSize": 20, 'category': 1, "color": "#FFFF00"})
        edges.append({'source': chinese_medicine, 'target': chemical_component})

    for index, row in chem_protein_links.iloc[0:].iterrows():
        chemical_component = row[0]
        target = row[1]
        nodes.append({'name': chemical_component, "symbolSize": 20, 'category': 1, "color": "#FFFF00"})
        nodes.append({'name': target, "symbolSize": 20, 'category': 2, "color": "#000000"})
        edges.append({'source': chemical_component, 'target': target})

    unique_list = list(set(tuple(item.items()) for item in nodes))
    nodes = [dict(item) for item in unique_list]

    unique_list = list(set(tuple(item.items()) for item in nodes))
    nodes = [dict(item) for item in unique_list]

    Graph(init_opts=opts.InitOpts(width="2400px", height="1200px")) \
        .add(
        '',
        nodes=nodes,
        links=edges,
        categories=categories,
        repulsion=8000,
        layout="circular",
        is_rotate_label=True,
        linestyle_opts=opts.LineStyleOpts(color="source", curve=0.3),
        label_opts=opts.LabelOpts(position="right")
    ) \
        .set_global_opts(
        title_opts=opts.TitleOpts(title=''),
        legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%")
    ) \
        .render(path=os.path.join(path, "Graph.html"))


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
