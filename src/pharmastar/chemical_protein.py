import pandas as pd
import os


def get_chem_protein_links(genes,
                           filename='9606.protein_chemical.links.transfer.v5.0.tsv',
                           score=900):
    r"""
    读取STITCH数据库的protein_chemical数据集，返回包含目标基因且combined_score大于等于score的记录
    :param genes: 字典类型，存储拟分析蛋白（基因）在STITCH中的ID与其名称的对应关系
    :param filename: 字符串类型，从STITCH数据库中下载的protein_chemical.links.transfer的文件名
    :param score: int类型，仅combined_score大于等于score的记录会被筛选出
    :return: chem_protein_links_about_genes: pd.DataFrame类型，protein_chemical数据集中包含目标基因且combined_score大于等于score的记录
    """

    # 读取STITCH数据库的protein_chemical数据集
    path = 'data/' + filename
    chem_protein_links_all = pd.read_csv(path,
                                         sep='\t',
                                         usecols=['chemical', 'protein', 'combined_score'])

    # 选取chem_protein中protein为拟分析蛋白（基因）、化合物以CIDm编号、combined_score大于等于score的记录
    chem_protein_links_about_genes = chem_protein_links_all.loc[
        (chem_protein_links_all['protein'].isin(genes)) &
        (chem_protein_links_all['chemical'].str.match(r'CIDm.*?')) &
        (chem_protein_links_all['combined_score'] >= score)].copy()

    # 添加protein对应的基因名的列
    chem_protein_links_about_genes['protein_name_of_gene'] = chem_protein_links_about_genes[
        'protein'].apply(lambda x: genes.get(x))

    # 重新设置索引
    chem_protein_links_about_genes.index = range(chem_protein_links_about_genes.shape[0])

    return chem_protein_links_about_genes


def get_chem_to_protein(chem_protein_links_about_genes,
                        filename='chemicals.v5.0.tsv.gz',
                        chunksize=10000000,
                        screen=True):
    r"""
    从STITCH数据库中的chemicals数据集读取chem_protein_links_about_genes中化合物的名称和SMILES表达式，并导出chem_about_genes_info中化合物的SMILES表达式
    :param chem_protein_links_about_genes: pd.DataFrame类型，protein_chemical数据集中包含目标基因且combined_score大于等于score的记录
    :param filename: 字符串类型，从STITCH数据库中下载的chemicals数据集的文件名
    :param chunksize: int类型，pd.read_csv中的chunksize参数
    :param screen: boolean类型，是否筛选SMILES表达式长度小于等于200的记录
    :return: chem_protein_links_about_genes: pd.DataFrame类型，protein_chemical数据集中包含目标基因、combined_score大于等于score且SMILES表达式长度小于等于200（可选）的记录及化合物信息
    :return: chem_about_genes_info: pd.DataFrame类型，chem_protein_links_about_genes中化合物的名称和SMILES表达式
    """

    # 在chemicals.v5.0.tsv.gz数据集中提取出chem_protein_links_about_genes中化合物对应的记录
    # 构建迭代器
    path = 'data/' + filename
    chem_iterator = pd.read_csv(path,
                                sep='\t',
                                chunksize=chunksize,
                                usecols=['chemical', 'name', 'SMILES_string'])
    # 遍历chemicals数据集
    chem_about_genes_info = pd.DataFrame()
    n = '200' if screen else ''
    for chunk in chem_iterator:
        chem_iterator_chunk = chunk.loc[(chunk['chemical'].isin(chem_protein_links_about_genes['chemical'])) &
                                        (chunk['SMILES_string']).str.match(r'^.{0,' + n + '}$')]
        chem_about_genes_info = pd.concat([chem_about_genes_info, chem_iterator_chunk])

    # 将chem_about_genes_info通过内连接合并到chem_protein_links_about_genes中，
    # 并将列名name改为chemical_name以与protein_name_of_gene区分
    chem_protein_links_about_genes = chem_protein_links_about_genes.merge(chem_about_genes_info,
                                                                          on='chemical',
                                                                          how='left')
    chem_protein_links_about_genes.rename(columns={'name': 'chemical_name'}, inplace=True)

    # 导出chem_about_genes_info中化合物的SMILES表达式
    if not os.path.exists('result'):  # 若无result目录，先创建该目录
        os.mkdir('result')
    chem_about_genes_info['SMILES_string'].drop_duplicates().to_csv('result/smiles_to_SwissADME.txt',
                                                                    index=False,
                                                                    header=False)
    # 重新设置索引
    chem_protein_links_about_genes.index = range(chem_protein_links_about_genes.shape[0])
    chem_about_genes_info.index = range(chem_about_genes_info.shape[0])

    return chem_protein_links_about_genes, chem_about_genes_info


def get_chem_protein_links_with_cheminfo(
        genes,
        protein_chemical_links_filename='9606.protein_chemical.links.transfer.v5.0.tsv',
        score=900,
        chemicals_filename='chemicals.v5.0.tsv.gz',
        chunksize=10000000):
    r"""
    读取STITCH数据库的protein_chemical数据集和chemicals数据集，返回包含目标基因且combined_score大于等于score的记录及化合物信息，并导出chem_about_genes_info中化合物的SMILES表达式
    :param genes: 字典类型，存储拟分析蛋白（基因）在STITCH中的ID与其名称的对应关系
    :param protein_chemical_links_filename: 字符串类型，从STITCH数据库中下载的protein_chemical.links.transfer的文件名
    :param score: int类型，仅combined_score大于等于score的记录会被筛选出
    :param chemicals_filename: 字符串类型，从STITCH数据库中下载的chemicals数据集的文件名
    :param chunksize: int类型，pd.read_csv中的chunksize参数
    :return: chem_protein_links_about_genes: pd.DataFrame类型，protein_chemical数据集中包含目标基因、combined_score大于等于score且SMILES表达式长度小于等于200（可选）的记录及化合物信息
    :return: chem_about_genes_info: pd.DataFrame类型，protein_chemical数据集中包含目标基因且combined_score大于等于score的记录中化合物的名称和SMILES表达式
    """

    chem_protein_links_about_genes = get_chem_protein_links(genes,
                                                            protein_chemical_links_filename,
                                                            score)
    chem_protein_links_about_genes, chem_about_genes_info = get_chem_to_protein(chem_protein_links_about_genes,
                                                                                chemicals_filename, chunksize)
    return chem_protein_links_about_genes, chem_about_genes_info
