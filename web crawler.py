import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
# 定義URL模板
url_template = "https://gra206.aca.ntu.edu.tw/classrm/index.php/acarm/webcr-use1-new?Type=1&page={}&SYearDDL=1112&BuildingDDL=%25&Week={}&Capacity=1&SelectButton=%E6%9F%A5%E8%A9%A2"

# 定義要爬取的頁數範圍
start_page = 1
end_page = 102
start_week=1
end_week=5
df = pd.DataFrame()
df = pd.DataFrame(columns=['name','col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'col8', 'col9', 'col10', 'col11', 'col12', 'col13', 'col14', 'col15','col16','peo'])

for Week in range(start_week,end_week+1):
# 迭代爬取每個頁面
    for page in range(start_page, end_page + 1):
        # 生成當前頁面的URL
        url = url_template.format(page, Week)

        # 發送請求並獲取網頁內容
        response = requests.get(url)
        html_content = response.text

        # 使用BeautifulSoup解析HTML內容
        soup = BeautifulSoup(html_content, "html.parser")

        # 找到表格元素
        table = soup.find("table", {"id": "ClassTimeGV"})

        # 定義字典以存儲每行的數據
        data = {}

        for row in table.find_all("tr"):
            cells = row.find_all("td")

            # 刪除表格中的頁數
            if len(cells) == 1:
                course_name = cells[0].text.strip()
                continue

            # 遍歷表格單元格
            for i, cell in enumerate(cells):
                if cell.find("br") is not None and "人" in cell.text:
                    cell_str = str(cell)
                    # 使用正則表達式抓取資料(拆分教室名稱和人數)
                    pattern_name = r'title="([^"]+)&lt;br'
                    matches_name = re.search(pattern_name, cell_str)
                    
                    if matches_name:
                        name = matches_name.group(1)
                        data['name'] = name
                    pattern_count = r'br\s*/&gt;([^人]+)'
                    matches_count = re.search(pattern_count, cell_str)

                    if matches_count:
                        count = matches_count.group(1)
                        data['peo'] = count
            #尋找課表            
            for i, cell in enumerate(cells):
                cell_value = cell.text.strip()
                data[f'col{i+1}'] = cell_value
                    
                if (i+1) % 16 == 0:
                    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
                    data = {}

