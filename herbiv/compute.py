import numpy as np
import pandas as pd
from typing import Union
from math import ceil
import random
from tqdm import tqdm


def score(tcm: pd.DataFrame,
          tcm_chem_links: pd.DataFrame,
          chem: pd.DataFrame,
          chem_protein_links: pd.DataFrame,
          formula: Union[pd.DataFrame, None] = None,
          formula_tcm_links: Union[pd.DataFrame, None] = None,
          weights: Union[dict, None] = None) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
        计算复方、中药和化合物的HerbiV Score。

        Args:
            tcm: 要计算HerbiV Score的中药的信息，格式与get.get_tcm的返回值相同。
            tcm_chem_links: tcm和chem中的中药-成分（化合物）连接信息。
            chem: 要计算HerbiV Score的化合物的信息，格式与get.get_chemicals的返回值相同。
            chem_protein_links: chem和拟分析靶点（蛋白）的化合物（中药成分）-蛋白质（靶点）连接信息。
            formula: 要计算HerbiV Score的复方信息，格式与get.get_formulas的返回值相同。默认为None。
            formula_tcm_links: formula和tcm中的复方-中药连接信息。默认为None。
            weights: 各靶点（蛋白）的权重，各权重的和应为1。默认为None，计算时将自动替换为相等的值。

        Returns:
            包含HerbiV Score的复方、中药和成分（化合物）的信息。

            tcm_and_score: 中药信息及HerbiV Score。
            chem_and_score: 成分（化合物）信息及HerbiV Score。
            formula_and_score: 复方信息及HerbiV Score。

        Examples:
            >>> from herbiv import get
            >>> protein_info = get.get_proteins('Ensembl_ID', ['ENSP00000381588', 'ENSP00000252519'])
            >>> chem_protein_links_info = get.get_chem_protein_links('Ensembl_ID', protein_info['Ensembl_ID'], 0)
            >>> chem_info = get.get_chemicals('HVCID', chem_protein_links_info['HVCID'])
            >>> tcm_chem_links_info = get.get_tcm_chem_links('HVCID', chem_info['HVCID'])
            >>> tcm_info = get.get_tcm('HVMID', tcm_chem_links_info['HVMID'])
            >>> formula_tcm_links_info = get.get_formula_tcm_links('HVMID', tcm_info['HVMID'])
            >>> formula_info = get.get_formula('HVPID', formula_tcm_links_info['HVPID'])
            >>> tcm_info, chem_info, formula_info = score(tcm_info,\
                                              tcm_chem_links_info,\
                                              chem_info,\
                                              chem_protein_links_info,\
                                              formula_info,\
                                              formula_tcm_links_info)
            >>> tcm_info
                    HVMID cn_name  ... ENSP00000252519 HerbiV Score Importance Score
            0     HVM2997     肉苁蓉  ...                     0.984882         0.991978
            1     HVM3101     沙苑子  ...                     0.995344         0.974194
            2     HVM3090      沙棘  ...                     0.958420         0.972441
            3     HVM2859      荞麦  ...                     0.955032         0.971191
            4     HVM4195     薏苡仁  ...                     0.984882         0.962036
            ...       ...     ...  ...                          ...              ...
            1266  HVM2206      硫磺  ...                     0.000000         0.075000
            1267  HVM1035   防己叶菝葜  ...                     0.000000         0.075000
            1268  HVM1509    红三叶草  ...                     0.000000         0.075000
            1269  HVM2625    南蛇藤根  ...                     0.000000         0.075000
            1270  HVM3202     生槐角  ...                     0.000000         0.075000
            [1271 rows x 22 columns]
            >>> chem_info
                   HVCID            Name  ... ENSP00000252519 HerbiV Score Importance Score
            0    HVC0385       captopril  ...                        0.989           0.4945
            1    HVC0689     aldosterone  ...                        0.883           0.4415
            2    HVC0036         glucose  ...                        0.865           0.4325
            3    HVC2094           Zn(II  ...                        0.854           0.4270
            4    HVC0208          chitin  ...                        0.854           0.4270
            ..       ...             ...  ...                          ...              ...
            181  HVC5481       genistein  ...                        0.000           0.0750
            182  HVC3501      triterpene  ...                        0.000           0.0750
            183  HVC0414    cyclosporine  ...                        0.000           0.0750
            184  HVC0359  benzo(a)pyrene  ...                        0.000           0.0750
            185  HVC6130        selenium  ...                        0.000           0.0750
            [186 rows x 11 columns]
            >>> formula_info
                    HVPID    name  ... ENSP00000252519 HerbiV Score Importance Score
            0     HVP2511     独活汤  ...                     0.999999         1.000000
            1     HVP1969   人参羌活散  ...                     0.999998         0.999999
            2     HVP0344  十二味正气散  ...                     0.999998         0.999999
            3     HVP3338   益气养元丸  ...                     0.999994         0.999997
            4     HVP0929     全痘汤  ...                     0.999994         0.999997
            ...       ...     ...  ...                          ...              ...
            5879  HVP3479     灵砂丹  ...                     0.000000         0.075000
            5880  HVP2284     硫黄膏  ...                     0.000000         0.075000
            5881  HVP4321     虾蟆散  ...                     0.000000         0.075000
            5882  HVP1083   治疥内消散  ...                     0.000000         0.075000
            5883  HVP4643     黄蜡丸  ...                     0.000000         0.075000
            [5884 rows x 9 columns]
    """
    formula_and_score = None
    if formula is not None:
        formula_and_score = formula.copy()
    tcm_and_score = tcm.copy()
    chem_and_score = chem.copy()

    proteins_id = chem_protein_links['Ensembl_ID'].unique()

    # 计算与各蛋白对应的HerbiV Score
    for protein in proteins_id:

        # 计算每一个化合物的HerbiV Score
        chem_and_score[protein + ' HerbiV Score'] = chem.loc[:, 'HVCID'].apply(lambda x: 1 - (1 - np.array(
            [*chem_protein_links.loc[(chem_protein_links['HVCID'] == x) &
                                     (chem_protein_links['Ensembl_ID'] == protein)]['Combined_score']])
                                                                                              ).prod()
                                                                               )

        # 计算各中药的HerbiV Score
        tcm_and_score[protein + ' HerbiV Score'] = tcm.loc[:, 'HVMID'].apply(lambda x: 1 - (1 - np.array(
            [*chem_and_score.loc[chem_and_score['HVCID'].isin(
                tcm_chem_links.loc[tcm_chem_links['HVMID'] == x]['HVCID'])][protein + ' HerbiV Score']])
                                                                                            ).prod()
                                                                             )

        # 若传入了复方相关信息，则还需计算各复方的HerbiV Score
        if formula is not None:
            formula_and_score[protein + ' HerbiV Score'] = formula.loc[:, 'HVPID'].apply(lambda x: 1 - (1 - np.array(
                [*tcm_and_score.loc[tcm_and_score['HVMID'].isin(
                    formula_tcm_links.loc[formula_tcm_links['HVPID'] == x]['HVMID'])][protein + ' HerbiV Score']])
                                                                                                        ).prod()
                                                                                         )

    # TODO: 验证各权重的和是否为靶点（蛋白）的总数或和为1。若权重为小数，则需要据此计算权重。
    # 若使用默认权重，则权重默认均为1
    if weights is None:
        weights = {col: 1 for col in [protein + ' HerbiV Score' for protein in proteins_id]}

    # TODO: 将所有Importance Score替换为HerbiV Score
    # 加权计算各复方、中药、成分（化合物）的HerbiV Score
    if formula is not None:
        formula_and_score['Importance Score'] = (formula_and_score[list(weights.keys())] * pd.Series(weights)).mean(axis=1)
    tcm_and_score['Importance Score'] = (tcm_and_score[list(weights.keys())] * pd.Series(weights)).mean(axis=1)
    chem_and_score['Importance Score'] = (chem_and_score[list(weights.keys())] * pd.Series(weights)).mean(axis=1)

    # 根据Importance Score降序排序
    if formula is not None:
        formula_and_score = formula_and_score.sort_values(by='Importance Score', ascending=False)
    tcm_and_score = tcm_and_score.sort_values(by='Importance Score', ascending=False)
    chem_and_score = chem_and_score.sort_values(by='Importance Score', ascending=False)

    # 重新设置索引
    if formula is not None:
        formula_and_score.index = range(formula_and_score.shape[0])
    tcm_and_score.index = range(tcm_and_score.shape[0])
    chem_and_score.index = range(chem_and_score.shape[0])

    return tcm_and_score, chem_and_score, formula_and_score


def component(items_and_score, random_state=None, num=1000, c=10):
    """
    :param random_state:
    :param tcm:
    :param items_and_score: pd存储复方/中药信息
    :param num: 需要的解的组数
    :return:
    """
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