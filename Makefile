.PHONY: clean
clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;

.PHONY: install
install: clean
	@pip install -r requirements.txt

.PHONY: run
run:
	python run.py

.PHONY: test
test:
	@nosetests -v --with-coverage --cover-package=cep_api --cover-package=commons