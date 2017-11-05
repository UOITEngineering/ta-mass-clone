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
	hashes = []
	repos = []
	with open(file) as fp:
		soup = BeautifulSoup(fp, 'html.parser')
		elements = soup.findAll("a", { "class" : "repo-detail-item tooltipped tooltipped-n", "aria-label": "View Submission"}, href=True)

		for element in elements:
			url = element['href']
			org = url.split('/')[3]
			repo = url.split('/')[4]
			hash = url.split('/')[6]
			url = 'git@github.com:%s/%s.git' % (org,repo)
			urls.append(url)
			hashes.append(hash)
			repos.append(repo)

	return urls, repos, hashes

def clone_repos(name, urls, repos, hashes):
	"""
	Clone urls into the clones dir

	:param urls: list of str
	"""
	git_command = 'git clone %s clones/%s/%s'
	change_dir_command = './clones/%s/%s'
	parent_dir = '../../../'
	hash_command = 'git reset --hard %s'
	for index, url in enumerate(urls):
		print('%d/%d' % (index, len(urls)))
		repo = repos[index]
		hash = hashes[index]

		git_command_ = git_command % (url, name, repo)
		hash_command_ = hash_command % (hash)
		repo_dir = change_dir_command % (name, repo)

		os.system(git_command_)
		try:
			os.chdir(repo_dir)
			os.system(hash_command_)
			os.chdir(parent_dir)
		except Exception as err:
			print(err)
		time.sleep(5)


if __name__ == '__main__':
	files = glob.glob('%s/*.html' % (CONFIG.data.dir))
	for file in files:
		name = file.split('/')[-1].split('.')[0]
		urls, repos, hashes = scrape_repo_elements(file)
		clone_repos(name, urls, repos, hashes)
