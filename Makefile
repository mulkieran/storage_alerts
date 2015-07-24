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
		--disable=too-few-public-methods

view:
	PYTHONPATH=. pyreverse --output=pdf storage_alerts
	mv classes_No_Name.pdf storage_alerts.pdf
	PYTHONPATH=. pyreverse --output=pdf storage_alerts/sources
	mv classes_No_Name.pdf storage_alerts_sources.pdf
	PYTHONPATH=. pyreverse --output=pdf storage_alerts/modules
	mv classes_No_Name.pdf storage_alerts_modules.pdf

doc-html:
	cd doc; $(MAKE) clean html
