#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = 'https://puzan.info'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
TAG_FEED_ATOM = 'feeds/tag/{slug}.atom.xml'

FEEDBURNER_ALL_FEED = 'http://feeds.feedburner.com/puzan'
YANDEX_SHARE = True

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

DISQUS_SITENAME = "puzan"
GOOGLE_ANALYTICS = "UA-50875216-1"

GITHUB_URL = 'https://github.com/puzan/puzan.github.io'
GITHUB_SKIP_FORK = False
GITHUB_USER = 'puzan'

ARTICLE_EXCLUDES = ['draft']
