#!/usr/bin/python3
import json
import argparse
import numpy as np
import pandas as pd
from herbiv import analysis
import warnings
# 消除 pandas Future Warning
warnings.simplefilter(action='ignore', category=FutureWarning)

"""
HerbiV Command Line Interface
"""


# Utils
def check_tcm_id(hvmid: str) -> bool:
    """
    检查给定字符串是不是一个 HVMID
    Args:
        hvmid: 给定字符串类型的 id
    Returns: true - 是 HVMID
    """
    return hvmid.startswith("HVM") and len(hvmid) == 7


def check_formula_id(hvpid: str) -> bool:
    """
    检查给定字符串是不是 HVPID
    Args:
        hvpid: 给定字符串类型的 id
    Returns: true - 是 HVPID
    """
    return hvpid.startswith("HVP") and len(hvpid) == 7


def check_protein_id(ensembl_id: str) -> bool:
    """
    检查给定字符串是不是 ensembl_id
    Args:
        ensembl_id: 给定字符串类型的 id
    Returns: true - 是 ensembl_id
    """
    return ensembl_id.startswith("ENSP") and len(ensembl_id) == 15


def check_id(ids: list[str], check_fun) -> bool:
    if ids is None:
        return False
    for _id in ids:
        if not check_fun(_id):
            return False
    return True


def json_prettier(json_str: str):
    """
    输出格式化的 json 字符串
    Args:
        json_str: 未格式化的 json 字符串
    Returns: 格式化后的 json 字符串
    """
    _dict = json.loads(json_str)
    pretty_json = json.dumps(_dict, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
    print(pretty_json)


def nan_converter(data: pd.DataFrame):
    """
    为了解决 json 不支持 NaN 的问题，将 data 中的 NaN 转化为 None
    Args:
        data:
    Returns:
    """
    data.replace(np.nan, None, inplace=True)
    return data


def from_tcm(tcms: list[str], path: str):
    """
    给定中药分析
    Args:
        tcms: 中药 id 列表, 如 ['HVM0367', 'HVM1695']
        path: pyechart 图像输出路径
    Returns:
    """
    if not check_id(tcms, check_tcm_id):
        # should never be here
        return json.dumps({'msg': 'Wrong TCM ID'})
    result = analysis.from_tcm_or_formula(tcms, out_for_cytoscape=False, out_graph=True, path=path)
    tmp = []
    for e in result:
        tmp.append(nan_converter(e))
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
    给定复方分析
    Args:
        formulas: 复方 id 列表, 如 ['HVP1625']
    Returns:
    """
    if not check_id(formulas, check_formula_id):
        return json.dumps({'msg': 'Wrong formula ID'})
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


def from_tcm_protein(tcms: list[str], proteins: list[str]):
    """
    给定中药和靶点分析
    Args:
        tcms:     中药 id 列表，如 ['HVM0367', 'HVM1695']
        proteins: 靶点 id 列表，如 ['ENSP00000381588', 'ENSP00000252519']
    Returns:
    """
    if not check_id(tcms, check_tcm_id):
        assert False, "Wrong TCM id"
    if not check_id(proteins, check_protein_id):
        assert False, "Wrong protein id"
    pass


def from_formula_protein(formulas: list[str], proteins: list[str]):
    """
    给定复方和靶点分析
    Args:
        formulas: 复方 id 列表，如 ['HVP1625']
        proteins: 靶点 id 列表，如 ['ENSP00000381588', 'ENSP00000252519']
    Returns:
    """
    if not check_id(formulas, check_formula_id):
        assert False, "Wrong formula id"
    if not check_id(proteins, check_protein_id):
        assert False, "Wrong protein id"
    # result = analysis.from_tcm_or_formula_proteins(formulas, proteins)
    # formula, formula_tcm_links, tcm, tcm_chem_links, chem, chem_protein_links, proteins = result


def from_protein(proteins: list[str]):
    """
    逆向网络药理学分析
    Args:
        proteins: 靶点 id 列表，如 ['ENSP00000381588', 'ENSP00000252519']
    Returns:
    """
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
    parser.add_argument('--function', "-f", choices=["tcm", "formula", "protein", "tcm_protein", "formula_protein"], required=True, help='Functions')
    parser.add_argument('--tcms', nargs="+", type=str, help='TCM ids')
    parser.add_argument('--formulas', nargs="+", type=str, help='Formula ids')
    parser.add_argument('--proteins', nargs="+", type=str, help='Protein ids')
    parser.add_argument('--path', "-p", type=str, help='Graph Output Path', default="result")
    parser.add_argument('--prettier', action='store_true', help='输出格式化的 json')
    args = parser.parse_args()
    print(args.prettier)

    if args.function == "tcm":
        print(from_tcm(args.tcms, args.path))
    elif args.function == "formula":
        print(from_formula(args.formulas))
    elif args.function == "protein":
        print(from_protein(args.proteins))
    elif args.function == "tcm_protein":
        print()
    elif args.function == "formula_protein":
        print()


if __name__ == '__main__':
    main()


