import re
import math
import time
import datetime
import gevent
from gevent import monkey
from bs4 import BeautifulSoup
from utils import file_util


monkey.patch_all()


def find_salary(url):
    import requests
    response = requests.get(
        url=url,
        timeout=10
    )
    salary = "Unknown"
    if response is None or response.status_code != 200:
        print(f"find_salary({url}) fail with invalid response")
        return salary
    content = response.content
    response.close()
    whole_body_soup = BeautifulSoup(content, "lxml")
    pattern = re.compile("薪\)")
    article = whole_body_soup.find("article", text=pattern)
    try:
        salary = article.text
        pass
    except:
        print(f"find_salary({url}) fail with {article}")
    return salary


def find_jobs_by_page(page, params):
    import requests
    search_job_url = "https://www.yourator.co/api/v2/jobs"
    params["page"] = page
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


def find_jobs(params):
    import requests
    search_job_url = "https://www.yourator.co/api/v2/jobs"
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


def do_salary_task(job):
    url = job["url"]
    salary = find_salary(url=url)
    brand = job["company"]["brand"]
    job_title = job["name"]
    return {
        "job_info": f"[{brand}] {job_title}",
        "link": url,
        "salary": salary
    }


# filter_params = {
#     "position[]": 1,  # full-time
#     "skillTag[]": [13]  # Python: 13
# }

filter_params = {
    "position[]": 1,  # full-time
    "category[]": 7   # Front-end Engineer
}

total_jobs = list()
page_size = 20
result = find_jobs(params=filter_params)
total_count = result["total"]
jobs = result["jobs"]
total_jobs.extend(jobs)
pages = math.ceil(total_count / page_size)
print(f"{total_count}")
print(f"{pages}")
if pages > 1:
    for page in range(2, pages + 1):
        jobs_in_the_page = find_jobs_by_page(page=page, params=filter_params)
        total_jobs.extend(jobs_in_the_page)

filtered_jobs = [job for job in total_jobs if job["has_salary_info"]]
print(f"len(total_jobs): {len(total_jobs)}")
print(f"len(filtered_jobs): {len(filtered_jobs)}")
# print(f"filtered_jobs: {filtered_jobs}")

for job in filtered_jobs:
    url_prefix = "https://www.yourator.co"
    path = job["path"]
    url = f"{url_prefix}{path}"
    job["url"] = url

start = time.time()
salary_tasks = [gevent.spawn(do_salary_task, job) for job in filtered_jobs]
# jobs = [gevent.spawn(print_head, url) for url in urls]
gevent.joinall(salary_tasks)
added_salary_jobs = [salary_task.value for salary_task in salary_tasks]
# print(f"filtered_jobs: {added_salary_jobs}")

now = datetime.datetime.now()
time_str = now.strftime("%Y%m%d_%H%M%S")  # ex. 20180118162739
export_filename = f"{time_str}_export_yourator_{len(added_salary_jobs)}.json"
export_data = {
    "jobs": added_salary_jobs
}
file_util.save_dict_as_json_file(directory_path="../", filename=export_filename, dict_data=export_data)
print(f"File is exported: {export_filename} {time.time() - start}")
