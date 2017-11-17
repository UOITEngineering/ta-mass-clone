from __future__ import print_function

from bs4 import BeautifulSoup
import glob
import os
import time

import config as CONFIG


def scrape_repo_elements(assignment):
	"""
	Use beautiful soup to get repo urls
	"""
	urls = []
	hashes = []
	repos = []
	with open('%s/%s.html' % (CONFIG.data.dir, assignment)) as fp:
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

	repo_dirs = []
	for index, url in enumerate(urls):
		print('%d/%d' % (index, len(urls)))
		repo = repos[index]
		hash = hashes[index]

		git_command_ = git_command % (url, name, repo)
		hash_command_ = hash_command % (hash)
		repo_dir = change_dir_command % (name, repo)
		repo_dirs.append(repo_dir)

		os.system(git_command_)
		try:
			os.chdir(repo_dir)
			os.system(hash_command_)
			os.chdir(parent_dir)
		except Exception as err:
			print(err)
		time.sleep(5)

	return repo_dirs


def split_clones(assignment):
	"""
	Use the split_config to extract files into appropriate folders

	:param repo_dirs: list of str
	"""
	clone_dir = '%s/%s' % (CONFIG.clones.dir, assignment)
	repo_dirs = os.listdir(clone_dir)
	for ind, repo in enumerate(repo_dirs):
		# repo = repos[ind]
		repo_dir = '%s/%s' % (clone_dir, repo)
		for key in CONFIG.split_config['folders'].keys():
			for split_file in CONFIG.split_config['folders'][key]:
				glob_path = '%s/**/%s' % (repo_dir, split_file)
				for glob_file in glob.glob(glob_path, recursive=True):
					glob_file = glob_file.replace(" ", "\ ")

					split_dir = '%s/%s' % (CONFIG.splits.dir, assignment)
					key_dir = '%s/%s/%s' % (split_dir, key, repo)
					cp_command = 'cp %s %s' % (glob_file, key_dir)

					try:
						if not os.path.exists(split_dir):
							os.makedirs(split_dir)
						if not os.path.exists(key_dir):
							os.makedirs(key_dir)
						os.system(cp_command)
					except Exception as err:
						print(err)


def extract_clones(assignment):
	"""
	Use the split_config to extract files into appropriate folders

	:param repo_dirs: list of str
	"""
	clone_dir = '%s/%s' % (CONFIG.clones.dir, assignment)
	repo_dirs = os.listdir(clone_dir)
	for ind, repo in enumerate(repo_dirs):
		# repo = repos[ind]
		repo_dir = '%s/%s' % (clone_dir, repo)
		for file_type in CONFIG.extract_config['file_types']:
			glob_path = '%s/**/*%s' % (repo_dir, file_type)
			for glob_file in glob.glob(glob_path, recursive=True):
				glob_file = glob_file.replace(" ", "\ ")

				extract_dir = '%s/%s' % (CONFIG.extract.dir, assignment)
				extract_repo_dir = '%s/%s' % (extract_dir, repo)
				cp_command = 'cp %s %s' % (glob_file, extract_repo_dir)

				try:
					if not os.path.exists(extract_dir):
						os.makedirs(extract_dir)
					if not os.path.exists(extract_repo_dir):
						os.makedirs(extract_repo_dir)
					os.system(cp_command)
				except Exception as err:
					print(err)



if __name__ == '__main__':
	split = True
	extract = True

	files = glob.glob('%s/*.html' % (CONFIG.data.dir))
	for assignment_file in files:
		assignment = assignment_file.split('/')[-1].split('.')[0]
		urls, repos, hashes = scrape_repo_elements(assignment)
		repo_dirs = clone_repos(assignment, urls, repos, hashes)

		if split:
			split_clones(assignment)
		if extract:
			extract_clones(assignment)
