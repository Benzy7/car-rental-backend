# Python environment
PYTHON = python3
PIP = pip3
VENV = ../env

activate:
	@echo "Activating virtual environment..."
	. $(VENV)/bin/activate

run:
	@echo "Running Django development server..."
	. $(VENV)/bin/activate && $(PYTHON) manage.py runserver --settings=skyCarManager.settings.dev

test:
	@echo "Running Django tests..."
	. $(VENV)/bin/activate && $(PYTHON) manage.py test --settings=skyCarManager.settings.dev

makemigrations:
	@echo "Making migrations..."
	. $(VENV)/bin/activate && $(PYTHON) manage.py makemigrations --settings=skyCarManager.settings.dev

migrate:
	@echo "Applying migrations..."
	. $(VENV)/bin/activate && $(PYTHON) manage.py migrate --settings=skyCarManager.settings.dev

mergemigrations:
	@echo "Merging migrations..."
	. $(VENV)/bin/activate && $(PYTHON) manage.py makemigrations --merge --settings=skyCarManager.settings.dev

freezereq:
	@echo "Freezing requirements..."
	. $(VENV)/bin/activate && pip list --format=freeze > requirements.txt

installreq:
	@echo "Installing requirements..."
	. $(VENV)/bin/activate && pip install -r requirements.txt
