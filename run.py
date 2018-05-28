import time
import datetime
from urllib import parse
from constants import job_constant
from constants import company_constant
from utils import crawler
from utils import csv_reader
from utils import file_util
from utils import job_util


if __name__ == "__main__":
    csv_file_path = "106.csv"
    companies = csv_reader.read_companies_info_from_csv(csv_file_path)
    target_industries = ["民間產業/資訊", "民間產業/數位內容", "民間產業/通訊"]
    filtered_companies = [company for company in companies if company["industry"] in target_industries]
    print(f"companies: {len(companies)}")
    print(f"filtered_companies: {len(filtered_companies)}")

    # get jobs
    total_jobs = list()
    for company in filtered_companies:
        company_id = crawler.find_company_id_by_name(company.get(company_constant.COMPANY_NAME))
        if company_id is None:
            continue
        job_result = crawler.find_jobs_by_company_id(company_id=company_id)
        jobs = job_result["data"]
        for job in jobs:
            company_name = company.get(company_constant.COMPANY_NAME)
            job_title = job.get(job_constant.JOB)
            query = f"?q={company_name}+{job_title}"
            utf8_encoded_query = parse.quote_plus(string=query, encoding="utf8")
            search_url = f"https://www.google.com.tw/search?q={company_name}+{job_title}"
            job[job_constant.SEARCH_URL] = search_url
        total_jobs.extend(jobs)
        print(f"{len(jobs)} {company}")
        time.sleep(0.8)

    # filter jobs
    filtered_jobs = [job for job in total_jobs if job_util.is_invalid_job(job)]
    export_data = {
        "jobs": filtered_jobs
    }

    now = datetime.datetime.now()
    time_str = now.strftime("%Y%m%d%H%M%S")  # ex. 20180118162739
    export_filename = f"{time_str}_export.json"
    file_util.save_dict_as_json_file(directory_path=".", filename=export_filename, dict_data=export_data)
    print(f"File is exported: {export_filename}")
