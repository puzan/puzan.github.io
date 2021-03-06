#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

PLUGIN_PATHS = ['plugins']
PLUGINS = ['tag_cloud', 'i18n_subsites', 'sitemap']

JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.i18n'],
}

AUTHOR = 'Ilya Zonov'
SITENAME = "Puzan's Pages"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Moscow'

DEFAULT_LANG = 'ru'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = None

TWITTER_CARDS = True
USE_OPEN_GRAPH = True
TWITTER_USERNAME = "puzan"

# Social widget
SOCIAL = (('twitter', f'https://twitter.com/{TWITTER_USERNAME}'),
          ('linkedin', 'https://www.linkedin.com/in/zonov'),
          ('github', 'https://github.com/puzan'),
          ('zen', 'https://zen.yandex.ru/id/5c4d6cc29c57e900ad31e8ba', 'home'),
          ('photos', 'https://yandex.ru/collections/user/ilzon', 'camera'),
          ('rss', 'https://feeds.feedburner.com/puzan'))

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

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {
            'css_class': 'highlight',
            'guess_lang': False,
            'linenums': False
        },
        'markdown.extensions.extra': {},
        'markdown.extensions.fenced_code': {}
    }
}

PYGMENTS_STYLE = 'zenburn'
CUSTOM_CSS = 'static/custom.css'

FAVICON = 'favicon.ico'

STATIC_PATHS = ['images', 'extra']

EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    'extra/custom.css': {'path': 'static/custom.css'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/keybase.txt': {'path': 'keybase.txt'},
    'extra/robots.txt': {'path': 'robots.txt'}
}

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'monthly',
        'pages': 'monthly'
    }
}

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
