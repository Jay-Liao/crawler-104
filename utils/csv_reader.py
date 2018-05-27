import pandas
from constants import company_constant


"""
民間產業/資訊
民間產業/數位內容
民間產業/通訊

政府機關/
民間產業/電機
民間產業/其他
民間產業/光電
民間產業/服務業
大學校院/
民間產業/機械
民間產業/半導體
財團法人研究機構/民間產業/電子
行政法人/
民間產業/金屬
公立研究機關（構）
民間產業/民生化工生技
"""


def read_companies_info_from_csv(csv_path):
    data = pandas.read_csv(csv_path, encoding="utf8")
    companies = list()
    for _, row in data.iterrows():
        if str(row.id).lower() == "nan":
            continue
        company = {
            company_constant.ID: row.id,
            company_constant.INDUSTRY: row.industry,
            company_constant.COMPANY_NAME: row.company_name
        }
        companies.append(company)
    return companies
