PY			=	venv/bin/python
RM			=	rm -rf
FK			=	flake8
MP			=	mypy

.PHONY: config install run debug lint lint-strict init-venv atv-venv \
	depend remove-venv clean fclean

config:
	@apt install python3.10-venv

install: init-venv
	@$(PY) -m pip install --upgrade pip
	@$(PY) -m pip install -r requirements.txt

run:
	$(PY) -m a_maze_ing config.txt

debug:
	$(PY) -m pdb -m a_maze_ing config.txt

lint:
	@$(FK) --exclude=venv .
	@$(MP) --exclude venv --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	@$(FK) --exclude=venv .
	@$(MP) --exclude venv --strict .

init-venv:
	@python -m venv venv --copies

atv-venv:
	@echo "source venv/bin/activate"

depend: install

remove-venv:
	$(RM) venv/

clean:
	@find . -name "__pycache__" -type d -exec $(RM) {} +
	$(RM) .mypy_cache

fclean: clean remove-venv
