null    :=
space   := $(null) #
comma   := ,

SUBDIRS = augmenters controllers handlers sources

check:
	pylint storage_alerts tests \
		--reports=no \
		--disable=I \
		--disable=abstract-class-little-used \
		--disable=abstract-class-not-used \
		--disable=bad-continuation \
		--disable=duplicate-code \
		--disable=invalid-name \
		--disable=missing-docstring \
		--disable=superfluous-parens \
		--disable=too-few-public-methods

PYREVERSE_OPTS = --output=pdf
view:
	-rm -Rf _pyreverse
	mkdir _pyreverse
	PYTHONPATH=. pyreverse ${PYREVERSE_OPTS} --project="storage_alerts" storage_alerts
	mv classes_storage_alerts.pdf _pyreverse
	mv packages_storage_alerts.pdf _pyreverse
	for s in ${SUBDIRS}; \
	do \
		PYTHONPATH=. pyreverse ${PYREVERSE_OPTS} --project="$${s}" storage_alerts/"$${s}"; \
		mv classes_"$${s}".pdf _pyreverse; \
		mv packages_"$${s}".pdf _pyreverse; \
	done

doc-html:
	cd doc; $(MAKE) clean html

clean:
	-rm -Rf _pyreverse

test:
	PYTHONPATH=.:tests/ python -m unittest discover -v -s tests/ -p '*_test.py'

OMIT_PATHS = storage_alerts/_runner.py
OMIT_PATHS += storage_alerts/controllers/time.py
OMIT_PATHS += storage_alerts/sources/generic/scanner.py
OMIT_PATHS += storage_alerts/sources/journal/by_line/reader.py
OMIT = $(subst $(space),$(comma),$(strip $(OMIT_PATHS)))
coverage:
	PYTHONPATH=.:tests/ coverage run --timid --branch --omit="$(OMIT)" -m unittest discover -v -s tests/ -p '*_test.py'
	coverage report --include="storage_alerts/*"
	coverage html --include="storage_alerts/*"
