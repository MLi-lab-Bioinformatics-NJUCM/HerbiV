import json
from json import JSONEncoder, dumps
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)


def check_tcm_id(hvmid: str) -> bool:
    """
    检查给定字符串是不是 HVMID
    :param hvmid: 给定字符串类型的 id
    :return: true - 是 HVMID
    """
    return hvmid.startswith("HVM") and len(hvmid) == 7


def check_formula_id(hvpid: str) -> bool:
    """
    检查给定字符串是不是 HVPID
    :param hvpid: 给定字符串类型的 id
    :return: true - 是 HVPID
    """
    return hvpid.startswith("HVP") and len(hvpid) == 7


def check_protein_id(ensembl_id: str) -> bool:
    """
    检查给定字符串是不是 ensembl_id
    :param ensembl_id: 给定字符串类型的 id
    :return: true - 是 ensembl_id
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
        json_str:
    Returns:
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
