import json
import concurrent.futures

from utils import get_year, get_month
from utils import get_submitter_info, get_country_from_domain

info = []
year_low = 2020
month_low = 8

print("Reading data...")

with open("data/arxiv.json") as f:
    for line in f:
        data = json.loads(line)
        year = get_year(data["versions"])
        month = get_month(data["versions"])
        if year >= year_low and month >= month_low:
            info.append((data["submitter"], data["title"]))

print("Done. Number of articles:", len(info))


def task(id, info_slice):
    print(f"Worker {id} started")
    already_seen_domains = {}

    for submitter, title in info_slice:
        country = None
        try:
            submitter_info = get_submitter_info(submitter, title)
            domain = submitter_info.email.split("@")[1]
            if domain in already_seen_domains:
                country = already_seen_domains[domain]
            else:
                country = get_country_from_domain(domain)
                already_seen_domains[domain] = country
        except:
            pass

        with open(f"data/countries/{id}.txt", "at") as f:
            f.write(str(country) + "\n")

    return f"Worker {id} completed"


num_workers = 8
chunk_size = len(info) // num_workers
chunk_indexes = [[start, start + chunk_size] for start in range(0, len(info), chunk_size)]
chunk_indexes[-1][1] = -1

with concurrent.futures.ProcessPoolExecutor(max_workers=100) as executor:
    futures = [executor.submit(task, i, info[s[0] : s[1]]) for i, s in enumerate(chunk_indexes)]
    for future in concurrent.futures.as_completed(futures):
        print(future.result())
