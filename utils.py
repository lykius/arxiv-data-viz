import arxiv.taxonomy as tax
from datetime import datetime
from scholarly import scholarly
import universities


def get_category(id):
    archive = tax.get_archive_display(id.split(".")[0])
    archive = archive.split("(")[0].strip()
    category = tax.get_category_display(id)
    category = category.split("(")[0].strip()
    if archive == category:
        return category
    return ": ".join([archive, category])


def get_year(versions_history):
    d = datetime.strptime(versions_history[0]["created"], "%a, %d %b %Y %H:%M:%S %Z")
    return d.year


def get_month(versions_history):
    d = datetime.strptime(versions_history[0]["created"], "%a, %d %b %Y %H:%M:%S %Z")
    return d.month


def get_submitter_info(submitter):
    try:
        query = scholarly.search_author(submitter)
        author = next(query).fill()
        return author
    except:
        return None


def get_country_from_domain(domain):
    try:
        country = None
        uniapi = universities.API()
        for u in uniapi.search(domain=domain):
            if domain in u.domains:
                country = u.country
                break
        return country
    except:
        return None
