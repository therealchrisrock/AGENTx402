.PHONY: proto-gen proto-clean proto-install help

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

proto-install: ## Install protobuf tools
	pip install grpcio-tools

proto-gen: ## Generate Python code from proto files
	@echo "Generating Python code from proto files..."
	@mkdir -p gen/python
	python -m grpc_tools.protoc \
		-I./proto \
		-I/usr/local/include \
		--python_out=./gen/python \
		--grpc_python_out=./gen/python \
		--pyi_out=./gen/python \
		./proto/api/v1/*.proto
	@touch gen/__init__.py
	@touch gen/python/__init__.py
	@touch gen/python/api/__init__.py
	@touch gen/python/api/v1/__init__.py
	@echo "Proto generation complete!"

proto-clean: ## Clean generated proto files
	@echo "Cleaning generated proto files..."
	rm -rf gen/
	@echo "Clean complete!"

install: ## Install dependencies
	pip install -e .
	pip install grpcio grpcio-tools

run-backend: ## Run the backend with gRPC server
	python -m src.backend.main

run-bot: ## Run the telegram bot
	python -m src.telegram_bot.main

test-grpc: ## Test gRPC connection
	python -m src.telegram_bot.test_grpc