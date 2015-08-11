null    :=
space   := $(null) #
comma   := ,

PYTHON := python2

COVERAGE := coverage
PYLINT := pylint
PYREVERSE := pyreverse
ifeq ($(PYTHON),python3)
   COVERAGE := coverage3
   PYLINT := python3-pylint
   PYREVERSE := python3-pyreverse
endif

SUBDIRS = augmenters controllers handlers sources

check:
	$(PYLINT) storage_alerts \
		--reports=no \
		--disable=I \
		--disable=abstract-class-little-used \
		--disable=abstract-class-not-used \
		--disable=duplicate-code \
		--disable=bad-continuation \
		--disable=invalid-name \
		--disable=missing-docstring \
		--disable=superfluous-parens \
		--disable=too-few-public-methods \
		--ignore-long-lines="from .* import .*"
	$(PYLINT) tests \
		--reports=no \
		--disable=I \
		--disable=bad-continuation \
		--disable=duplicate-code \
		--disable=invalid-name \
		--disable=too-few-public-methods \
		--disable=too-many-public-methods

PYREVERSE_OPTS = --output=pdf
view:
	-rm -Rf _pyreverse
	mkdir _pyreverse
	PYTHONPATH=. $(PYREVERSE) ${PYREVERSE_OPTS} --project="storage_alerts" storage_alerts
	mv classes_storage_alerts.pdf _pyreverse
	mv packages_storage_alerts.pdf _pyreverse
	for s in ${SUBDIRS}; \
	do \
		PYTHONPATH=. $(PYREVERSE) ${PYREVERSE_OPTS} --project="$${s}" storage_alerts/"$${s}"; \
		mv classes_"$${s}".pdf _pyreverse; \
		mv packages_"$${s}".pdf _pyreverse; \
	done

doc-html:
	cd doc; $(MAKE) clean html

clean:
	-rm -Rf _pyreverse

test:
	PYTHONPATH=.:tests/ $(PYTHON) -m unittest discover -v -s tests/ -p '*_test.py'

OMIT_PATHS = storage_alerts/_runner.py
OMIT_PATHS += storage_alerts/sources/journal/by_line/reader.py
OMIT = $(subst $(space),$(comma),$(strip $(OMIT_PATHS)))
coverage:
	PYTHONPATH=.:tests/ $(COVERAGE) run --timid --branch --omit="$(OMIT)" -m unittest discover -v -s tests/ -p '*_test.py'
	$(COVERAGE) report --include="storage_alerts/*"
	$(COVERAGE) html --include="storage_alerts/*"

archive:
	git archive --format tar.gz HEAD > storage_alerts.tar.gz

go:
	PYTHONPATH=. $(PYTHON) storage_alerts.py
