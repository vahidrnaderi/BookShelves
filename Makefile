.PHONY: dev
dev:
	cd aap && python3 manage.py runserver 8000

.PHONY: run
run:
	cd aap && ./init.sh

.PHONY: lint
lint:
	flake8 aap/
	isort -c aap/
	pylint aap/
	black --check aap/

.PHONY: test
test:
	python manage.py test

.PHONY: package
package:
	python -m build

.PHONY: image
image:
	docker build -t aap -f deploy/docker/Dockerfile .

.PHONY: docker-compose
docker-compose:
	docker-compose -f deploy/docker/docker-compose.yaml up
