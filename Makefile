PYTHON ?= python
PIP ?= pip
USER_ID ?= 1

.PHONY: help install dev-install run run-bypass quiz chatbot voice test

help:
	@echo Available commands:
	@echo   make install       - Install runtime dependencies
	@echo   make dev-install   - Install runtime and development dependencies
	@echo   make run           - Launch the main Lumina app
	@echo   make run-bypass    - Launch the app and bypass login with USER_ID
	@echo   make quiz          - Launch the standalone quiz demo
	@echo   make chatbot       - Launch the CLI chatbot demo
	@echo   make voice         - Launch the voice chat demo
	@echo   make test          - Run the test suite

install:
	$(PIP) install -r requirements.txt

dev-install:
	$(PIP) install -r dev-requirements.txt

run:
	$(PYTHON) main.py

run-bypass:
	$(PYTHON) main.py --bypass $(USER_ID)

quiz:
	$(PYTHON) frontend/quiz/quiz.py

chatbot:
	$(PYTHON) backend/ChatBot/main.py

voice:
	$(PYTHON) backend/ChatBot/voicechat_screen.py

test:
	$(PYTHON) -m pytest
