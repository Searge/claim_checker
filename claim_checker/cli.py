#!/usr/bin/env python3
"""
Command-line interface for claim_checker.
"""
import typer
from pathlib import Path

from claim_checker.config import load_config
from claim_checker.core import analyze_text, analyze_file

app = typer.Typer(help="Tool for analyzing text for logical fallacies and bias")

@app.command()
def analyze(
    text: str = typer.Option(None, "--text", "-t", help="Text to analyze"),
    file: Path = typer.Option(None, "--file", "-f", help="File to analyze"),
    output: Path = typer.Option(None, "--output", "-o", help="Path to save the report"),
    language: str = typer.Option("uk", "--language", "-l", help="Analysis language (default: uk)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """Analyzes text or file for logical fallacies, bias, and unsupported claims."""
    config = load_config()

    if text:
        result = analyze_text(text, language, config)
    elif file and file.exists():
        result = analyze_file(file, language, config)
    else:
        typer.echo("You must specify either text (--text) or file (--file) to analyze")
        raise typer.Exit(1)

    if output:
        # Save result to file
        pass
    else:
        # Print result to console
        pass

if __name__ == "__main__":
    app()
