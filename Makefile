SUBDIRS = augmenters controllers examples handlers sources

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
