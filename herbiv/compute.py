import numpy as np
import pandas as pd
from math import ceil
import random
from tqdm import tqdm


def score(tcm,
          tcm_chem_links,
          chem,
          chem_protein_links,
          formula=None,
          formula_tcm_links=None):
    """
    计算化合物和中药的Importance Score
    :param formula_tcm_links:
    :param formula:
    :param tcm: pd.DataFrame类型，中药信息
    :param tcm_chem_links: pd.DataFrame类型，中药-化合物（中药成分）连接信息
    :param chem: pd.DataFrame类型，化合物（中药成分）信息
    :param chem_protein_links: pd.DataFrame类型，化合物（中药成分）-蛋白质（靶点）连接信息
    :return: chem: pd.DataFrame类型，化合物的Importance Score的计算结果
    :return: tcm: pd.DataFrame类型，中药的Importance Score的计算结果
    """

    tcm_c = tcm.copy()
    chem_c = chem.copy()

    # 计算化合物的Importance Score
    chem_c['Importance Score'] = chem_c.loc[:, 'HVCID'].apply(
        lambda x: 1 - (
                1 - np.array([*chem_protein_links.loc[chem_protein_links['HVCID'] == x]['Combined_score']])).prod())

    # 计算中药的Importance Score
    tcm_c['Importance Score'] = tcm_c.loc[:, 'HVMID'].apply(
        lambda x: 1 - (1 - np.array([*chem_c.loc[
            chem_c['HVCID'].isin(tcm_chem_links.loc[tcm_chem_links['HVMID'] == x]['HVCID'])][
            'Importance Score']])).prod())

    # 若传入了复方相关信息，则需计算复方的Importance Score
    if formula is not None:
        formula_c = formula.copy()
        formula_c['Importance Score'] = formula_c.loc[:, 'HVPID'].apply(
            lambda x: 1 - (1 - np.array([*tcm_c.loc[
                tcm_c['HVMID'].isin(formula_tcm_links.loc[formula_tcm_links['HVPID'] == x]['HVMID'])][
                'Importance Score']])).prod())
        # 根据Importance Score降序排序
        formula_c = formula_c.sort_values(by='Importance Score', ascending=False)
        # 重新设置索引
        formula_c.index = range(formula_c.shape[0])
    else:
        formula_c = None

    # 根据Importance Score降序排序
    tcm_c = tcm_c.sort_values(by='Importance Score', ascending=False)

    # 重新设置索引
    tcm_c.index = range(tcm_c.shape[0])
    chem_c.index = range(chem_c.shape[0])

    return tcm_c, chem_c, formula_c


def component(items_and_score, random_state=None, num=1000, c=10):
    '''
    :param random_state:
    :param tcm:
    :param items_and_score: pd存储复方/中药信息
    :param num: 需要的解的组数
    :return:
    '''
    if 'HVPID' in items_and_score.columns:
        by = 'HVPID'
        name = 'name'
    else:
        by = 'HVMID'
        name = 'cn_name'

    dps = []
    items_ls = []
    n = len(items_and_score)
    weights = [1 for _ in range(n)]
    names = [*items_and_score.loc[:, by]]
    values = [*items_and_score.loc[:, 'Importance Score']]
    n = ceil(len(weights) / 10)

    if random_state is not None:
        random.seed(random_state)

    for _ in tqdm(range(num)):
        random_indices = random.sample(range(len(weights)), n)
        weights = [weights[i] for i in random_indices]
        names = [names[i] for i in random_indices]
        values = [values[i] for i in random_indices]

        # 不能再得出之前的解
        dp, items = knapsack(weights, n, items_ls, names, values, c)
        dps.append(dp)
        items_ls.append(items)

    # 用pd.DataFrame存储结果
    components = pd.DataFrame(dps)
    components.columns = ['Importance Score']
    components["items"] = items_ls
    components["items"] = components["items"].apply(lambda x: ';'.join(x))
    components = components.loc[:, ['items', 'Importance Score']]

    # 计算Score的提升量
    components['Boost'] = components.apply(boost, axis=1, args=(items_and_score, by))

    #components.loc[:, 'items'] = components.loc[:, 'items'].apply(
        #lambda x: ';'.join([str(items_and_score.loc[items_and_score[by] == x][name].iloc[0]) for x in x.split(';')]))

    # 根据boost降序排序
    components = components.sort_values(by='Boost', ascending=False)
    # 重新设置索引
    components.index = range(components.shape[0])

    return components


