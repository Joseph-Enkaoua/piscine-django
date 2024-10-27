ERROR = \033[0;31m
SUCCESS = \033[0;32m
INFO = \033[0;34m
NC = \033[0m 

DOCKER_COMPOSE = docker-compose
DOCKER = docker
PYTHON_PATH = python3

django-clean:
	@echo "$(INFO)[INFO] Cleaning up Django app$(NC)"
	@echo "----------------------------------------"
	find  ex/migrations/ -type f ! -name '__init__.py' -exec rm -f {} +

django-run:
	@echo "$(INFO)[INFO] Running Django app$(NC)"
	@echo "----------------------------------------"
	@pip3 install -r requirements.txt
	$(PYTHON_PATH) manage.py makemigrations
	$(PYTHON_PATH) manage.py migrate
	$(PYTHON_PATH) manage.py runserver

docker-clean:
	@echo "$(INFO)[INFO] Cleaning up Docker containers$(NC)"
	@echo "----------------------------------------"
	$(DOCKER_COMPOSE) down --rmi all -v --remove-orphans
	@if [ "$$( $(DOCKER) ps -aq )" ]; then \
		$(DOCKER) rm $$( $(DOCKER) ps -aq ) || true; \
	fi
	@echo "$(SUCCESS)[SUCCESS] Docker containers cleaned$(NC)"

docker-run:
	@echo "$(INFO)[INFO] Running Docker containers$(NC)"
	@echo "----------------------------------------"
	$(DOCKER_COMPOSE) up -d --build
	@echo "$(SUCCESS)[SUCCESS] Docker containers running$(NC)"
	@sleep 2

docker-logs:
	@echo "$(INFO)[INFO] Showing Docker logs$(NC)"
	@echo "----------------------------------------"
	$(DOCKER_COMPOSE) logs -f

docker-connect:
	@echo "$(INFO)[INFO] Connecting to Docker container$(NC)"
	@echo "----------------------------------------"
	$(DOCKER) exec -it postgres psql -U djangouser -d djangotraining

run: docker-run django-run

logs: docker-logs

connect: docker-connect

clean: django-clean

fclean: clean docker-clean

re : fclean run

help:
	@echo "$(INFO)	Available commands:$(NC)"
	@echo "$(INFO)	make 						-  Build and run the database and Django app$(NC)"
	@echo "$(INFO)	make clean 			-  Clean up Django app$(NC)"
	@echo "$(INFO)	make fclean			-  Clean up Docker containers and Django app$(NC)"
	@echo "$(INFO)	make re 				-  fclean and make$(NC)"
	@echo "$(INFO)	make logs 			-  Show Docker logs$(NC)"
	@echo "$(INFO)	make connect 		-  Connect to Docker container$(NC)"

.DEFAULT_GOAL := run

.DEFAULT:
	@echo "$(ERROR)[ERROR] Unknown target '$@'. Use 'make help' to see available commands.$(NC)"
	@make help

.PHONY: run clean fclean re django-clean django-run docker-clean docker-run docker-logs docker-connect

	