# S3-Logs-Analyzer

- Download the access logs and parse them to retrieve the actual access counts for the files being hosted on S3
- Generate a CSV with fields: file, date, downloads

## Setup

	$ virtualenv pyenv --no-site-packages
	$ source pyenv/bin/activate
	$ pip install -r requirements.txt

## Download S3 log files (only downloads non existing ones)

	$ python sync.py [the flags]
	$ get a coffee (if initial_import)

## Parse

	$ python parse.py --folder [the folder name where the log files got downloaded to]
