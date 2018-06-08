import re
import math
import time
from bs4 import BeautifulSoup
import requests


def find_salary(url):
    response = requests.get(
        url=url,
        timeout=10
    )
    if response is None or response.status_code != 200:
        print(f"find_salary({url}) fail")
    content = response.content
    response.close()
    whole_body_soup = BeautifulSoup(content, "lxml")
    pattern = re.compile("薪\)")
    article = whole_body_soup.find("article", text=pattern)
    return article.text


def find_jobs_by_page(page):
    search_job_url = "https://www.yourator.co/api/v2/jobs"
    params = {
        "position[]": 1,  # full-time
        "skillTag[]": [13],  # Python: 13
        "page": page

    }
    response = requests.get(
        url=search_job_url,
        params=params,
        timeout=3
    )

    try:
        result = response.json()
        return result["jobs"]
    except:
        print(f"find_jobs() fail.")
        return list()
    finally:
        response.close()


def find_jobs():
    search_job_url = "https://www.yourator.co/api/v2/jobs"
    params = {
        "position[]": 1,  # full-time
        "skillTag[]": [13]  # Python: 13

    }
    response = requests.get(
        url=search_job_url,
        params=params,
        timeout=3
    )

    try:
        data = response.json()
        return data
    except:
        print(f"find_jobs() fail.")
        return list()
    finally:
        response.close()


total_jobs = list()
page_size = 20
result = find_jobs()
total_count = result["total"]
jobs = result["jobs"]
total_jobs.extend(jobs)
pages = math.ceil(total_count / page_size)
print(f"{total_count}")
print(f"{pages}")
if pages > 1:
    for page in range(2, pages + 1):
        jobs_in_the_page = find_jobs_by_page(page=page)
        total_jobs.extend(jobs_in_the_page)
print(f"len(jobs): {len(total_jobs)}")
print(f"jobs: {total_jobs}")

filtered_jobs = [job for job in total_jobs if job["has_salary_info"]]
print(f"len(jobs): {len(filtered_jobs)}")
print(f"jobs: {filtered_jobs}")

for job in filtered_jobs:
    url_prefix = "https://www.yourator.co"
    path = job["path"]
    job_title = job["name"]
    url = f"{url_prefix}{path}"
    salary = find_salary(url=url)
    print(f"{job_title}/{salary} {url}")
    time.sleep(1.2)
