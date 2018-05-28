from bs4 import BeautifulSoup
from urllib import parse
import requests


def find_company_id_by_name(company_name):
    search_company_url = "https://www.104.com.tw/cust/list/index/"
    params = {
        "keyword": company_name,
        "jobsource": "checkc"
    }
    utf8_encoded_params = parse.urlencode(params).encode("utf-8")
    response = requests.get(
        url=search_company_url,
        params=utf8_encoded_params,
        timeout=3
    )
    whole_body_soup = BeautifulSoup(response.content, "lxml")
    first_company_summary_div = whole_body_soup.select_one('div[class="company-summary"]')
    if first_company_summary_div is None:
        return None
    first_company_article = whole_body_soup.select_one('article[class="items"]')
    if first_company_article is None:
        return None
    article_soup = BeautifulSoup(str(first_company_article), "lxml")
    first_a = article_soup.select_one('a')
    the_company_url = first_a.get("href")
    params_map = parse.parse_qs(parse.urlparse(the_company_url).query)
    j_list = params_map.get("j")
    if not j_list:
        return None
    company_id = j_list[0]
    return company_id


def find_jobs_by_company_id(company_id):
    search_job_url = "http://www.104.com.tw/i/apis/jobsearch.cfm"
    params = {
        "fmt": 8,
        "c": company_id,
        "area": "6001001000",
        # cat: 2007001000 軟體╱工程類人員全部, 2007001004 軟體設計工程師, 2007001006 Internet程式設計師
        "cat": "2007001004,2007001006",
        "kwop": 3,
        "kws": "python",
        "role_status": 19,
        "intmp": 2,
        "incs": 2,
        "role": 1,
        "cols": "NAME,JOB,DESCRIPTION,OTHERS,JOB_ADDRESS,JOB_ADDR_NO_DESCRIPT",
        "pgsz": 999
    }
    utf8_encoded_params = parse.urlencode(params).encode("utf-8")
    response = requests.get(
        url=search_job_url,
        params=utf8_encoded_params,
        timeout=3
    )
    data = response.json()
    response.close()
    return data
