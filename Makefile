help:
	@echo "Commands:"
	@echo "  test: do unittests"
	@echo "  clean: clean project/"

test:
	python -m unittest discover -s tests/

clean:
	@find . -name \#* | xargs rm
