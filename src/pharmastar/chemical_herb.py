from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
import time


def get_herb_from_chem(filtered_chem, waiting_time=30):
    r"""
    获取HERB数据库中filtered_chem中化合物及其对应的中药
    :param filtered_chem: pd.DataFrame类型，包含经过ADME过滤后的化合物的CID、名称、SMILES表达式和Ingredient_id
    :param waiting_time: int类型，获取items数失败后的等待时间（秒）
    :return chem_herb: pd.DataFrame类型，包含filtered_chem中化合物的名称、STITCH数据库中的CID和HERB数据库中对应的中药
    """
    # 设置为无界面
    options = Options()
    options.add_argument('--headless')

    # 禁止图片
    options.add_argument('blink-settings=imagesEnabled=false')

    # 初始化浏览器
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    # 建立存储化合物-中药关系的数据框chem_herb
    chem_herb = pd.DataFrame()
    for ingredient_id in tqdm(filtered_chem['Ingredient_id']):
        # 提取当前ingredient_id对应的化合物名称和STITCH数据库中的CID
        chem_name = filtered_chem.loc[filtered_chem['Ingredient_id'] == ingredient_id]['name'].all()
        cid = filtered_chem.loc[filtered_chem['Ingredient_id'] == ingredient_id]['chemical'].all()

        # 生成当前化合物在HERB数据库中对应的url
        url = 'http://herb.ac.cn/Detail/?v=' + ingredient_id + '&label=Ingredient'

        # 获取该网页
        driver.get(url)

        # 解析网页
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 获取当前url中Related Herbs的items数
        # 部分网页有较多的可交互元素，需较长时间来加载，如HBIN040799
        if get_items(soup) is None:
            time.sleep(waiting_time)
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # 部分网页无可用的信息，无法获取items数，需要跳过，如HBIN001054
            if get_items(soup) is None:
                continue

        for i in range(get_items(soup) // 5 + 1):  # Related Herbs的表格可能有多页，根据items数计算需点击下一页的次数
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            for sibling in soup.main.div.div.h3.next_siblings:
                if sibling.h4 is None:
                    continue
                else:
                    if sibling.h4.string == 'Related Herbs':  # 定位Related Herbs所在的标签
                        for child in sibling.ul:  # 定位Next Page所在的标签并获取其Xpath
                            if child.attrs.get('title') == 'Next Page':
                                xpath = xpath_soup(child)

                        for child in sibling.tbody.children:
                            # 将当前化合物的名称、STITCH数据库中的CID和网页中Related Herbs中的Herb Chinese name存储到chem_herb中
                            if child.contents[2].string != 'NA':
                                one_chem_herb = pd.DataFrame({'name': [chem_name],
                                                              'herb': [child.contents[2].string],
                                                              'CID': [cid]})
                                chem_herb = pd.concat([chem_herb, one_chem_herb])

            # 点击下一页
            click = driver.find_element_by_xpath(xpath)
            click.click()

    # 关闭浏览器
    driver.close()

    # 删除重复值并重新设置索引
    chem_herb = chem_herb.drop_duplicates()
    chem_herb.index = range(chem_herb.shape[0])

    return chem_herb


def get_items(soup):
    r"""
    获取soup对应的网页中Related Herbs的items数
    :param soup: bs4.BeautifulSoup类，经BeautifulSoup解析后的网页
    :return items: int类型，soup对应的网页中Related Herbs的items数；若无法获取到，则返回None
    """
    try:
        for sibling in soup.main.div.div.h3.next_siblings:
            if sibling.h4 is None:
                continue
            else:
                if sibling.h4.string == 'Related Herbs':
                    items = int(sibling.ul.li.string[:-6])
                    return items
    except:
        return None


def xpath_soup(element):
    # type: (typing.Union[bs4.element.Tag, bs4.element.NavigableString]) -> str
    r"""
    Generate xpath from BeautifulSoup4 element.
    From https://gist.github.com/ergoithz/6cf043e3fdedd1b94fcf
    :param element: BeautifulSoup4 element.
    :type element: bs4.element.Tag or bs4.element.NavigableString
    :return: xpath as string
    :rtype: str
    Usage
    -----
    >>> import bs4
    >>> html = (
    ...     '<html><head><title>title</title></head>'
    ...     '<body><p>p <i>1</i></p><p>p <i>2</i></p></body></html>'
    ...     )
    >>> soup = bs4.BeautifulSoup(html, 'html.parser')
    >>> xpath_soup(soup.html.body.p.i)
    '/html/body/p[1]/i'
    >>> import bs4
    >>> xml = '<doc><elm/><elm/></doc>'
    >>> soup = bs4.BeautifulSoup(xml, 'lxml-xml')
    >>> xpath_soup(soup.doc.elm.next_sibling)
    '/doc/elm[2]'
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:  # type: bs4.element.Tag
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name if 1 == len(siblings) else '%s[%d]' % (
                child.name,
                next(i for i, s in enumerate(siblings, 1) if s is child)
            )
        )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)
