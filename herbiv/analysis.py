from herbiv import get
from herbiv import compute
from herbiv import output


# TODO: 将文档修改为get中的格式。
def from_tcm_or_formula(tcm_or_formula_id,
                        proteins_id=None,
                        score=990,
                        out_for_cytoscape=True,
                        out_graph=True,
                        re=True,
                        path='results'):
    """
        进行经典的正向网络药理学分析

        Args:
            tcm_or_formula_id: 任何可以使用in判断一个元素是否在其中的组合数据类型，拟分析的中药或复方的ID。
            proteins_id: None 或任何可以使用in判断一个元素是否在其中的组合数据类型，存储拟分析蛋白（靶点）在STITCH中的Ensembl_ID。
                        默认为None
            score (int): HerbiV_chemical_protein_links数据集中仅combined_score大于等于score的记录会被筛选出，默认为990。
            out_for_cytoscape (bool): 是否输出用于Cytoscape绘图的文件，默认为True。
            out_graph (bool): 是否输出基于ECharts的html格式的网络可视化图，默认为True。
            re (bool): 是否返回原始分析结果（中药、化合物（中药成分）、蛋白（靶点）及其连接信息）。
            path (str): 存放结果的目录。


        Returns:
            formula: 复方信息（仅在输入的tcm_or_formula为HVPID时返回）。
            formula_tcm_links: 复方-中药连接信息（仅在输入的tcm_or_formula为HVPID时返回）。
            tcm: 中药信息。
            tcm_chem_links: 中药-化合物（中药成分）连接信息。
            chem: 化合物（中药成分）信息。
            chem_protein_links: 化合物（中药成分）-蛋白（靶点）连接信息。
            proteins: 蛋白（靶点）信息。


        Examples:
            **From Formula**

            >>> from_tcm_or_formula(['HVP1625'])
            See more at : demo.ipynb

            **From TCM**

            >>> from_tcm_or_formula(['HVM0367', 'HVM1695'])
            See more at :demo

            **From Formula and Proteins**

            >>> from_tcm_or_formula(['HVP1625'],['ENSP00000381588', 'ENSP00000252519'], score=400)# medium confidence in STITCH
    """

    

    if tcm_or_formula_id[0][2] == 'P':  # 判断输入是否为复方的HVPID
        formula = get.get_formula('HVPID', tcm_or_formula_id)  # 获取该复方的信息
        formula_tcm_links = get.get_formula_tcm_links('HVPID', formula['HVPID'])
        tcm = get.get_tcm('HVMID', formula_tcm_links['HVMID'])
    else:
        formula = None
        formula_tcm_links = None
        tcm = get.get_tcm('HVMID', tcm_or_formula_id)

    tcm_chem_links = get.get_tcm_chem_links('HVMID', tcm['HVMID'])
    chem = get.get_chemicals('HVCID', tcm_chem_links['HVCID'])
    chem_protein_links = get.get_chem_protein_links('HVCID', chem['HVCID'], score)

    if proteins_id is None:
        proteins = get.get_proteins('Ensembl_ID', chem_protein_links['Ensembl_ID'])
    else:
        proteins = get.get_proteins('Ensembl_ID', proteins_id)

    # 深度优先搜索筛选有效节点
    formula, formula_tcm_links, tcm, tcm_chem_links, chem, chem_protein_links, proteins = dfs_filter(
        formula, formula_tcm_links, tcm, tcm_chem_links, chem, chem_protein_links, proteins)

    tcm, chem, formula = compute.score(tcm, tcm_chem_links, chem, chem_protein_links, formula, formula_tcm_links)

    if out_for_cytoscape:
        output.out_for_cyto(tcm, tcm_chem_links, chem, chem_protein_links, proteins, path)

    if out_graph:
        output.vis(tcm, tcm_chem_links, chem, chem_protein_links, proteins, path)

    if re:
        if tcm_or_formula_id[0][2] == 'P':
            return formula, formula_tcm_links, tcm, tcm_chem_links, chem, chem_protein_links, proteins
        else:
            return tcm, tcm_chem_links, chem, chem_protein_links, proteins


