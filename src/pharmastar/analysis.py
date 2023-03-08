from . import chemical_protein
from . import chemical
from . import chemical_herb
from . import output


def reverse(genes,
            protein_chemical_links_filename='9606.protein_chemical.links.transfer.v5.0.tsv',
            score=900,
            chemicals_filename='chemicals.v5.0.tsv.gz',
            chunksize=1000000,
            swiss_filename='swissadme.csv',
            drug_likeness_num=3,
            try_num=3):
    r"""
    进行反向网络药理学分析
    :param genes: 字典类型，存储拟分析蛋白（基因）在STITCH中的ID与其名称的对应关系
    :param protein_chemical_links_filename: 字符串类型，从STITCH数据库中下载的protein_chemical.links.transfer的文件名
    :param score: int类型，仅combined_score大于等于score的记录会被筛选出
    :param chemicals_filename: 字符串类型，从STITCH数据库中下载的chemicals数据集的文件名
    :param chunksize: int类型，遍历chemicals数据集时的chunksize，该值过大可能耗尽计算机的内存
    :param swiss_filename: SwissADME的分析结果（csv文件）的路径
    :param drug_likeness_num: int类型，筛选类药性指标时至少有多少个为Yes
    :param try_num: int类型，pubchempy重复尝试的次数
    """
    chem_protein_links_with_cheminfo, chem_about_genes_info = chemical_protein.get_chem_protein_links_with_cheminfo(
        genes,
        protein_chemical_links_filename,
        score,
        chemicals_filename,
        chunksize)

    s = "接下来将使用PubChem，请确认网络后按Enter键继续\nNext will use PubChem, please confirm your Internet and press Enter to continue"
    input(s)
    filtered_chem = chemical.adme_filter(chem_about_genes_info, swiss_filename, drug_likeness_num)
    washed_herb_ingredient = chemical.load_washed_herb_ingredient_info()
    herb_id_and_smiles = washed_herb_ingredient.loc[:, ['Ingredient_id', 'Ingredient_Smile']]
    filtered_chem = chemical.combine_herb_and_stitch_chemical_info(filtered_chem, herb_id_and_smiles, try_num)

    input("接下来将使用HERB，请确认网络后按Enter键继续\nNext will use HERB, please confirm your Internet and press Enter to continue")
    chem_herb = chemical_herb.get_herb_from_chem(filtered_chem)

    output.out_for_cytoscape(chem_herb, chem_protein_links_with_cheminfo)
