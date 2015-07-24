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
	PYTHONPATH=. pyreverse --output=pdf storage_alerts
	mv classes_No_Name.pdf storage_alerts.pdf
	PYTHONPATH=. pyreverse --output=pdf storage_alerts/examples
	mv classes_No_Name.pdf storage_alerts_examples.pdf
	PYTHONPATH=. pyreverse --output=pdf storage_alerts/handling
	mv classes_No_Name.pdf storage_alerts_handling.pdf
	PYTHONPATH=. pyreverse --output=pdf storage_alerts/sources
	mv classes_No_Name.pdf storage_alerts_sources.pdf

doc-html:
	cd doc; $(MAKE) clean html
