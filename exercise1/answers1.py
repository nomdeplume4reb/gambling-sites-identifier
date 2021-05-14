#installation as needed:
#import sys
#import subprocess

# implement pip as a subprocess:
#subprocess.check_call([sys.executable, '-m', 'pip', 'install',
#'url_parser'])

#subprocess.check_call([sys.executable, '-m', 'pip', 'install',
#'selenium'])

from url_parser import parse_url
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = 'https://nomdeplume4reb.github.io/portfolio/'

#use url_parser library to parse parts of give url
parsed = parse_url('https://nomdeplume4reb.github.io/portfolio/')

#covert none types to empty string
convert_None = lambda i : i or ''

#create variables for parts of url
tld = parsed['top_domain']
domain = parsed['domain']+'.'+parsed['top_domain']

#because 'hostname' is not included in url_parser library, I have to
sub = ''
if parsed['sub_domain'] == None:
    sub = ''
else:
    sub = '.'
hostname = convert_None(parsed['sub_domain'])+sub+parsed['domain']+'.'+parsed['top_domain']

path = parsed['path']
links_list = []
same_hostname = []
same_domain = []
different_domain = []

#set up a dictionary to output formated results:
links = {'Same hostname': same_hostname, 'Same domain': same_domain, 'Different domain': different_domain}
parsed_url = {'TLD': tld, 'DOMAIN': domain, 'HOSTNAME': hostname, 'PATH': path, 'LINKS': links}

#use selenium to scrape the (possibly dynamic) website for links on page and append them to links_list
#insert local path for Chrome!
driver = webdriver.Chrome()

driver.get(url)

continue_link = driver.find_element_by_tag_name('a')
elems = driver.find_elements_by_xpath("//a[@href]")
for elem in elems:
    links_list.append(elem.get_attribute("href"))
driver.quit()

# sort links according to same_domain, same_host, or different_domain
for link in links_list:
    if domain in link:
        same_domain.append(link)
    elif hostname in link:
        same_hostname.append(link)
    else:
        different_domain.append(link)

#output is the dictionary parsed_url
print(parsed_url)
