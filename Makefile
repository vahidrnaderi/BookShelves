.PHONY: run
run:
	python manage.py runserver :8000

.PHONY: lint
lint:
	flake8 .
	pylint .
	black -C .

.PHONY: test
test:
	python manage.py test

.PHONY: package
package:
	python -m build