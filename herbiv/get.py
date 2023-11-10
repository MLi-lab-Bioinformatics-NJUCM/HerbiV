import os
import pandas as pd


def get_formula(by, items):
    """
        读取HerbiV_formula数据集，返回items中复方的信息。
        Read the HerbiV_formula dataset and return the information about the compound party in items.

        Args:
            by (str): 数据集中与items相匹配的列的列名。The column name of the column in the dataset that matches items.
            items (collections.abc.Iterable): 要查询的复方

        Returns:
            pandas.DataFrame: items中复方的信息。Information on compounding in items.

        Examples:
            >>> get_formula('HVPID', ['HVP1625'])
                 HVPID  ... Source Document
            0  HVP1625  ...   shang han lun
            [1 rows x 6 columns]

    """

    # 读取数据集
    formula_all = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + r'/data/HerbiV_formula.csv')

    # 在HerbiV_formula中获取items中复方的信息
    formula = formula_all.loc[formula_all[by].isin(items)].copy()

    # 重新设置索引
    formula.index = range(formula.shape[0])

    return formula


def get_formula_tcm_links(by, items):
    """
        读取HerbiV_formula_tcm_links数据集，返回items中复方/中药的复方-中药连接信息。

        Args:
            by (str): 数据集中与items相匹配的列的列名。
            items (collections.abc.Iterable): 要查询的复方/中药

        Returns:
            pandas.DataFrame: items中复方/中药的复方-中药连接信息。

        Examples:
            >>> get_formula_tcm_links('HVPID', ['HVP1625'])
                 HVPID    HVMID
            0  HVP1625  HVM0367
            1  HVP1625  HVM0735
            2  HVP1625  HVM0766
            3  HVP1625  HVM1695
            4  HVP1625  HVM3203
            5  HVP1625  HVM4463

    """

    # 读取数据集
    formula_tcm_links_all = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) +
                                        r'/data/HerbiV_formula_tcm_links.csv')

    # 在HerbiV_formula_tcm_links中获取items中复方/中药的复方-中药连接信息
    formula_tcm_links = formula_tcm_links_all.loc[formula_tcm_links_all[by].isin(items)].copy()

    # 重新设置索引
    formula_tcm_links.index = range(formula_tcm_links.shape[0])

    return formula_tcm_links


def get_tcm(by, items):
    """
            读取HerbiV_tcm数据集，返回items中中药的信息

            Args:
                by (str): str类型，数据集中与items相匹配的列的列名
                items (collections.abc.Iterable): 要查询的中药

            Returns:
                pandas.DataFrame: items中中药的信息

            Examples:
                >>> get_tcm('HVMID', ['HVM0367', 'HVM1695'])
                    HVMID cn_name  pinyin_name  ... TCM_ID_id SymMap_id TCMSP_id
                0  HVM0367      柴胡      CHAI HU  ...    3396.0      58.0     80.0
                1  HVM0735      大枣       DA ZAO  ...    1076.0      90.0    193.0
                2  HVM0766      党参    DANG SHEN  ...    1345.0      96.0    203.0
                3  HVM1695      黄芩    HUANG QIN  ...    6700.0     188.0    371.0
                4  HVM3203      生姜  SHENG JIANG  ...    7484.0     367.0    640.0
                [5 rows x 19 columns]
    """

    # 读取数据集
    tcm_all = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + r'/data/HerbiV_tcm.csv')

    # 在HerbiV_tcm中获取items中中药的信息
    tcm = tcm_all.loc[tcm_all[by].isin(items)].copy()

    # 重新设置索引
    tcm.index = range(tcm.shape[0])

    return tcm


