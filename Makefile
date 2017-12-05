default: help
help:
	@echo "Please use \`make <target>' where <target> is one of:"
	@echo "  help         to show this message"
	@echo "  lint         to run flake8 and pylint"
	@echo "  test-setup   to install dependencies"


test-setup:
	pip install --upgrade pip
	pip install -r requirements.txt

lint:
	pycodestyle --ignore=E402,E722 --max-line-length=160 . sop

.PHONY: help lint test-setup
