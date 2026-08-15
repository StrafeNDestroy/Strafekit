.PHONY: test

test:
	uv run pytest tests/test_parser.py -v && uv run python scripts/show_sample_host.py
