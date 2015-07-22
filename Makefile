check:
	pylint storage_alerts tests \
		--reports=no \
		--disable=I \
		--disable=invalid-name
