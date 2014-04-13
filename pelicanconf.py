#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Ilya Zonov'
SITENAME = u"Puzan's Pages"
SITEURL = ''

TIMEZONE = 'Europe/Moscow'

DEFAULT_LANG = u'ru'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = None

# Social widget
SOCIAL = (('twitter', 'https://twitter.com/puzan'),
          ('linkedin', 'http://www.linkedin.com/in/zonov'),
          ('github', 'http://github.com/puzan'),)

DEFAULT_PAGINATION = 10

THEME = './theme'
BOOTSTRAP_THEME = 'readable-old'

# Urls
ARTICLE_URL = '{category}/{date:%Y}-{date:%m}-{date:%d}-{slug}.html'
ARTICLE_SAVE_AS = ARTICLE_URL

CATEGORY_URL = '{slug}/index.html'
CATEGORY_SAVE_AS = CATEGORY_URL
CATEGORIES_URL = 'categories.html'
CATEGORIES_SAVE_AS = CATEGORIES_URL

TAG_URL = 'tag/{slug}.html'
TAG_SAVE_AS = TAG_URL
TAGS_URL = 'tag/index.html'
TAGS_SAVE_AS = TAGS_URL

AUTHOR_URL = 'author/{slug}/index.html'
AUTHOR_SAVE_AS = AUTHOR_URL
AUTHORS_URL = False
AUTHORS_SAVE_AS = AUTHORS_URL

ARCHIVES_URL = 'archives.html'
ARCHIVES_SAVE_AS = ARCHIVES_URL
YEAR_ARCHIVE_SAVE_AS = '{date:%Y}.html'
MONTH_ARCHIVE_SAVE_AS = '{date:%Y}-{date:%m}.html'

TAG_CLOUD_STEPS = 3
TAG_CLOUD_MAX_ITEMS = 100

DISPLAY_TAGS_INLINE = True
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True

MD_EXTENSIONS = ['codehilite(guess_lang=False,css_class=highlight,linenums=False)',
                 'extra',
                 'fenced_code']

PYGMENTS_STYLE = 'zenburn'

GITHUB_URL = 'https://github.com/puzan/puzan.github.io'
GITHUB_SKIP_FORK = False
GITHUB_USER = 'puzan'

STATIC_PATHS = ['images', 'extra']

EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
