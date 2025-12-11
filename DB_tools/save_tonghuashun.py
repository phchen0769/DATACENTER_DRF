import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import django
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 设置django环境，否则无法使用django的ORM
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "datacenter_drf.settings")
django.setup()


# 导入用户数据
from apps.finance.models import Dividend


# A股银行字典
BANKS_IN_STOCK_A = [
    {"code": "601398", "name": "工商银行"},
    {"code": "600036", "name": "招商银行"},
    {"code": "601288", "name": "农业银行"},
    {"code": "601988", "name": "中国银行"},
    {"code": "000001", "name": "平安银行"},
    {"code": "601939", "name": "建设银行"},
    {"code": "601166", "name": "兴业银行"},
    {"code": "601328", "name": "交通银行"},
    {"code": "600016", "name": "民生银行"},
    {"code": "601658", "name": "邮储银行"},
    {"code": "600919", "name": "江苏银行"},
    {"code": "601169", "name": "北京银行"},
    {"code": "601916", "name": "浙商银行"},
    {"code": "600000", "name": "浦发银行"},
    {"code": "603323", "name": "苏农银行"},
    {"code": "601009", "name": "南京银行"},
    {"code": "601998", "name": "中信银行"},
    {"code": "002142", "name": "宁波银行"},
    {"code": "601818", "name": "光大银行"},
    {"code": "600015", "name": "华夏银行"},
    {"code": "600926", "name": "杭州银行"},
    {"code": "601997", "name": "贵阳银行"},
    {"code": "601229", "name": "上海银行"},
    {"code": "600928", "name": "西安银行"},
    {"code": "601860", "name": "紫金银行"},
    {"code": "002936", "name": "郑州银行"},
    {"code": "601838", "name": "成都银行"},
    {"code": "601128", "name": "常熟银行"},
    {"code": "601528", "name": "瑞丰银行"},
    {"code": "001227", "name": "兰州银行"},
    {"code": "002807", "name": "江阴银行"},
    {"code": "002966", "name": "苏州银行"},
    {"code": "601963", "name": "重庆银行"},
    {"code": "601187", "name": "厦门银行"},
    {"code": "600908", "name": "无锡银行"},
    {"code": "002948", "name": "青岛银行"},
    {"code": "601665", "name": "齐鲁银行"},
    {"code": "601577", "name": "长沙银行"},
]

# 港股银行字典
BANKS_IN_STOCK_H = [
    {"code": "0939", "name": "建设银行"},
    {"code": "1398", "name": "工商银行"},
    {"code": "3968", "name": "招商银行"},
    {"code": "3988", "name": "中国银行"},
    {"code": "1288", "name": "农业银行"},
    {"code": "1658", "name": "邮储银行"},
    {"code": "1988", "name": "民生银行"},
    {"code": "0998", "name": "中信银行"},
    {"code": "3328", "name": "交通银行"},
    {"code": "2016", "name": "浙商银行"},
    {"code": "0011", "name": "恒生银行"},
    {"code": "6818", "name": "中国光大银行"},
    {"code": "3618", "name": "重庆农村商业银行"},
    {"code": "6199", "name": "贵州银行"},
    {"code": "3866", "name": "青岛银行"},
    {"code": "6196", "name": "郑州银行"},
    {"code": "0023", "name": "东亚银行"},
    {"code": "1963", "name": "重庆银行"},
    {"code": "3698", "name": "徽商银行"},
    {"code": "6138", "name": "哈尔滨银行"},
    {"code": "9889", "name": "东莞农商银行"},
    {"code": "1578", "name": "天津银行"},
    {"code": "9668", "name": "渤海银行"},
    {"code": "1916", "name": "江西银行"},
    {"code": "1551", "name": "广州农商银行"},
    {"code": "1216", "name": "中原银行"},
    {"code": "2066", "name": "盛京银行"},
    {"code": "2139", "name": "甘肃银行"},
    {"code": "2356", "name": "大新银行集团"},
    {"code": "6122", "name": "九台农商银行"},
    {"code": "6190", "name": "九江银行"},
    {"code": "1983", "name": "泸州银行"},
    {"code": "2596", "name": "宜宾银行"},
    {"code": "2558", "name": "晋商银行"},
    {"code": "9677", "name": "威海银行"},
]


# 保存单个分红信息到DRF中
def import_dividend(dividend):
    # 检查是否已存在相同记录
    existing = Dividend.objects.filter(
        stock_type=dividend["股票类型"],
        stock_code=dividend["股票代码"],
        announcement_date=dividend["公告日期"],
        ex_dividend_date=dividend["除净日"],
    ).first()

    if existing:
        print(
            f"记录已存在，跳过: {dividend['股票名称']} 公告日期: {dividend['公告日期']}"
        )
        return

    Dividend.objects.create(
        stock_type=dividend["股票类型"],
        stock_code=dividend["股票代码"],
        stock_name=dividend["股票名称"],
        announcement_date=dividend["公告日期"],
        ex_dividend_date=dividend["除净日"],
        dividend_before_tax=dividend["派息(税前)(元)"],
        payment_date=dividend["派息日"],
    )


