front:
	cd frontend ; npm run dev --host

dev:
	docker-compose -f dev.yml up --build --force-recreate --no-deps

prod:
	docker-compose -f prod.yml up --build --force-recreate --no-deps

stop:
	docker-compose down ; docker image prune -f

ma:
	docker exec -it Django_API sh -c "python manage.py makemigrations"

mi:
	docker exec -it Django_API sh -c "python manage.py migrate"

su:
	cd backend; . venv/Scripts/activate; python manage.py createsuperuser

fr:
	cd backend; . venv/Scripts/activate; pip freeze > requirements.txt

in:
	cd backend; . venv/Scripts/activate; pip install -r requirements.txt

exec:
	docker exec -it Django_API sh

admin:
	python manage.py createsuperuser
