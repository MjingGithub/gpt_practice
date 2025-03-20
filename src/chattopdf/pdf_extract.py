import tabula

pdf_path="xxx.pdf"

dfs = tabula.read_pdf(pdf_path,stream=True,pages='all')

print(len(dfs))

print(dfs)

tabula.convert_into(pdf_path,"xxx.csv",output_format="csv",pages='all')

tabula.convert_into(pdf_path,"xxx.json",output_format="json",pages='all')