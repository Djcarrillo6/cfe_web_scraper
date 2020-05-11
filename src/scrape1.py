import csv
import datetime
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from collections import Counter
from stop_words import get_stop_words



## to get rid of specific punction marks in the scraping of the site
def clean_word(word):
	word = word.replace("!", "")
	word = word.replace("?", "")
	word = word.replace(".", "")
	word = word.replace(":", "")
	word = word.replace(",", "")
	word = word.replace(";", "")
	return word 




def clean_up_words(words):
	new_words = []
	pkg_stop_words = get_stop_words('en')
	print(pkg_stop_words)
	my_stop_words = ['the', 'is', 'and']
	for word in words:
		word = word.lower()
		if word in my_stop_words or word in pkg_stop_words: ## checking to see if any stop words are in either of the lists I defined.
			pass
		else:
			cleaned_word = clean_word(word)
			new_words.append(cleaned_word)
	return new_words


def create_csv_path(csv_path):
	if not os.path.exists(path):
		with open(csv_path, 'w') as csvfile: # open that path w = write and/or create
			header_columns = ['word', 'count', 'timestamp'] #arbitray values that i assign to the csv file colum header
			writer = csv.DictWriter(csvfile, fieldnames=header_columns)
			writer.writeheader()



saved_domains = {
	"joincfe.com": "main-container",
	"tim.blog": "content-area"
}

my_url = input("Enter the url to scrape: ")


print("Grabbing...", my_url)
domain = urlparse(my_url).netloc
print("via domain", domain)

response = requests.get(my_url)

print("Status is", response.status_code) #200, 403, 404, 500, 503 (typical error codes)

if response.status_code != 200:
	print("You can't scrape this!", response.status_code)
else:
	print("Scrapping...")
	#print(response.text)
	html = response.text
	soup = BeautifulSoup(html, "html.parser")
	if domain in saved_domains:
		div_class = saved_domains[domain]
		body_ = soup.find("div", {"class": div_class})
	else:
		body_ = soup.find("body")

	words = body_.text.split()
	word_counts = Counter(words)
	print(word_counts.most_common(30)) # number of words = '30'

	## to create the csv file
	filename = domain.replace(".", "-") + '.csv'
	path = 'csv/' + filename
	timestamp = datetime.datetime.now() #timestamp
	create_csv_path(path)
	with open(path, 'a') as csvfile: # open that path w = write and/or create
		header_columns = ['word', 'count', 'timestamp'] #arbitray values that i assign to the csv file colum header
		writer = csv.DictWriter(csvfile, fieldnames=header_columns)
		for word, count in word_counts.most_common(30):
			writer.writerow({			#to write the rows in the csv file
					"count": count,
					"word": word,
					"timestamp": timestamp
				})


