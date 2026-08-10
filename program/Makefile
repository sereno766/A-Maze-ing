NAME		=	"A-Maze-ing"
PY			=	venv/bin/python
RM			=	rm -rf
FK			=	flake8
MP			=	mypy


DEFAULT		=	\033[0m
RED			=	\033[1;31m
CYAN		=	\033[1;36m
PINK		=	\033[1;35m
GREEN		=	\033[1;32m
YELLOW		=	\033[1;33m
REWHITE		=	\033[1;7;97m
RECYAN		=	\033[1;7;36m
REPINK		=	\033[1;7;35m
RERED		=	\033[1;7;31m
REGREEN		=	\033[1;7;32m
REYELLOW	=	\033[1;7;33m

config:
	@apt install python3.10-venv

install:

run:
	$(PY) -m a_maze_ing config.txt --debug

debug:

lint:
	@$(FK) .
	@$(MP) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	@$(FK) .
	@$(MP) --strict .

init-venv:
	@python -m venv venv --copies

atv-venv:
	@echo "source venv/bin/activate"

depend:
	@pip install -r requirements.txt

remove-venv:
	$(RM) venv/

clean:
	@find . -name "__pycache__" -type d -exec $(RM) {} +
	$(RM) .mypy_cache

fclean: clean remove-venv
