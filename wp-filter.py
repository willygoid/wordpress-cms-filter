import requests
from requests.sessions import Session
import time, os
from threading import Thread,local
from queue import Queue

if os.name == "nt":
	os.system("cls")
else:
	os.system("clear")
	
class bcolors:
    OKPURPLE = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(bcolors.OKCYAN + """
 [#] Wordpress CMS Filter
 [#] Coded by @willygoid
 [#] www.haxor.id
""" + bcolors.ENDC)

sitelist = input("Sitelist : ")
threadp = input("Thread (default: 1000): ")
if threadp == '' or type(threadp) != int:
    threadp = 1000
    
url_list = open(sitelist,"r").read().splitlines()
q = Queue(maxsize=0)            #Use a queue to store all URLs

for url in url_list:
    if url is None:
        url = "http://example.com"
    if "http" not in url:
        url = "http://" + url
    q.put(url)
thread_local = local()          #The thread_local will hold a Session object

def get_session() -> Session:
    if not hasattr(thread_local,'session'):
        thread_local.session = requests.Session() # Create a new Session if not exists
    return thread_local.session

def save(url):
    print(bcolors.OKGREEN + "WordPress ---> " + bcolors.ENDC + url)
    with open("wordpress.txt","a") as f:
        f.write(url + "\n")
        
def download_link() -> None:
    '''download link worker, get URL from queue until no url left in the queue'''
    session = get_session()
    ua = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    while True:
        url = q.get()
        urlCheck = url + '/license.txt'
        try:
            response = session.get(urlCheck,headers=ua,timeout=1)
            if response.status_code < 403:
                save(url)
            else: 
                print(bcolors.WARNING + "Not WordPress ---> " + bcolors.ENDC + url)
        except:
            print(bcolors.FAIL + "Not working ---> " + bcolors.ENDC + url)
            #print(f'Read {response.status_code} from {url}')
        q.task_done()          # tell the queue, this url downloading work is done

def download_all(urls) -> None:
    '''Start 10 threads, each thread as a wrapper of downloader'''
    thread_num = threadp
    for i in range(thread_num):
        t_worker = Thread(target=download_link)
        t_worker.start()
    q.join()                   # main thread wait until all url finished downloading

print(bcolors.OKPURPLE + "===[ Start Work ]==="+ bcolors.ENDC)
start = time.time()
download_all(url_list)
end = time.time()
print(f'download {len(url_list)} links in {end - start} seconds')
