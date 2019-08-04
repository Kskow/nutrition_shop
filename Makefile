build:
	sudo docker-compose build --no-cache web
up:
	sudo docker-compose up web
bash:
	sudo docker-compose run web bash
migrate:
	sudo docker-compose run web python manage.py makemigrations && sudo docker-compose run web python manage.py migrate
test:
	sudo docker-compose run web python manage.py test app_name.tests
shell:
	sudo docker-compose run web python manage.py shell
start:
	sudo docker-compose build web && sudo docker-compose run web python manage.py makemigrations \
	&& sudo docker-compose run web python manage.py migrate && sudo docker-compose up web
requirements:
	pip-compile --output-file requirements.txt requirements.in