def boost(row, items_and_score, by):
    ls = row['items'].split(';')
    scores = [*items_and_score.loc[items_and_score[by].isin(ls)]['Importance Score']]
    return (row['Importance Score'] - max(scores))/max(scores)


def knapsack(weights, n, forbidden_combinations, names, values, c=10):
    # 创建一个二维列表用于存储计算结果
    dp = [[0] * (c + 1) for _ in range(n + 1)]
    # 创建一个二维列表用于记录选择的中药/复方
    items = [[""] * (c + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, c + 1):
            if weights[i - 1] <= j:
                # 检查当前是否与禁止组合冲突
                conflict = False
                for combination in forbidden_combinations:
                    if names[i - 1] in combination and any(
                            item in items[i - 1][j - weights[i - 1]] for item in combination):
                        conflict = True
                        break
                if conflict:
                    dp[i][j] = dp[i - 1][j]
                    items[i][j] = items[i - 1][j]
                else:
                    if 1 - (1 - values[i - 1]) * (1 - dp[i - 1][j - weights[i - 1]]) > dp[i - 1][j]:
                        dp[i][j] = 1 - (1 - values[i - 1]) * (1 - dp[i - 1][j - weights[i - 1]])
                        items[i][j] = names[i - 1] + ", " + items[i - 1][j - weights[i - 1]]
                    else:
                        dp[i][j] = dp[i - 1][j]
                        items[i][j] = items[i - 1][j]
            else:
                dp[i][j] = dp[i - 1][j]
                items[i][j] = items[i - 1][j]

    # 优化中药/复方存储
    items = [s[:-2] for s in items[-1]]

    # 计算累计Score比例
    score_ratio = np.cumsum(dp[-1]) / np.sum(dp)

    # 最大似然估计
    mle_estimates = (score_ratio - 1 / len(score_ratio)) / np.sqrt(2 / len(score_ratio))

    # 应选择的复方/中药数（即索引）但不能只选择一个
    num_components = np.argmin(mle_estimates) + 1
    num_components = 2 if num_components <= 1 else num_components

    return dp[-1][num_components], items[num_components].split(', ')


if __name__ == '__main__':
    import get

    protein_info = get.get_proteins('Ensembl_ID', ['ENSP00000381588', 'ENSP00000252519'])
    chem_protein_links_info = get.get_chem_protein_links('Ensembl_ID', protein_info['Ensembl_ID'], 0)
    chem_info = get.get_chemicals('HVCID', chem_protein_links_info['HVCID'])
    tcm_chem_links_info = get.get_tcm_chem_links('HVCID', chem_info['HVCID'])
    tcm_info = get.get_tcm('HVMID', tcm_chem_links_info['HVMID'])
    formula_tcm_links_info = get.get_formula_tcm_links('HVMID', tcm_info['HVMID'])
    formula_info = get.get_formula('HVPID', formula_tcm_links_info['HVPID'])

    tcm_info, chem_info, formula_info = score(tcm_info,
                                              tcm_chem_links_info,
                                              chem_info,
                                              chem_protein_links_info,
                                              formula_info,
                                              formula_tcm_links_info)
    tcms = component(tcm_info.loc[tcm_info['Importance Score'] != 1.0], random_state=138192, c=2)
    formulas = component(formula_info.loc[formula_info['Importance Score'] != 1.0], random_state=138192, c=5)