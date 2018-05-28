from constants import job_constant


def is_invalid_job(job):
    from filters import job_filter

    for invalid_keyword in job_filter.exclude_job_keywords:
        if invalid_keyword.lower() in job.get(job_constant.JOB).lower():
            return False
    return True