def get_tcm_chem_links(by, items):

    """
            读取HerbiV_tcm_chemical_links数据集，返回items中中药/化合物的中药-成分信息

            Args:
                by (str): str类型，数据集中与items相匹配的列的列名
                items (collections.abc.Iterable): 要查询的中药/化合物

            Returns:
                pandas.DataFrame: items中中药/化合物的中药-成分信息

            Examples:
                >>> get_tcm_chem_links('HVMID', tcm_info['HVMID'])
                    HVMID    HVCID
            0     HVM0367  HVC0284
            1     HVM0367  HVC3018
            2     HVM0367  HVC0396
            3     HVM0367  HVC1371
            4     HVM0367  HVC1045

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

            Args:
                by (str): str类型，数据集中与items相匹配的列的列名
                items (collections.abc.Iterable): 要查询的化合物

            Returns:
                pandas.DataFrame: items中化合物的信息

            Examples:
                >>> get_chemicals('HVCID', tcm_chem_links_info['HVCID'])
                   HVCID                    Name  ...     STITCH_id     HERB_id
            0    HVC0018   p-hydroxybenzaldehyde  ...  CIDm00000126  HBIN010505
            1    HVC0026            acetaldehyde  ...  CIDm00000177  HBIN014388
            2    HVC0034               allantoin  ...  CIDm00000204  HBIN015193
            3    HVC0036                 glucose  ...  CIDm00000206  HBIN001003
            4    HVC0040                  ribose  ...  CIDm00000229  HBIN016558
            [5 rows x 8 columns]

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

            Args:
                by (str): str类型，数据集中与items相匹配的列的列名
                items (collections.abc.Iterable): 要查询的化合物/蛋白质
                score (int): int类型，仅combined_score大于等于score的记录会被筛选出，默认为900

            Returns:
                pandas.DataFrame: items中化合物/蛋白质的combined_score大于等于score的化合物-蛋白质（靶点）连接信息

            Examples:
                >>> get_chem_protein_links('HVCID', chem_info['HVCID'])
                    HVCID       Ensembl_ID  Combined_score
            0     HVC5547  ENSP00000297494           0.976
            1     HVC5538  ENSP00000206249           0.983
            2     HVC5538  ENSP00000343925           0.983
            3     HVC5512  ENSP00000260630           0.933
            4     HVC5512  ENSP00000369050           0.912

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



def get_proteins(by, items):
    """
                读取HerbiV_proteins数据集，返回items中蛋白质的信息

                Args:
                    by (str): str类型，数据集中与items相匹配的列的列名
                    items (collections.abc.Iterable): 要查询的蛋白质

                Returns:
                    pandas.DataFrame: items中蛋白质的信息

                Examples:
                    >>> get_proteins('Ensembl_ID', chem_protein_links_info['Ensembl_ID'])
                        Ensembl_ID  ...                     gene_name
                0     ENSP00000002165  ...  FUCA2 PSEC0151 UNQ227/PRO260
                1     ENSP00000013222  ...                          INMT
                2     ENSP00000014930  ...                     HEBP1 HBP
                3     ENSP00000023064  ...                   SLC7A9 BAT1
                4     ENSP00000043402  ...     RTN4R NOGOR UNQ330/PRO526
                [5 rows x 3 columns]

        """

    # 数据的输入
    current_directory = os.path.dirname(os.path.abspath(__file__))
    proteins_all = pd.read_csv(current_directory + r'/data/HerbiV_proteins.csv')

    # 在HerbiV_chemical_proteins中获取items中化合物的信息
    proteins = proteins_all.loc[proteins_all[by].isin(items)].drop_duplicates(subset=['Ensembl_ID'])

    # 重置索引
    proteins.index = range(proteins.shape[0])

    return proteins


def get_tcm_or_formula(tcm_or_formula):
    """
                    获取tcm_or_formula中元素对应的中药、复方及其连接信息

                    Args:
                        tcm_or_formula (collections.abc.Iterable): 要查询的中药或复方的ID

                    Returns:
                        pandas.DataFrame: tcm_or_formula中的复方信息
                        pandas.DataFrame: tcm_or_formula中的中药信息
                        pandas.DataFrame: tcm_or_formula中的复方-中药连接信息

                    Examples:
                        >>> get_tcm_or_formula(['HVP1625'])
                            HVPID  ... Source Document
                        0  HVP1625  ...   shang han lun
                        [1 rows x 6 columns]

            """

    if tcm_or_formula[0][2] == 'P':  # 判断输入是否为复方的HVPID
        formula = get_formula('HVPID', tcm_or_formula)
        formula_tcm_links = get_formula_tcm_links('HVPID', formula['HVPID'])
        tcm = get_tcm('HVMID', formula_tcm_links['HVMID'])
    else:
        formula = None
        formula_tcm_links = None
        tcm = get_tcm('HVMID', tcm_or_formula)
    return formula, tcm, formula_tcm_links


if __name__ == '__main__':
    formula_info = get_formula('HVPID', ['HVP1625'])
    formula_tcm_links_info = get_formula_tcm_links('HVPID', formula_info['HVPID'])
    tcm_info = get_tcm('HVMID', formula_tcm_links_info['HVMID'])
    tcm_chem_links_info = get_tcm_chem_links('HVMID', tcm_info['HVMID'])
    chem_info = get_chemicals('HVCID', tcm_chem_links_info['HVCID'])
    chem_protein_links_info = get_chem_protein_links('HVCID', chem_info['HVCID'])
    protein_info = get_proteins('Ensembl_ID', chem_protein_links_info['Ensembl_ID'])
    formula_info1, tcm_info1, formula_tcm_links_info1 = get_tcm_or_formula(['HVP1625'])
    formula_info2, tcm_info2, formula_tcm_links_info2 = get_tcm_or_formula(['HVM0367', 'HVM1695'])
