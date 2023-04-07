from . import chemical_protein
from . import chemical
from . import tcm_chemical
from . import tcm
from . import output


def reverse(genes,
            score=900,
            save=True,
            path='result/'):
    r"""
    进行逆向网络药理学分析
    :param genes: 字典类型，存储拟分析蛋白（基因）在STITCH中的ID与其名称的对应关系
    :param score: int类型，仅combined_score大于等于score的记录会被筛选出
    :param save: 布尔类型，是否保存原始分析结果
    :param path: 字符串类型，存放结果的目录
    """

    chem_protein_links = chemical_protein.get_chem_protein_links(genes, score, save)

    chem = chemical.get_chemicals(chem_protein_links, save)

    tcm_chem_links = tcm_chemical.get_tcm_chem_links(chem, save)

    cm = tcm.get_tcm(tcm_chem_links, save)

    output.out_for_cyto(chem_protein_links, chem, genes, tcm_chem_links, cm, path)

    return cm
