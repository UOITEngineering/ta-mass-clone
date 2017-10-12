from __future__ import print_function

from bs4 import BeautifulSoup
import glob
import os
import time

import config as CONFIG


def scrape_repo_elements(file):
	"""
	Use beautiful soup to get repo urls
	"""
	urls = []
	with open(file) as fp:
		soup = BeautifulSoup(fp, 'html.parser')
		elements = soup.findAll("a", { "class" : "btn btn-outline " }, href=True)
		for element in elements:
			url = element['href']
			org = url.split('/')[3]
			repo = url.split('/')[-1]
			url = 'git@github.com:%s/%s.git' % (org,repo)
			urls.append(url)

	return urls

def clone_repos(name, urls):
	"""
	Clone urls into the clones dir

	:param urls: list of str
	"""
	command = 'git clone %s clones/%s/%s'
	for url in urls:
		repo_name = url.split('/')[-1].split('.')[0]
		url_command = command % (url, name, repo_name)
		os.system(url_command)
		time.sleep(2)


if __name__ == '__main__':
	files = glob.glob('%s/*.html' % (CONFIG.data.dir))
	for file in files:
		name = file.split('/')[-1].split('.')[0]
		repos = scrape_repo_elements(file)
		clone_repos(name, repos)
