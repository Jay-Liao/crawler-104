import os
import time
import datetime
import random
import math
from urllib import parse
from concurrent.futures import ThreadPoolExecutor
from concurrent import futures
from constants import company_constant
from constants import job_constant
from utils import crawler
from utils import csv_reader
from utils import file_util
from utils import job_util
from filters import industry_filter


def do_company_task(company):
    sleeping = random.uniform(1, 1.2)
    time.sleep(sleeping)
    company_id = crawler.find_company_id_by_name(company[company_constant.COMPANY_NAME])
    company[company_constant.COMPANY_ID] = company_id
    print(f"{company[company_constant.COMPANY_NAME]} {company_id}")
    return company


def do_job_task(companies):
    sleeping = random.uniform(2.5, 3)
    time.sleep(sleeping)
    company_ids = [company[company_constant.COMPANY_ID] for company in companies]
    jobs = crawler.find_jobs_by_company_ids(company_ids=company_ids)
    for job in jobs:
        company_name = parse.quote_plus(string=job[job_constant.COMPANY_NAME], encoding="utf8")
        job_title = parse.quote_plus(string=job[job_constant.JOB_TITLE], encoding="utf8")
        search_url = f"https://www.google.com.tw/search?q={company_name}+{job_title}"
        job[job_constant.SEARCH_URL] = search_url
    print(f"{len(jobs)} {companies}")
    return jobs


if __name__ == "__main__":
    directory = "csv_data"
    companies_map = dict()
    for root, dirs, files in os.walk(directory):
        for filename in files:
            csv_file_path = os.path.join(root, filename)
            companies = csv_reader.read_companies_info_from_csv(csv_file_path)
            for company in companies:
                companies_map[company[company_constant.COMPANY_NAME]] = company
            print(f"The {csv_file_path} has been read.")
    companies = [company for company in companies_map.values()]
    industries = list(set([company[company_constant.INDUSTRY] for company in companies]))
    target_industries = industry_filter.target_industries
    filtered_companies = [company for company in companies if company[company_constant.INDUSTRY] in target_industries]
    print(f"industries: {industries}")
    print(f"target_industries: {target_industries}")
    print(f"companies: {len(companies)}")
    print(f"filtered_companies: {len(filtered_companies)}")
    start_time = time.time()
    executor = ThreadPoolExecutor(max_workers=1)
    company_tasks = list()
    for company in filtered_companies:
        company_task = executor.submit(do_company_task, company)
        company_tasks.append(company_task)

    target_companies = list()
    for future in futures.as_completed(company_tasks):
        company = future.result()
        if company[company_constant.COMPANY_ID] is not None:
            target_companies.append(company)
    print(f"target_companies {len(target_companies)} {time.time() - start_time}")

    # get jobs
    total_jobs = list()
    job_tasks = list()
    page_size = 5
    pages = int(math.ceil(len(target_companies)/page_size))
    for page in range(pages):
        a_page_companies = target_companies[page * page_size:(page + 1) * page_size]
        job_executor = ThreadPoolExecutor(max_workers=2)
        job_task = executor.submit(do_job_task, a_page_companies)
        job_tasks.append(job_task)

    for future in futures.as_completed(job_tasks):
        jobs = future.result()
        total_jobs.extend(jobs)

    # filter jobs
    target_jobs = [job for job in total_jobs if job_util.is_invalid_job(job)]
    export_data = {
        "jobs": target_jobs
    }

    now = datetime.datetime.now()
    time_str = now.strftime("%Y%m%d_%H%M%S")  # ex. 20180118162739
    export_filename = f"{time_str}_export_{len(target_companies)}_{len(target_jobs)}.json"
    file_util.save_dict_as_json_file(file_path=export_filename, dict_data=export_data)
    print(f"File is exported: {export_filename} {time.time() - start_time}")