# 日期字符串解析函数
def parse_date(date_str):
    """
    将日期字符串解析为 date 对象。如果为 '--'、空字符串或包含 '--'，则返回 None。
    """
    if not date_str or "--" in date_str or date_str.strip() == "":
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        try:
            return datetime.strptime(date_str, "%Y/%m/%d").date()
        except ValueError:
            return None


# A股银行分红数据提取
def extract_dividend_amount(dividend_text):
    """
    从分红方案文本中提取派息金额
    """
    # 匹配"X元"的模式，提取元前面的数字（例如：10派1.414元 -> 提取1.414）
    match = re.search(r"([\d\.]+)元", dividend_text)
    if match:
        # 将提取到的数字除以10，并保留3位小数
        return round(float(match.group(1)) / 10, 5)

    return dividend_text


def get_A_banks_dividend(stock_code, stock_name):
    """
    从同花顺网站获取指定A股的分红数据
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": f"https://basic.10jqka.com.cn/{stock_code}/",
    }

    url = f"https://basic.10jqka.com.cn/{stock_code}/bonus.html"
    print(f"正在访问: {url}")

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        # 尝试多种编码方式解决中文乱码问题
        encodings = ["utf-8", "gbk", "gb2312", "ISO-8859-1"]
        soup = None

        for encoding in encodings:
            try:
                response.encoding = encoding
                soup = BeautifulSoup(response.text, "lxml")
                # 检查是否还有乱码
                title = soup.title.string if soup.title else ""
                if "\ufffd" not in title and ("分红" in title or "权益分派" in title):
                    break
            except:
                continue

        # 如果还是有乱码，使用content自动检测
        if soup is None or "\ufffd" in soup.get_text():
            # 使用content自动检测编码
            soup = BeautifulSoup(response.content, "lxml")

        # 查找指定class的表格
        table = soup.find("table", class_="m_table m_hl mt15")
        if not table:
            print(f"未找到class为'm_table m_hl mt15'的表格")
            return pd.DataFrame()

        print("找到目标表格")

        data = []

        # 获取所有行
        rows = table.find_all("tr")
        if len(rows) < 2:
            print("表格行数不足")
            return pd.DataFrame()

        # 获取表头
        header_row = rows[0]
        header_cells = header_row.find_all(["td", "th"])
        header = [cell.get_text(strip=True) for cell in header_cells]
        print(f"表头: {header}")

        # 解析数据行
        for row in rows[1:]:
            cells = row.find_all(["td", "th"])
            cell_texts = [cell.get_text(strip=True) for cell in cells]

            if len(cell_texts) == len(header) and any(cell_texts):
                # 构造行数据字典
                row_data = dict(zip(header, cell_texts))
                print(f"解析到行数据: {row_data}")

                try:
                    # 提取关键信息 (A股字段)
                    announcement_date_text = row_data.get("实施公告日", "")
                    dividend_text = row_data.get("分红方案说明", "")
                    ex_dividend_date_text = row_data.get("A股除权除息日", "")
                    payment_date_text = row_data.get("派息日", "")

                    dividend_amount = extract_dividend_amount(dividend_text)
                    # 如果没有提取到分红金额，则设为空字符串
                    if dividend_amount is None:
                        dividend_amount = ""

                    record = {
                        "股票类型": "A股",
                        "股票代码": stock_code,
                        "股票名称": stock_name,
                        "公告日期": parse_date(announcement_date_text),
                        "除净日": parse_date(ex_dividend_date_text),
                        "派息(税前)(元)": dividend_amount,
                        "派息日": parse_date(payment_date_text),
                    }

                    import_dividend(record)

                except Exception as e:
                    print(f"处理行数据时出错: {e}")
                    print(f"行数据: {row_data}")

        print(f"解析到{stock_name}分红数据,行数：", len(data))
        return pd.DataFrame(data)

    except Exception as e:
        print(f"数据获取失败，错误类型：{type(e).__name__}, 详情：{str(e)}")
        import traceback

        traceback.print_exc()
        return pd.DataFrame()


def get_H_banks_dividend(stock_code, stock_name):
    """
    从同花顺网站获取指定H股的分红数据
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": f"https://basic.10jqka.com.cn/HK{stock_code}/",
    }

    url = f"https://basic.10jqka.com.cn/HK{stock_code}/bonus.html"
    print(f"正在访问: {url}")

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        # 尝试多种编码方式解决中文乱码问题
        encodings = ["utf-8", "gbk", "gb2312", "ISO-8859-1"]
        soup = None

        for encoding in encodings:
            try:
                response.encoding = encoding
                soup = BeautifulSoup(response.text, "lxml")
                # 检查是否还有乱码
                title = soup.title.string if soup.title else ""
                if "\ufffd" not in title and (
                    "分红" in title
                    or "权益分派" in title
                    or "分紅" in title
                    or "權益分派" in title
                ):
                    break
            except:
                continue

        # 如果还是有乱码，使用content自动检测
        if soup is None or "\ufffd" in soup.get_text():
            # 使用content自动检测编码
            soup = BeautifulSoup(response.content, "lxml")

        # 查找指定class的表格
        table = soup.find("table", class_="m_table m_hl mt15")
        if not table:
            print(f"未找到class为'm_table m_hl mt15'的表格")
            return pd.DataFrame()

        print("找到目标表格")

        data = []

        # 获取所有行
        rows = table.find_all("tr")
        if len(rows) < 2:
            print("表格行数不足")
            return pd.DataFrame()

        # 获取表头
        header_row = rows[0]
        header_cells = header_row.find_all(["td", "th"])
        header = [cell.get_text(strip=True) for cell in header_cells]
        print(f"表头: {header}")

        # 解析数据行
        for row in rows[1:]:
            cells = row.find_all(["td", "th"])
            cell_texts = [cell.get_text(strip=True) for cell in cells]

            if len(cell_texts) == len(header) + 1 and any(cell_texts):
                # 构造行数据字典
                row_data = dict(zip(header, cell_texts))
                print(f"解析到行数据: {row_data}")

                try:
                    # 只提取前4列的数据
                    # 提取关键信息 (H股字段)
                    announcement_date_text = row_data.get(
                        "公告日期", ""
                    ) or row_data.get("公布日期", "")
                    dividend_scheme = row_data.get("方案", "") or row_data.get(
                        "分紅方案", ""
                    )
                    ex_dividend_date_text = row_data.get("除净日", "") or row_data.get(
                        "除權日", ""
                    )
                    payment_date_text = row_data.get("派息日", "") or row_data.get(
                        "派息日期", ""
                    )

                    # 处理"方案"列的内容
                    dividend_amount = None
                    if dividend_scheme and "不分红" not in dividend_scheme:
                        # 检查是否包含"元"、"港元"或"港币"
                        if (
                            "元" in dividend_scheme
                            or "港元" in dividend_scheme
                            or "港币" in dividend_scheme
                        ):
                            # 提取数值，支持关键字前后都有数字的模式
                            # 例如：0.1港元，港币0.2，每股0.109361港元 等
                            # 匹配模式：数字+关键字 或 关键字+数字
                            match = re.search(
                                r"([\d\.]+)(?:元|港元|港币|人民币)|(?:元|港元|港币|人民币)([\d\.]+)",
                                dividend_scheme,
                            )
                            if match:
                                # 提取匹配到的数字（可能是组1或组2）
                                dividend_amount = float(
                                    match.group(1) or match.group(2)
                                )
                        else:
                            # 如果不包含"元"、"港元"或"港币"，则保留原始内容
                            dividend_amount = dividend_scheme

                    record = {
                        "股票类型": "H股",
                        "股票代码": stock_code,
                        "股票名称": stock_name,
                        "公告日期": parse_date(announcement_date_text),
                        "除净日": parse_date(ex_dividend_date_text),
                        "派息(税前)(元)": dividend_amount,
                        "派息日": parse_date(payment_date_text),
                    }

                    # 只有当派息金额有效时才导入
                    if record["派息(税前)(元)"] is not None:
                        import_dividend(record)
                        print("已保存分红数据：", record)
                        data.append(record)
                    else:
                        print(f"无效的分红金额，跳过该条记录。原始数据: {row_data}")

                except Exception as e:
                    print(f"处理行数据时出错: {e}")
                    print(f"行数据: {row_data}")

        print(f"解析到{stock_name}分红数据,行数：", len(data))
        return pd.DataFrame(data)

    except Exception as e:
        print(f"数据获取失败，错误类型：{type(e).__name__}, 详情：{str(e)}")
        import traceback

        traceback.print_exc()
        return pd.DataFrame()


def get_all_banks_bonus():
    """
    获取所有银行的分红数据
    """
    print("开始抓取所有A股银行的分红数据...")
    for bank in BANKS_IN_STOCK_A:
        print(f"正在抓取 {bank['name']} ({bank['code']}) 的分红数据...")
        get_A_banks_dividend(bank["code"], bank["name"])
        time.sleep(3)  # 避免请求过快被封IP

    print("开始抓取所有H股银行的分红数据...")
    for bank in BANKS_IN_STOCK_H:
        print(f"正在抓取 {bank['name']} ({bank['code']}) 的分红数据...")
        get_H_banks_dividend(bank["code"], bank["name"])
        time.sleep(3)  # 避免请求过快被封IP

    print("所有银行分红数据抓取完成！")


if __name__ == "__main__":
    # 如果需要获取所有银行数据，取消下面的注释
    get_all_banks_bonus()

    # 测试获取单个银行的分红数据
    # print("开始抓取民生银行(600016)的分红数据...")
    # get_A_banks_dividend("600016", "民生银行")
    # print("分红数据抓取完成！")
