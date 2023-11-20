PREFIX ?= /usr/local

TEST_DIR = ~/.config/projekti

.PHONY: reset
install:
	@rm -rf "${TEST_DIR}/*"
	@echo "Resetting test directory"

.PHONY: test-with-editor
test-with-editor:
	@export EDITOR="nano"
	@python projekti init -c "${TEST_DIR}"

