import camelot
import pandas as pd
tables = camelot.read_pdf('xxx.pdf')
# tables.export('camelot_hhh.csv', f='csv', compress=True) # json, excel, html, markdown, sqlite
# tables.export('camelot_json', f='json', compress=True) # json, excel, html, markdown, sqlite

# 使用 ExcelWriter 将多个 DataFrame 写入同一个 Excel 文件的不同工作表
with pd.ExcelWriter('xxx.xlsx') as writer:
    # for sheet_name, dataframe in dfs.items():
    #     dataframe.to_excel(writer, sheet_name=sheet_name, index=False)

    for i,table in enumerate(tables):
        print(f"pageNumber:{i+1} \n")
        print(f"dateframe:{table.df} \n")
        df = table.df
        # 设置第一行为列名
        # df.columns = df.iloc[0]  # 使用第一行替换列名
        df.columns = [col.replace('\n', '') for col in df.iloc[0]]  # 去掉换行符
        df = df[1:]  # 删除第一行数据

        # 清理数据内容，去掉换行符
        df = df.map(lambda x: x.replace('\n', '').strip())

        df=df.reset_index(drop=True)  # 重置索引以删除旧索引
        sheet_name = f"sheet{i+1}"
        df.to_excel(writer, sheet_name=sheet_name, index=False)

