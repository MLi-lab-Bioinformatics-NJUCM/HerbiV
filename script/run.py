import json
import argparse

import utils
from herbiv import analysis
import warnings
# 消除 pandas Future Warning
warnings.simplefilter(action='ignore', category=FutureWarning)


def from_tcm(tcms: list[str]):
    """
    对中药分析
    :param tcms: 中药 id 列表, 如 ['HVM0367', 'HVM1695']
    :return: json 字符串
    """
    if not utils.check_id(tcms, utils.check_tcm_id):
        return json.dumps({'msg': 'Wrong TCM ID'})
    result = analysis.from_tcm_or_formula(tcms)
    tmp = []
    for e in result:
        tmp.append(utils.nan_converter(e))
    tcm, tcm_chem_links, chem, chem_protein_links, proteins = tmp

    return json.dumps({
        'tcm':               tcm.to_dict(orient='records'),
        'tcm_chem_link':     tcm_chem_links.to_dict(orient='records'),
        'chem':              chem.to_dict(orient='records'),
        'chem_protein_link': chem_protein_links.to_dict(orient='records'),
        'protein':           proteins.to_dict(orient='records')
    })


def from_formula(formulas: list[str]):
    """
    对复方分析
    :param formulas: 复方 id 列表, 如 ['HVP1625']
    :return: json 字符串
    """
    if not utils.check_id(formulas, utils.check_formula_id):
        assert False, "Wrong formula id"
    result = analysis.from_tcm_or_formula(formulas)
    formula, formula_tcm_links, tcm, tcm_chem_links, chem, chem_protein_links, proteins = result
    return json.dumps({
        'formula':            formula,
        'tcm':                tcm,
        'tcm_chem_links':     tcm_chem_links,
        'chem':               chem,
        'chem_protein_links': chem_protein_links,
        'proteins':           proteins,
    })


def from_tcm_proteins(tcms: list[str], proteins: list[str]):
    """
    给定中药和靶点分析（？）
    :param tcms:
    :param proteins:
    :return:
    """
    if not utils.check_id(tcms, utils.check_tcm_id):
        assert False, "Wrong TCM id"
    if not utils.check_id(proteins, utils.check_protein_id):
        assert False, "Wrong protein id"
    pass


def from_formula_proteins(formulas:list[str], proteins:list[str]):
    """
    给定复方和靶点分析
    :param formulas: 复方 id 列表，如 ['HVP1625']
    :param proteins: 靶点 id 列表，如 ['ENSP00000381588', 'ENSP00000252519']
    :return:
    """
    if not utils.check_id(formulas, utils.check_formula_id):
        assert False, "Wrong formula id"
    if not utils.check_id(proteins, utils.check_protein_id):
        assert False, "Wrong protein id"
    result = analysis.from_tcm_or_formula_proteins(formulas, proteins)
    formula, formula_tcm_links, tcm, tcm_chem_links, chem, chem_protein_links, proteins = result


# TODO
def from_proteins(proteins: list[str]):
    # 逆向网络药理学分析
    # 优化
    formula, formula_tcm_links, tcm, tcm_chem_links, chem, chem_protein_links, proteins, tcms, formulas = analysis.from_proteins(
        ['ENSP00000381588', 'ENSP00000252519'],
        score=0,
        random_state=138192,
        num=100)
    # 不优化
    formula, formula_tcm_links, tcm, tcm_chem_links, chem, chem_protein_links, proteins, tcms, formulas = analysis.from_proteins(
        ['ENSP00000381588', 'ENSP00000252519'],
        score=0,
        tcm_component=False,
        formula_component=False,
        out_for_cytoscape=False
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--function', choices=["tcm", "formula"], required=True, help='Functions')
    parser.add_argument('--tcms', nargs="+", type=str, help='TCM ids')
    parser.add_argument('--formulas', nargs="+", type=str, help='Formula ids')
    parser.add_argument('--proteins', nargs="+", type=str, help='Protein ids')
    args = parser.parse_args()

    if args.function == "tcm":
        print(from_tcm(args.tcms))
    elif args.function == "formula":
        print(from_formula(args.formulas))


if __name__ == '__main__':
    main()
