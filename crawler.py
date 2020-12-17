import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python"

def get_last_page(url):
  result = requests.get(URL)

  soup = BeautifulSoup(result.text, "html.parser")

  pagination = soup.find("div", {"class": "s-pagination"}).find_all("a")
  pagination = pagination[-2].get_text(strip = True)
  return int(pagination)

def extract_jobs(html):
  title = html.find("div", {"class": "grid--cell fl1"}).find("a")["title"]  ##일자리 제목

  company, location = html.find("div", {"class": "grid--cell fl1"}).find("h3", {"class": "fc-black-700"}).find_all("span",recursive=False)

  company = company.get_text(strip = True)
  location = location.get_text(strip = True)

  job_id = html['data-jobid']

  return {
    'title': title,
    'company': company,
    'location': location,
    'link': f"https://stackoverflow.com/jobs/{job_id}"
  }

def extract_so_jobs(last_page, url):
  jobs = []
  for page in range(last_page):
    print(f"stackoverflow {page + 1}페이지에서 일자리 긁어오는 중...")

    result = requests.get(f"{url}&pg={page+1}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "-job"})

    for result in results:
      jobs.append(extract_jobs(result))

  return jobs

def get_jobs(word):
  URL = f"https://stackoverflow.com/jobs?q={word}"
  last_page = get_last_page(URL)
  jobs = extract_so_jobs(last_page, URL)
  return jobs