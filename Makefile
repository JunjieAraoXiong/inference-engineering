PDF ?= /Users/hansonxiong/Downloads/Inference Engineering (1).pdf

.PHONY: bootstrap extract download-readings progress

bootstrap:
	python3 scripts/bootstrap_learning_repo.py --pdf "$(PDF)"

extract:
	python3 scripts/extract_book_assets.py --pdf "$(PDF)"

download-readings:
	python3 scripts/download_readings.py --manifest readings/recommended-readings.json

progress:
	python3 scripts/progress.py
