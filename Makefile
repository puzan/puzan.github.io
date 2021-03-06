PY?=python3
PELICAN?=pelican
PELICANOPTS=

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
CONFFILE=$(BASEDIR)/pelicanconf.py
PUBLISHCONF=$(BASEDIR)/publishconf.py
PUBLISHDIR=$(BASEDIR)/publish

GITHUB_PAGES_BRANCH=master


DEBUG ?= 0
ifeq ($(DEBUG), 1)
	PELICANOPTS += -D
endif

RELATIVE ?= 0
ifeq ($(RELATIVE), 1)
	PELICANOPTS += --relative-urls
endif

# New post variables
DRAFTDIR=$(INPUTDIR)/draft
DATE := $(shell date +'%Y-%m-%d')
DATETIME := $(shell date +'%Y-%m-%d %H:%M:%S')
SLUG := $(shell echo '${NAME}' | sed -e 's/[^[:alnum:]]/-/g' | \
	tr -s '-' | tr A-ZА-Я a-zа-я | sed -e 's/-$$//g')
CATEGORY ?= linux
EXT ?= md
POSTFILE := $(DRAFTDIR)/$(DATE)-$(SLUG).$(EXT)

NOW := $(shell date +"%c")
GIT_TMP := $(shell mktemp)

help:
	@echo 'Makefile for a pelican Web site                                           '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make html                           (re)generate the web site          '
	@echo '   make clean                          remove the generated files         '
	@echo '   make regenerate                     regenerate files upon modification '
	@echo '   make publish                        generate using production settings '
	@echo '   make serve [PORT=8000]              serve site at http://localhost:8000'
	@echo '   make serve-global [SERVER=0.0.0.0]  serve (as root) to $(SERVER):80    '
	@echo '   make devserver [PORT=8000]          serve and regenerate together      '
	@echo '   make ssh_upload                     upload the web site via SSH        '
	@echo '   make rsync_upload                   upload the web site via rsync+ssh  '
	@echo '   make github                         upload the web site via gh-pages   '
	@echo '                                                                          '
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html   '
	@echo 'Set the RELATIVE variable to 1 to enable relative urls                    '
	@echo '                                                                          '

html:
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)

regenerate:
	$(PELICAN) -r $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

serve:
ifdef PORT
	$(PELICAN) -l $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS) -p $(PORT)
else
	$(PELICAN) -l $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)
endif

serve-global:
ifdef SERVER
	$(PELICAN) -l $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS) -p $(PORT) -b $(SERVER)
else
	$(PELICAN) -l $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS) -p $(PORT) -b 0.0.0.0
endif


devserver:
ifdef PORT
	$(PELICAN) -lr $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS) -p $(PORT)
else
	$(PELICAN) -lr $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)
endif

$(PUBLISHDIR)/.git:
	git worktree add $(PUBLISHDIR) -B master origin/master

publish: $(PUBLISHDIR)/.git
	@cp $(PUBLISHDIR)/.git $(GIT_TMP)
	$(PELICAN) $(INPUTDIR) -o $(PUBLISHDIR) -s $(PUBLISHCONF) $(PELICANOPTS)
	@cp $(GIT_TMP) $(PUBLISHDIR)/.git
	@rm $(GIT_TMP)
	cd $(PUBLISHDIR) && git status

commit: publish
	cd $(PUBLISHDIR) && git add --all && git commit -m "Generate Pelican $(NOW)"

github: commit
	git push origin $(GITHUB_PAGES_BRANCH)

newpost:
ifdef NAME
	@echo "Title: $(NAME)" > $(POSTFILE)
	@echo "Category: $(CATEGORY)" >> $(POSTFILE)
	@echo "Date: $(DATETIME)" >> $(POSTFILE)
	@echo "" >> $(POSTFILE)
	@echo "" >> $(POSTFILE)
	@${EDITOR} ${POSTFILE}
else
	@echo 'Variable NAME is not defined.'
	@echo 'Do make newpost NAME='"'"'Post Name'"'"
endif

.PHONY: html help clean regenerate serve serve-global devserver publish commit github
