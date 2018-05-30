# crawler-104
A crawler for searching 104 jobs.


## Precondition
```sh
virtualenv -p python3 envname
source venv/bin/activate
pip install -r requirements.txt
```

## Run Crawler
```sh
python run.py
```

## Customize Filter
crawler-104/filters/job_filter.py
```py
exclude_job_keywords = ["硬體"] # exlude jobs which job title contain exclude_job_keywords.

include_keyword = "python" # include jobs which job title, job description or skills contain include_keyword
```

## Reference
104 API document - http://www.104.com.tw/i/api_doc/jobsearch/documentation.cfm
