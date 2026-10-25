install:
	@pip install uv
	@uv sync

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
