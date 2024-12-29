ERROR = \033[0;31m
SUCCESS = \033[0;32m
INFO = \033[0;34m
NC = \033[0m 

PYTHON_PATH = python3

django-clean:
	@if docker container inspect -f '{{.State.Running}}' redis 2>/dev/null | grep -q true; then \
		echo "$(INFO)[INFO] Stopping Redis container$(NC)"; \
		docker stop redis; \
	else \
		echo "$(INFO)[INFO] Redis container was not found$(NC)"; \
	fi

django-run:
	@if docker container inspect -f '{{.State.Running}}' redis 2>/dev/null | grep -q true; then \
		echo "$(INFO)[INFO] Redis is already running$(NC)"; \
	else \
		echo "$(INFO)[INFO] Starting Redis instance$(NC)"; \
		docker run -d --rm -p 6379:6379 --name redis redis:7; \
	fi
	@echo "$(INFO)[INFO] Running Django app$(NC)"
	@echo "----------------------------------------"
	pip3 install -r requirements.txt
	$(PYTHON_PATH) ./d09/manage.py makemigrations account chat
	$(PYTHON_PATH) ./d09/manage.py migrate
	sleep 1
	$(PYTHON_PATH) ./d09/manage.py populate
	$(PYTHON_PATH) ./d09/manage.py runserver

data-clean:
	@if [ -e ./d09/db.sqlite3 ]; then \
		rm ./d09/db.sqlite3; \
		echo "$(INFO)[INFO] Deleted ./d09/db.sqlite3$(NC)"; \
	else \
		echo "$(INFO)[INFO] ./d09/db.sqlite3 not found, skipping deletion$(NC)"; \
	fi


run: django-run

clean: django-clean

fclean: clean data-clean

re : fclean run

help:
	@echo "$(INFO)	Available commands:$(NC)"
	@echo "$(INFO)	make 				-  Build and run the Django app$(NC)"
	@echo "$(INFO)	make clean 			-  Clean up Django app$(NC)"
	@echo "$(INFO)	make fclean			-  Clean up data and Django app$(NC)"
	@echo "$(INFO)	make re 			-  fclean and make$(NC)"

.DEFAULT_GOAL := run

.DEFAULT:
	@echo "$(ERROR)[ERROR] Unknown target '$@'. Use 'make help' to see available commands.$(NC)"
	@make help

.PHONY: run clean fclean re django-clean django-run
