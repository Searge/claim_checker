#!/usr/bin/env python3
"""
Command-line interface for claim_checker.
"""

from pathlib import Path
from typing import Optional

import typer

from claim_checker.config import load_config
from claim_checker.core import analyze_file, analyze_text

# Create the main app
app = typer.Typer(help="Tool for analyzing text for logical fallacies and bias")


# Define the analyze command
@app.command()
def analyze(
    text: Optional[str] = typer.Option(None, "--text", "-t", help="Text to analyze"),
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="File to analyze"),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Path to save the report"
    ),
    language: str = typer.Option(
        "uk", "--language", "-l", help="Analysis language (default: uk)"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Analyzes text or file for logical fallacies, bias, and unsupported claims."""
    config = load_config()

    if text:
        result = analyze_text(text, language, config)
        typer.echo(
            f"Analysis completed. Found {result['summary']['issues_count']} issues."
        )
    elif file and file.exists():
        result = analyze_file(file, language, config)
        typer.echo(
            f"Analysis of {file} completed. Found {result['summary']['issues_count']} issues."
        )
    else:
        typer.echo("You must specify either text (--text) or file (--file) to analyze")
        raise typer.Exit(1)

    if output:
        # Save result to file
        typer.echo(f"Report saved to {output}")
    else:
        # Print result to console in simplified format
        typer.echo("Analysis results:")
        typer.echo(f"- Score: {result['summary']['overall_score']}/100")
        if result["summary"]["recommendations"]:
            typer.echo("- Recommendations:")
            for rec in result["summary"]["recommendations"]:
                typer.echo(f"  * {rec}")
        else:
            typer.echo("- No recommendations at this time.")


# Create a default command that mimics analyze to maintain backwards compatibility
@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    text: Optional[str] = typer.Option(None, "--text", "-t", help="Text to analyze"),
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="File to analyze"),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Path to save the report"
    ),
    language: str = typer.Option(
        "uk", "--language", "-l", help="Analysis language (default: uk)"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Main entry point that forwards to analyze command when no subcommand is specified."""
    if ctx.invoked_subcommand is None and (text or file):
        analyze(text=text, file=file, output=output, language=language, verbose=verbose)


if __name__ == "__main__":
    app()
