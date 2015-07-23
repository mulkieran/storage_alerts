check:
	pylint storage_alerts tests \
		--reports=no \
		--disable=I \
		--disable=abstract-class-little-used \
		--disable=abstract-class-not-used \
		--disable=invalid-name \
		--disable=missing-docstring \
		--disable=too-few-public-methods
