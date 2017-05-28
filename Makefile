run:
	venv/bin/gunicorn app:app -k aiohttp.worker.GunicornWebWorker -b localhost:8081 --reload

menu:
	venv/bin/python make_menu.py

whitelist:
	venv/bin/python make_whitelist.py

create_virtualenv:
	rm -rf venv
	virtualenv -p python3.6 venv

clean_logs:
	rm -rf logs
	mkdir logs

virtualenv: create_virtualenv
	venv/bin/pip install -r requirements.txt

requirements:
	venv/bin/pip freeze > requirements.txt

test:
	venv/bin/pytest --ignore venv

.PHONY: config
config:
	cp -n config/config.template.yml config.yml
