#!/bin/bash
set -e

# Colors for messages
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Initializing claim-checker project...${NC}"

# Create directory structure
echo "Creating directory structure..."
mkdir -p claim_checker/{analyzer,detector,reporter,logic_gates,languages/uk,utils}
mkdir -p tests/{analyzer,detector,reporter,logic_gates,utils}
mkdir -p config/{rules,languages/uk}
mkdir -p docs
mkdir -p data/test_corpus

# Create __init__.py files
echo "Initializing Python packages..."
touch claim_checker/__init__.py
touch claim_checker/analyzer/__init__.py
touch claim_checker/detector/__init__.py
touch claim_checker/reporter/__init__.py
touch claim_checker/logic_gates/__init__.py
touch claim_checker/utils/__init__.py
touch claim_checker/languages/__init__.py
touch claim_checker/languages/uk/__init__.py

# Create basic configuration files
echo "Creating configuration files..."
cat > config/config.yaml << EOF
# Main configuration for claim_checker
version: 0.1.0
default_language: uk

modules:
  analyzer:
    enabled: true
  detector:
    enabled: true
  reporter:
    enabled: true
  logic_gates:
    enabled: true

logging:
  level: INFO
  file: logs/claim_checker.log
EOF

cat > config/languages/uk/config.yaml << EOF
# Configuration for Ukrainian language
language:
  code: uk
  name: Ukrainian
  resources:
    dictionaries:
      - emotional_words
      - intensifiers
      - hedges
    models:
      - tokenizer
      - lemmatizer
      - pos_tagger
      - ner
EOF

cat > config/rules/logical_fallacies.yaml << EOF
# Rules for detecting logical fallacies
rules:
  ad_hominem:
    description: "Attack on the person instead of the argument"
    patterns:
      - "{person} doesn't understand"
      - "{person} doesn't know"
    severity: high

  false_dichotomy:
    description: "False dichotomy (black and white thinking)"
    patterns:
      - "either {option1}, or {option2}"
      - "if not {option1}, then {option2}"
    severity: medium
EOF

# Create main module files
echo "Creating main module files..."

cat > claim_checker/__main__.py << EOF
#!/usr/bin/env python3
"""
Main module for running claim_checker.
"""
from claim_checker.cli import app

if __name__ == "__main__":
    app()
EOF

cat > claim_checker/cli.py << EOF
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
EOF

cat > claim_checker/config.py << EOF
#!/usr/bin/env python3
"""
Module for working with claim_checker configuration.
"""
import os
from pathlib import Path
from typing import Dict, Any

import yaml

def get_config_dir() -> Path:
    """Returns the path to the configuration directory."""
    # First check environment variable
    config_dir = os.environ.get("CLAIM_CHECKER_CONFIG_DIR")
    if config_dir:
        return Path(config_dir)

    # If not found, use the standard path
    return Path(__file__).parent.parent / "config"

def load_config() -> Dict[str, Any]:
    """Loads the main configuration and language resources."""
    config_dir = get_config_dir()
    config_path = config_dir / "config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # Load language resources
    default_language = config.get("default_language", "uk")
    language_config_path = config_dir / "languages" / default_language / "config.yaml"

    if language_config_path.exists():
        with open(language_config_path, "r", encoding="utf-8") as f:
            language_config = yaml.safe_load(f)
            config["language"] = language_config.get("language", {})

    return config
EOF

cat > claim_checker/core.py << EOF
#!/usr/bin/env python3
"""
Core module for claim_checker that coordinates the analysis process.
"""
from pathlib import Path
from typing import Dict, Any, Union

from claim_checker.analyzer.analyzer import Analyzer
from claim_checker.detector.detector import Detector
from claim_checker.reporter.reporter import Reporter
from claim_checker.logic_gates.pipeline import LogicPipeline

