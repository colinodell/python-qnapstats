# AGENTS.md

This file provides guidance to AI coding agents working with code in this repository.

## Overview

`qnapstats` is a small Python library that reads system information (CPU, memory, NICs, fans, volumes, SMART health, bandwidth, firmware) from QNAP NAS devices running QTS, by calling the NAS's CGI endpoints and parsing their XML responses. Supported Python: 3.7 through 3.15 (`python_requires='>=3.7'`), so avoid syntax newer than 3.7 (no walrus operator, no `match`, etc.).

## Commands

CI runs `tox` with one env per Python version; each env runs these in order, and any failure fails the build:

```bash
export PYTHONPATH=.:qnapstats LANG=C.UTF-8
flake8                          # max line length 120 (tox.ini)
pylint qnapstats                # config in pylintrc
pydocstyle qnapstats
python tests/test-models.py     # the whole test suite
python setup.py check --restructuredtext --strict   # tox "desc" env: README.rst must be valid RST
```

Or run everything for one version with `tox -e py39`.

There is no test runner: `tests/test-models.py` is a plain script of top-level `assert`s, so it stops at the first failure and has no way to select a single test. To narrow down a failure, temporarily filter `models` in that script or reproduce the call in a REPL.

`debug.py` prompts for credentials and calls every public method in debug mode against a real NAS — useful for capturing XML responses for new fixtures.

## Architecture

Everything lives in the `QNAPStats` class in `qnapstats/qnap_stats.py`:

- **Session/auth:** `_init_session` lazily logs in via `authLogin.cgi` (POST first, falling back to GET; the password is base64-encoded) and stores the `authSid`. Every later request appends `sid=<sid>`. A response with `authPassed == "0"` sets `_session_error`, which forces a new login on the next call.
- **Requests:** public `get_*` methods call `_get_url` (which retries once on failure) or `_execute_post_url`, and `_handle_response` returns the parsed `QDocRoot` dict, or `None` for non-200 or non-`text/xml` responses. Public methods return `None` when the NAS gives no usable data.
- **XML parsing:** responses go through `xmltodict`, so a repeated element becomes a list but a single one becomes a dict. Pass `force_list=` for elements that can appear once or many times.
- **Firmware differences:** QTS versions and models return different fields. Many keys are numbered per item (e.g. `eth_ip1`, `sysfan2`, driven by a `*_count` field), and fields can be missing on some devices. Prefer `.get()` and skipping incomplete entries over indexing that raises `KeyError`. `get_bandwidth` falls back from the `QSM40bandwidth` API to the legacy `bandwidth` API.

## Tests and fixtures

`tests/responses/<MODEL>-<FIRMWARE>/` holds one directory per captured device. `add_mock_responses` registers each `<name>.xml` present (e.g. `systemstats.xml`) with `responses` at a fixed URL, and the matching `<name>.json` is the expected output, compared as `json.dumps(result, sort_keys=True)`, with no trailing newline in the file. `login.xml` must return `authSid` `12345`, since the mocked URLs hard-code `sid=12345`. Any directory in `tests/responses` is picked up automatically.

When a change alters a method's output (e.g. a new key in `get_system_stats`), regenerate the affected `.json` fixtures in every model directory; a missed fixture fails CI.

## Releases

Releases are automated by semantic-release (`.releaserc.json`, `.github/workflows/release.yaml`) on every push to `master`:

- Only conventional-commit prefixes create releases and release notes: `fix:` (patch), `feat:` (minor). Commits without a prefix ship in the next release but are left out of its notes. Use `docs:`, `ci:`, `chore:`, etc. for changes that shouldn't release.
- semantic-release writes the version into `setup.py` and commits it with `CHANGELOG.md`. Don't bump the version by hand.
- The `publish` job uploads to PyPI with trusted publishing (no API token). If an upload fails, use "Re-run failed jobs", or run the Release workflow manually with a `tag` input to publish an existing tag.

README.rst has a Device Support table; update it when adding a tested model.
