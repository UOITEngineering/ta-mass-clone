# ta-mass-clone
Using beautiful soup and python scripting, mass clone student repositories

# Setup

1. The glob scripting requires python 3.6, so use this to enable virtual env for python 3
```
virtualenv -p python3.6 venv
source venv/bin/activate
```

2. Install the necessary packages
```
pip install -r requirenments.txt
```

3. Download the assignment html with all repos listed to the *data* sub folder. *Tip: download as complete webpages*

# Clone

1. Run the scrape script
```
python scrape_and_clone.py
```
