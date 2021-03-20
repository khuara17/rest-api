import concurrent.futures
import requests
import threading
import time


thread_local = threading.local()

# delay_value = 5

def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url):
    session = get_session()
    with session.get(url) as response:
        # print(f"Read {len(response.content)} from {url}")
        print(response)


def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_site, sites)


def process(delay_value):
    site = [
        "https://httpbin.org/delay/" + str(delay_value),
    ] * 5
    print(site)
    start_time = time.time()
    download_all_sites(site)
    duration = time.time() - start_time
    print(f"Downloaded {len(site)} in {duration} seconds")
    return duration

# process(delay_value)