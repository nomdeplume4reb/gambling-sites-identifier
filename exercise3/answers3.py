#installation as needed:
#import sys
#import subprocess

# implement pip as a subprocess:
#subprocess.check_call([sys.executable, '-m', 'pip', 'install',
#'pandas'])

#subprocess.check_call([sys.executable, '-m', 'pip', 'install',
#'selenium'])

#subprocess.check_call([sys.executable, '-m', 'pip', 'install',
#'nltk'])


#PART ONE
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

#text file with list of known gambling sites:
file = 'C:/Users/rache/Downloads/Junior Content Analyst/exercise3/gamblingsites.txt'

#create dataframe from text file
sites_df = pd.read_csv(file, delimiter = "\t", header=None)

sites_df.columns = ['site']

#iterate over dataframe to get the content of each site and input into content column
content = []

for index, row in sites_df.iterrows():
    url = row.site
    #insert chrome file path!
    driver = webdriver.Chrome()
    driver.get(url)
    body = driver.find_elements_by_css_selector("body")
    for elem in body:
        text = elem.text
        content.append(text)
    driver.quit()

sites_df['content'] = content

print(sites_df)

#saving file so I don't have to scrape each time
sites_df.to_csv(r'C:/Users/rache/Downloads/Junior Content Analyst/exercise3/gambling-sites-text.csv', index = None)

#creating lists and dictionaries from words in content columns
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#download nltk stopwords as needed: nltk.download('punkt')

#create string from content column
content_words = ' '.join(content)

content_words = re.sub('[^0-9a-zA-Z]+', ' ', content_words)

#download stopwords (e.g. 'the', 'will') from nltk so they can be filtered from list
stop_words = set(stopwords.words('english'))

#tokenizing words into list and filtering out stopwords
word_tokens = word_tokenize(content_words)

filtered_list = [w for w in word_tokens if not w in stop_words]

filtered_list = []

for w in word_tokens:
    if w not in stop_words:
        filtered_list.append(w)

# Converts each token into lowercase
for i in range(len(filtered_list)):
        filtered_list[i] = filtered_list[i].lower()

#creating dictionary as required by assignment. NLTK outputs word tokens as list
keyword_dictionary = dict.fromkeys(filtered_list, None)

#finding most common words
keywords = FreqDist(filtered_list)

keywords.most_common(10)

gambling_words = []

for elem in keywords.most_common(10):
    gambling_words.append(elem[0])

#print(gambling_words)

#PART TWO
#repeating process as a function, whose output classifies site as gambling or non-gambling
def inspect_url(url):
    content = []
    #insert chrome file path!
    driver = webdriver.Chrome()
    driver.get(url)
    body = driver.find_elements_by_css_selector("body")
    for elem in body:
        text = elem.text
        content.append(text)
    driver.quit()
    content_words = ' '.join(content)

    content_words = re.sub('[^0-9a-zA-Z]+', ' ', content_words)

    stop_words = set(stopwords.words('english'))

    word_tokens = word_tokenize(content_words)

    filtered_list = [w for w in word_tokens if not w in stop_words]

    filtered_list = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_list.append(w)

    for i in range(len(filtered_list)):
            filtered_list[i] = filtered_list[i].lower()

    keywords = FreqDist(filtered_list)

    #finding most common words for inputed site
    top_words = []

    for elem in keywords.most_common(10):
        top_words.append(elem[0])
    #checking if any of the top words from site are including in the list of gambling words from part 1
    check =  any(item in top_words for item in gambling_words)

    if check is True:
        return "Gambling site"
    else :
        return "Non-Gambling site"

inspect_url('https://www.888poker.com/')
