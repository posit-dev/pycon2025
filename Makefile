.PHONY: setup

setup:
	uv venv .venv
	. .venv/bin/activate && uv pip install -r requirements.txt

setup-quarto:
	cd website && \
		quarto add quarto-ext/shinylive && \
		quarto add shafayetShafee/line-highlight

preview:
	quarto preview website

serve:
	make preview