def analyze_text(text: str, language: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyzes text for logical fallacies and bias.

    Args:
        text: Text to analyze
        language: Language code
        config: System configuration

    Returns:
        Dictionary with analysis results
    """
    # Initialize main components
    analyzer = Analyzer(language, config)
    detector = Detector(language, config)
    reporter = Reporter(language, config)
    pipeline = LogicPipeline(config)

    # Analyze text
    analysis_result = analyzer.analyze(text)
    detection_result = detector.detect(text, analysis_result)

    # Apply logic rules
    processed_result = pipeline.process(detection_result)

    # Generate report
    report = reporter.generate_report(processed_result)

    return report

def analyze_file(file_path: Path, language: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyzes a file for logical fallacies and bias.

    Args:
        file_path: Path to the file
        language: Language code
        config: System configuration

    Returns:
        Dictionary with analysis results
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    return analyze_text(text, language, config)
EOF

# Create stubs for main module classes
mkdir -p claim_checker/{analyzer,detector,reporter,logic_gates}

cat > claim_checker/analyzer/analyzer.py << EOF
#!/usr/bin/env python3
"""
Text analyzer module.
"""
from typing import Dict, Any

class Analyzer:
    """
    Class for analyzing linguistic characteristics of text.
    """

    def __init__(self, language: str, config: Dict[str, Any]):
        """
        Initializes the analyzer for a specific language.

        Args:
            language: Language code
            config: System configuration
        """
        self.language = language
        self.config = config

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyzes text and returns linguistic characteristics.

        Args:
            text: Text to analyze

        Returns:
            Dictionary with analysis results
        """
        # Stub for MVP
        return {
            "text_length": len(text),
            "language": self.language,
            "emotional_language": [],
            "readability": {
                "score": 0,
                "level": "unknown"
            },
            "metadata": {}
        }
EOF

cat > claim_checker/detector/detector.py << EOF
#!/usr/bin/env python3
"""
Logical fallacy detector module.
"""
from typing import Dict, Any

class Detector:
    """
    Class for detecting logical fallacies and unsupported claims.
    """

    def __init__(self, language: str, config: Dict[str, Any]):
        """
        Initializes the detector for a specific language.

        Args:
            language: Language code
            config: System configuration
        """
        self.language = language
        self.config = config

    def detect(self, text: str, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detects logical fallacies and unsupported claims in text.

        Args:
            text: Text to analyze
            analysis_result: Results of linguistic analysis

        Returns:
            Dictionary with detection results
        """
        # Stub for MVP
        return {
            "logical_fallacies": [],
            "unsupported_claims": [],
            "consistency_issues": [],
            "references": []
        }
EOF

cat > claim_checker/reporter/reporter.py << EOF
#!/usr/bin/env python3
"""
Report generator module.
"""
from typing import Dict, Any

class Reporter:
    """
    Class for generating reports based on analysis results.
    """

    def __init__(self, language: str, config: Dict[str, Any]):
        """
        Initializes the report generator for a specific language.

        Args:
            language: Language code
            config: System configuration
        """
        self.language = language
        self.config = config

    def generate_report(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a report based on analysis results.

        Args:
            results: Analysis results

        Returns:
            Report as a dictionary
        """
        # Stub for MVP
        return {
            "summary": {
                "issues_count": 0,
                "overall_score": 100,
                "recommendations": []
            },
            "details": results,
            "visualizations": {}
        }
EOF

cat > claim_checker/logic_gates/pipeline.py << EOF
#!/usr/bin/env python3
"""
Logic pipeline module for processing results.
"""
from typing import Dict, Any

class LogicPipeline:
    """
    Class for applying logic rules to analysis results.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the logic pipeline.

        Args:
            config: System configuration
        """
        self.config = config

    def process(self, detection_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes detection results using logic rules.

        Args:
            detection_result: Detection results

        Returns:
            Processed results
        """
        # Stub for MVP
        return detection_result
EOF

# Create tests
mkdir -p tests
cat > tests/test_analyzer.py << EOF
#!/usr/bin/env python3
"""
Tests for the analyzer module.
"""
import pytest
from claim_checker.analyzer.analyzer import Analyzer

def test_analyzer_initialization():
    """Test analyzer initialization."""
    analyzer = Analyzer("uk", {})
    assert analyzer.language == "uk"

def test_analyzer_simple_analysis():
    """Test simple text analysis."""
    analyzer = Analyzer("uk", {})
    result = analyzer.analyze("Test text")
    assert "text_length" in result
    assert result["text_length"] == 9
EOF

# Set executable permissions
chmod +x claim_checker/__main__.py
chmod +x claim_checker/cli.py

echo -e "${GREEN}Project structure successfully created!${NC}"
echo "To install dependencies, run:"
echo "uv pip install -e ."
echo "To run tests, run:"
echo "pytest"