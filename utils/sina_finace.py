import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_ccb_dividend():
    """专业级新浪财经分红数据抓取函数"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://finance.sina.com.cn/",
    }

    # A股获取链接
    url = "https://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/601939.phtml"
    # H股获取链接
    # url = "https://stock.finance.sina.com.cn/hkstock/dividends/00939.html"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        if response.encoding == "ISO-8859-1":
            response.encoding = "gb2312"

        soup = BeautifulSoup(response.text, "lxml")

        table = soup.find("table", id="sharebonus_1")

        if not table:
            print("未找到分红表格，建议手动检查页面结构。")
            print(f"你可以在终端运行：$BROWSER {url}")
            return pd.DataFrame()

        columns = [th.get_text(strip=True) for th in table.select("tr th")]
        print("解析到的表头：", columns)

        data = []
        for row in table.select("tbody tr"):
            cells = [td.get_text(strip=True) for td in row.select("td")]
            # 过滤空行
            print(cells)
            pass

            if len(cells) == len(columns):
                row_dict = dict(zip(columns, cells))
                try:
                    record = {
                        "公告日期": row_dict.get("公告日期"),
                        "进度": row_dict.get("进度"),
                        "除权除息日": row_dict.get("除权除息日"),
                        "股权登记日": row_dict.get("股权登记日"),
                        "分红方案(每10股)": row_dict.get("分红方案(每10股)"),
                        "派息(税前)(元)": row_dict.get("派息(税前)(元)"),
                    }
                    data.append(record)
                except Exception as e:
                    print("解析某行数据失败：", row_dict, e)

        print("解析到的数据行数：", len(data))
        if data:
            print("首行数据：", data[0])

        df = pd.DataFrame(data)
        if "公告日期" not in df.columns:
            print("DataFrame实际列名：", df.columns.tolist())
            return pd.DataFrame()
        df["公告日期"] = pd.to_datetime(df["公告日期"], errors="coerce")
        df = df.dropna(subset=["公告日期"])

        return df.sort_values("公告日期", ascending=False)

    except Exception as e:
        print(f"数据获取失败，错误类型：{type(e).__name__}, 详情：{str(e)}")
        return pd.DataFrame()


if __name__ == "__main__":
    df = get_ccb_dividend()
    if not df.empty:
        print("建设银行最新3次分红记录：")
        print(df.head(3).to_markdown(index=False))
    else:
        print("未获取到有效分红数据，请检查网络或页面结构")