def from_proteins(proteins,
                  score=0,
                  random_state=None,
                  num=1000,
                  tcm_component=True,
                  formula_component=True,
                  out_for_cytoscape=True,
                  re=True,
                  path='result'):
    """
        进行逆向网络药理学分析

        Args:
            proteins: 任何可以使用in判断一个元素是否在其中的组合数据类型，存储拟分析蛋白（靶点）在STITCH中的Ensembl_ID。
            score (int): HerbiV_chemical_protein_links数据集中仅combined_score大于等于score的记录会被筛选出，默认为0。
            random_state (int): 指定优化模型使用的随机数种子。
            num (int):指定优化时需生成的解的组数。
            tcm_component (bool): 是否进行中药组合优化。
            formula_component (bool): 是否进行复方组合优化。
            out_for_cytoscape (bool): 是否输出用于Cytoscape绘图的文件。
            re (bool): 是否返回原始分析结果。
            path (str): 存放结果的目录。


        Returns:
            formula: 复方信息。
            formula_tcm_links: 复方-中药连接信息。
            tcm: 中药信息。
            tcm_chem_links: 中药-化合物（中药成分）连接信息。
            chem: 化合物（中药成分）信息。
            chem_protein_links: 化合物（中药成分）-蛋白（靶点）连接信息。
            proteins: 蛋白（靶点）信息。
            tcms: 包含优化模型得到的中药组合中各中药的ID、组合对疾病相关靶点集合的潜在作用、组合前后潜在作用的提升量。
            formulas: 包含优化模型得到的复方组合中各复方的ID、组合对疾病相关靶点集合的潜在作用、组合前后潜在作用的提升量。

        Examples:
            **From Proteins**

            进行优化
            >>> from_proteins(['ENSP00000381588', 'ENSP00000252519'],score=0,random_state=138192,num=100)
            See more at : demo.ipynb

            不进行优化
            >>> from_proteins(['ENSP00000381588', 'ENSP00000252519'],score=0,tcm_component=False,formula_component=False,out_for_cytoscape=False)
            See more at : demo.ipynb

    """


    proteins = get.get_proteins('Ensembl_ID', proteins)
    chem_protein_links = get.get_chem_protein_links('Ensembl_ID', proteins['Ensembl_ID'], score)

    # **新增的异常处理代码**
    if chem_protein_links.empty:
        raise ValueError(f"根据设定的score值（score={score}），没有找到符合条件的化合物-蛋白连接。请尝试降低score值以获取更多结果。")


    chem = get.get_chemicals('HVCID', chem_protein_links['HVCID'])
    tcm_chem_links = get.get_tcm_chem_links('HVCID', chem['HVCID'])
    tcm = get.get_tcm('HVMID', tcm_chem_links['HVMID'])
    formula_tcm_links = get.get_formula_tcm_links('HVMID', tcm['HVMID'])
    formula = get.get_formula('HVPID', formula_tcm_links['HVPID'])

    # 深度优先搜索筛选有效节点
    formula, formula_tcm_links, tcm, tcm_chem_links, chem, chem_protein_links, proteins = dfs_filter(
        formula, formula_tcm_links, tcm, tcm_chem_links, chem, chem_protein_links, proteins)

    # 计算Score
    tcm, chem, formula = compute.score(tcm, tcm_chem_links, chem, chem_protein_links, formula, formula_tcm_links)

    # 调用优化模型
    tcms = compute.component(tcm.loc[tcm['Importance Score'] != 1.0], random_state, num) if tcm_component else None
    formulas = compute.component(formula.loc[formula['Importance Score'] != 1.0],
                                 random_state, num) if formula_component else None

    if out_for_cytoscape:
        output.out_for_cyto(tcm, tcm_chem_links, chem, chem_protein_links, proteins, path)

    if re:
        return formula, formula_tcm_links, tcm, tcm_chem_links, chem, chem_protein_links, proteins, tcms, formulas


