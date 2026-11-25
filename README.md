# Taskboard

A small command-line task tracker (Python 3.12, SQLite, pytest)

    python -m taskboard.cli add "Write report" --priority 1 --due 2026-12-01
    python -m taskboard.cli list
    python -m taskboard.cli done 1
    python -m taskboard.cli search report

## Tests

    pip install -r requirements-dev.txt
    python -m pytest --cov=taskboard --cov-report=xml:coverage.xml

## Baseline

Baseline version: initial commit (tag `baseline`). Used for SECU/CSCN73010 Assignment 3.
