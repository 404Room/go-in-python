help:
	@echo "Commands:"
	@echo "  test: do unittests"

test:
	python -m unittest discover -s tests/
