# joblint-hn

This script uses requests, lxml, and (joblint)[https://github.com/rowanmanning/joblint] to test all of the currently-available job postings on Hacker News' jobs page for various common recruiting fails.

I wrote it basically as soon as I heard of joblint, because, obviously! The script is quick, dirty, and totally non-asynchronous (and relatedly slow), because I am impatient.

### Installation

You'll need python, pip, and npm already installed.

* Make a virtualenv (suggested instructions below, if you have another way do that instead)
  * `$ virtualenv env`
  * `$ source env/bin/activate`
* `$ pip install -r requirements.txt`
* `$ npm install joblint -g`
  * or whatever the (joblint repository)[https://github.com/rowanmanning/joblint] installation instructions recommend, who knows, it might change in the future
* `$ python hn.py`

Please don't run the script too many times too often--the goal is not to DDOS Hacker News! You can re-run the mass lint step by setting '''download_afresh''' to '''False''' in `hn.py`.
