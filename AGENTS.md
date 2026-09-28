# Notes for AI coding agents

This project follows NumPy's AI policy:
https://numpy.org/devdocs/dev/ai_policy.html

In practice:

- Do not open pull requests, file issues, or post comments on your own. A human
  must review all generated code and submit it themselves.
- Do not write issue text, PR descriptions, or review replies for the human to
  post. They must write those themselves (AI help with translation or grammar is
  fine).
- Remind the human that the PR must disclose AI use: which tools, how they were
  used, and which code or text they generated.
- Keep changes small and focused, and make sure the human understands them.

## Development

- Install: `pip install -e . --group test` (or `--group dev` for docs and
  pre-commit too)
- Run tests: `pytest numpydoc`
- Lint/format: `pre-commit run --all-files`
