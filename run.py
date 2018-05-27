import time
from constants import job_constant
from constants import company_constant
from utils import crawler
from utils import csv_reader


def is_invalid_job(job):
    invalid_keywords = ["測試", "課長", "主任", "硬體", "韌體", "自動化", "資安", "DevOps", "Security", "QA", "PHP", "IT",
                        "Front", "Support", "Learning", "Test", "Research", "Architect"]
    for invalid_keyword in invalid_keywords:
        if invalid_keyword.lower() in job.get(job_constant.JOB).lower():
            return False
    return True


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
    total_jobs.extend(jobs)
    print(f"{len(jobs)} {company}")
    time.sleep(1)

# filter jobs
filtered_jobs = [job for job in total_jobs if is_invalid_job(job)]
print({
    "jobs": filtered_jobs
})
