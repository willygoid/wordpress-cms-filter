import threading
import time, os
import requests

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
 [#] Domain to IP
 [#] Coded by @willygoid
 [#] www.haxor.id
""" + bcolors.ENDC)

sitelist = input("Sitelist : ")
threadp = input("Thread (default: 1000): ")
if threadp == '' or type(threadp) != int:
    threadp = 1000
    
#url_list = open(sitelist,"r").read().splitlines()

def save(url):
    print(bcolors.OKGREEN + "WordPress ---> " + bcolors.ENDC + url)
    with open("wordpress.txt","a") as f:
        f.write(url + "\n")

def resolveDns(hostnames):
    ua = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    for host in hostnames:
        try:
            if "http" not in host:
                checkHost = "http://" + host
            
            urlCheck = checkHost + '/license.txt'
            response = requests.get(urlCheck,headers=ua,timeout=5)
            if response.status_code < 400:
                if 'WordPress - Web publishing software' in response.text:
                    save(host)
                else:
                    print(bcolors.WARNING + "Not WordPress ---> " + bcolors.ENDC + host)
            else: 
                print(bcolors.WARNING + "Not WordPress ---> " + bcolors.ENDC + host)
            
        except Exception as e:
            print(bcolors.FAIL + "Not working ---> " + bcolors.ENDC + host)
            continue

if __name__ == "__main__":
    
    with open(sitelist) as file:
        hostnames = (line.rstrip() for line in file) 
        hostnames = list(line for line in hostnames if line)
    
    print(bcolors.OKPURPLE + "===[ Start Work ]==="+ bcolors.ENDC)
    start = time.time()
    
    threads = list()

    chunksize = threadp

    chunks = [hostnames[i:i + chunksize] for i in range(0, len(hostnames), chunksize)]
    for chunk in chunks:
        x = threading.Thread(target=resolveDns, args=(chunk,))
        threads.append(x)
        x.start()

    for chunk, thread in enumerate(threads):
        thread.join()

    end = time.time()
    duration = end - start
    print(" ")
    print(f'{bcolors.OKCYAN}Finished {len(hostnames)} links in {duration} seconds {bcolors.ENDC}')