def dfs_filter(formula, formula_tcm_links, tcm, tcm_chem_links, chem, chem_protein_links, proteins):
    """
        深度优先搜索筛选有效节点（在完整的（复方-）中药-化合物-蛋白通路中的节点）

        Args:
            formula: 复方信息。
            formula_tcm_links: 复方-中药连接信息。
            tcm: 中药信息。
            tcm_chem_links:中药-化合物（中药成分）连接信息。
            chem: 化合物（中药成分）信息。
            chem_protein_links: 化合物（中药成分）-蛋白（靶点）连接信息。
            proteins: 蛋白（靶点）信息。


        Returns:
            formula: 复方信息。
            formula_tcm_links: 复方-中药连接信息。
            tcm: 中药信息。
            tcm_chem_links: 中药-化合物（中药成分）连接信息。
            chem: 化合物（中药成分）信息。
            chem_protein_links: 化合物（中药成分）-蛋白（靶点）连接信息。
            proteins: 蛋白（靶点）信息。


        Examples:
            **dfs_filter**

            # TODO: 待补充
            >>>


    """


    formula_id = set()
    tcm_id = set()
    chem_id = set()
    proteins_id = set()

    # 深度优先搜索得到有效节点的ID
    for f in formula['HVPID'] if (formula_tcm_links is not None) else [0]:
        for m in tcm['HVMID'] if (formula_tcm_links is None) else set(formula_tcm_links.loc[
                                                                        formula_tcm_links['HVPID'] == f]['HVMID']):
            for c in set(tcm_chem_links.loc[tcm_chem_links['HVMID'] == m]['HVCID']):
                for p in set(chem_protein_links.loc[chem_protein_links['HVCID'] == c]['Ensembl_ID']):
                    if p in proteins['Ensembl_ID'].tolist():
                        formula_id.add(f)
                        tcm_id.add(m)
                        chem_id.add(c)
                        proteins_id.add(p)

    # 根据有效节点的ID更新formula, formula_tcm_links, tcm, tcm_chem_links, chem, chem_protein_links, proteins
    formula = None if formula is None else formula.loc[formula['HVPID'].isin(formula_id)]
    tcm = tcm.loc[tcm['HVMID'].isin(tcm_id)]
    chem = chem.loc[chem['HVCID'].isin(chem_id)]
    proteins = proteins.loc[proteins['Ensembl_ID'].isin(proteins_id)]
    formula_tcm_links = None if formula_tcm_links is None else formula_tcm_links.loc[
        formula_tcm_links['HVPID'].isin(formula_id) & formula_tcm_links['HVMID'].isin(tcm_id)]
    tcm_chem_links = tcm_chem_links.loc[tcm_chem_links['HVMID'].isin(tcm_id) & tcm_chem_links['HVCID'].isin(chem_id)]
    chem_protein_links = chem_protein_links.loc[chem_protein_links['HVCID'].isin(chem_id) &
                                                chem_protein_links['Ensembl_ID'].isin(proteins_id)]

    # 重新编号（chem、tcm和formula在计算score时会重新编号，此处不再重新编号）
    tcm_chem_links.index = range(tcm_chem_links.shape[0])
    chem_protein_links.index = range(chem_protein_links.shape[0])
    proteins.index = range(proteins.shape[0])

    return formula, formula_tcm_links, tcm, tcm_chem_links, chem, chem_protein_links, proteins


if __name__ == '__main__':
    from_tcm_or_formula(['HVP1625'], ['ENSP00000381588', 'ENSP00000252519'], score=0)
    tcm_ft, tcm_chem_links_ft, chem_ft, chem_protein_links_ft, protein_ft = from_tcm_or_formula(['HVM0735'], )
    formula_ff, formula_tcm_links_ff, tcm_ff, tcm_chem_links_ff, chem_ff, chem_protein_links_ff, protein_ff = \
        from_tcm_or_formula(['HVP1625'], )
    formula_fg, tcm_fg, tcm_chem_l_fg, chem_fg, chem_protein_l_fg, protein_fg, tcms_fg, formulas_fg, proteins_fg = from_proteins(
        ['ENSP00000381588', 'ENSP00000252519'], num=3)
    # tcm_ftp, tcm_chem_links_ftp, chem_ftp, chem_protein_links_ftp, protein_ftp = \
    #     from_tcm_or_formula_proteins(['HVM0367', 'HVM1695'], ['ENSP00000381588', 'ENSP00000252519'])
    # formula_ffp, formula_tcm_links_ffp, tcm_ffp, tcm_chem_links_ffp, chem_ffp, chem_protein_links_ffp, protein_ffp = \
    #     from_tcm_or_formula_proteins(['HVP1625'], ['ENSP00000381588', 'ENSP00000252519'])
