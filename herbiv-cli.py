#!/usr/bin/python3
import json
import argparse
import numpy as np
import pandas as pd
from herbiv import analysis
import warnings
# 消除 pandas Future Warning
# warnings.simplefilter(action='ignore', category=FutureWarning)
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
    return data.where((data.applymap(lambda x: True if str(x) != 'nan' else False)), None)


def from_tcm(tcms: list[str], score: int, path: str):
    """
    给定中药分析
    Args:
        tcms: 中药 id 列表, 如 ['HVM0367', 'HVM1695']
        score:
        path: 图像输出路径
    Returns:
    """
    if not check_id(tcms, check_tcm_id):
        return json.dumps({'msg': 'Wrong TCM ID'})
    result = analysis.from_tcm_or_formula(tcms, score=score, path=path)
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


def from_formula(formulas: list[str], score: int, path):
    """
    给定复方分析
    Args:
        formulas: 复方 id 列表, 如 ['HVP1625']
        score:
        path:     图像输出路径
    Returns:
    """
    if not check_id(formulas, check_formula_id):
        return json.dumps({'msg': 'Wrong formula ID'})
    result = analysis.from_tcm_or_formula(formulas, score=score, path=path)
    tmp = []
    for e in result:
        tmp.append(nan_converter(e))
    formula, formula_tcm_links, tcm, tcm_chem_links, chem, chem_protein_links, proteins = tmp
    return json.dumps({
        'formula':            formula.to_dict(orient='records'),
        'formula_tcm_links':  formula_tcm_links.to_dict(orient='records'),
        'tcm':                tcm.to_dict(orient='records'),
        'tcm_chem_links':     tcm_chem_links.to_dict(orient='records'),
        'chem':               chem.to_dict(orient='records'),
        'chem_protein_links': chem_protein_links.to_dict(orient='records'),
        'proteins':           proteins.to_dict(orient='records'),
    }, ensure_ascii=False)


def from_tcm_protein(tcms: list[str], proteins: list[str], score: int, path):
    """
    给定中药和靶点分析
    Args:
        tcms:     中药 id 列表，如 ['HVM0367', 'HVM1695']
        proteins: 靶点 id 列表，如 ['ENSP00000043402', 'ENSP00000223366']
        score:
        path:
    Returns:
    """
    if not check_id(tcms, check_tcm_id):
        return json.dumps({'msg': 'Wrong TCM ID'})
    if not check_id(proteins, check_protein_id):
        return json.dumps({'msg': 'Wrong protein ID'})
    result = analysis.from_tcm_or_formula(
        tcm_or_formula_id=tcms,
        proteins_id=proteins,
        path=path,
        score=score
    )
    tmp = []
    for e in result:
        tmp.append(nan_converter(e))
    tcm, tcm_chem_links, chem, chem_protein_links, proteins = tmp
    return json.dumps({
        'tcm': tcm.to_dict(orient='records'),
        'tcm_chem_link': tcm_chem_links.to_dict(orient='records'),
        'chem': chem.to_dict(orient='records'),
        'chem_protein_link': chem_protein_links.to_dict(orient='records'),
        'protein': proteins.to_dict(orient='records')
    }, ensure_ascii=False)


def from_formula_protein(formulas: list[str], proteins: list[str], score: int, path):
    """
    给定复方和靶点分析
    Args:
        formulas: 复方 id 列表，如 ['HVP1625']
        proteins: 靶点 id 列表，如 ['ENSP00000381588', 'ENSP00000252519']
        score:
        path:
    Returns:
    """
    if not check_id(formulas, check_formula_id):
        return json.dumps({'msg': 'Wrong formula ID'})
    if not check_id(proteins, check_protein_id):
        return json.dumps({'msg': 'Wrong protein ID'})
    result = analysis.from_tcm_or_formula(
        tcm_or_formula_id=formulas,
        proteins_id=proteins,
        path=path,
        score=score
    )
    tmp = []
    for e in result:
        tmp.append(nan_converter(e))
    formula, formula_tcm_links, tcm, tcm_chem_links, chem, chem_protein_links, proteins = tmp
    return json.dumps({
        'formula':            formula.to_dict(orient='records'),
        'formula_tcm_links':  formula_tcm_links.to_dict(orient='records'),
        'tcm':                tcm.to_dict(orient='records'),
        'tcm_chem_links':     tcm_chem_links.to_dict(orient='records'),
        'chem':               chem.to_dict(orient='records'),
        'chem_protein_links': chem_protein_links.to_dict(orient='records'),
        'proteins':           proteins.to_dict(orient='records'),
    }, ensure_ascii=False)


def from_protein(proteins: list[str], score: int, path):
    """
    逆向网络药理学分析
    Args:
        proteins: 靶点 id 列表，如 ['ENSP00000381588', 'ENSP00000252519']
        score:
        path:
    Returns:
    """
    if not check_id(proteins, check_protein_id):
        return json.dumps({'msg': 'Wrong protein ID'})
    # 优化
    result = analysis.from_proteins(
        proteins,
        score=score,
        random_state=138192,
        num=100,
        path=path
    )
    tmp = []
    for e in result:
        tmp.append(nan_converter(e))
    formula, formula_tcm_links, tcm, tcm_chem_links, chem, chem_protein_links, proteins, tcms, formulas = tmp
    return json.dumps({
        'formula':            formula.to_dict(orient='records'),
        'formula_tcm_links':  formula_tcm_links.to_dict(orient='records'),
        'tcm':                tcm.to_dict(orient='records'),
        'tcm_chem_links':     tcm_chem_links.to_dict(orient='records'),
        'chem':               chem.to_dict(orient='records'),
        'chem_protein_links': chem_protein_links.to_dict(orient='records'),
        'proteins':           proteins.to_dict(orient='records'),
        'tcms':               tcms.to_dict(orient='records'),
        'formulas':           formulas.to_dict(orient='records')
    }, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--function', "-f", choices=["tcm", "formula", "protein", "tcm_protein", "formula_protein"], required=True, help='Functions')
    parser.add_argument('--tcms', nargs="+", type=str, help='TCM ids')
    parser.add_argument('--formulas', nargs="+", type=str, help='Formula ids')
    parser.add_argument('--proteins', nargs="+", type=str, help='Protein ids')
    parser.add_argument('--path', "-p", type=str, help='Graph Output Path', default="result")
    parser.add_argument('--prettier', action='store_true', help='输出格式化的 json')
    parser.add_argument('--score', "-s", type=int, default=990, help='分数')
    args = parser.parse_args()

    if args.function == "tcm":
        print(from_tcm(args.tcms, args.score, args.path))
    elif args.function == "formula":
        print(from_formula(args.formulas, args.score, args.path))
    elif args.function == "tcm_protein":
        print(from_tcm_protein(args.tcms, args.proteins, args.score, args.path))
    elif args.function == "formula_protein":
        print(from_formula_protein(args.formulas, args.proteins, args.score, args.path))
    elif args.function == "protein":
        print(from_protein(args.proteins, args.score, args.path))


if __name__ == '__main__':
    main()
