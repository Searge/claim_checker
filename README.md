# claim_checker

A tool for analyzing text to identify potential issues with logic, bias, and factual accuracy.

## Overview

`claim_checker` is a tool that performs preliminary analysis of text to identify potential problems with logic, bias, and factual accuracy. The system conducts preliminary analysis without making definitive judgments, instead highlighting areas that may require critical examination by human users.

## Features

- Modular architecture with clear separation between language-specific and language-agnostic components
- Initial support for Ukrainian language with a framework for multi-language capabilities
- Detection of common logical fallacies, emotional manipulation, and unsupported claims
- Presentable analysis results with visualizations
- YAML-based configuration for all settings and resources

## Installation

```bash
# Clone the repository
git clone https://github.com/searge/claim_checker.git
cd claim_checker

# Set up virtual environment
pyenv local 3.13  # or any Python version >= 3.10
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -e .
```

## Quick Start

### Project Initialization

```bash
# Run the initialization script
chmod +x init_project.sh
./init_project.sh
```

### Usage

```bash
# Analyze text
claim_checker analyze --text "Text to analyze"

# Analyze file
claim_checker analyze --file path/to/file.txt

# Save results to a file
claim_checker analyze --file path/to/file.txt --output result.json
```

## Project Structure

```txt
claim_checker/
├── claim_checker/           # Main package
│   ├── analyzer/            # Analyzer module
│   │   └── analyzer.py      # Analyzer class
│   ├── detector/            # Detector module
│   │   └── detector.py      # Detector class
│   ├── reporter/            # Reporter module
│   │   └── reporter.py      # Report generator class
│   ├── logic_gates/         # Logic rules module
│   │   └── pipeline.py      # Logic pipeline class
│   ├── languages/           # Language resources
│   │   └── uk/              # Ukrainian language
│   ├── utils/               # Utilities
│   ├── __main__.py          # Entry point
│   ├── cli.py               # Command-line interface
│   ├── config.py            # Configuration handling
│   └── core.py              # Core logic
├── config/                  # Configuration files
│   ├── config.yaml          # Main configuration
│   ├── rules/               # Analysis rules
│   │   └── logical_fallacies.yaml  # Rules for logical fallacies
│   └── languages/           # Language configurations
│       └── uk/              # Ukrainian language
│           └── config.yaml  # Ukrainian language configuration
├── data/                    # Test data
│   └── test_corpus/         # Test corpus
├── docs/                    # Documentation
├── tests/                   # Tests
│   └── test_analyzer.py     # Tests for analyzer
├── pyproject.toml           # Project configuration file
├── init_project.sh          # Project initialization script
└── README.md                # Project documentation
```

## Architecture

### Core Modules

1. **analyzer** - linguistic analysis of text
   - Emotional language
   - Readability
   - Text statistics

2. **detector** - detection of problematic areas
   - Logical fallacies
   - Unsupported claims
   - Consistency checking

3. **reporter** - report generation
   - Result aggregation
   - Visualization
   - Report formatting

4. **logic_gates** - logical rules pipeline
   - Rule configuration
   - Threshold settings
   - Custom rules

## Multi-language Support

The project is designed for multi-language support with initial implementation for Ukrainian:

- Language-specific resources stored in `claim_checker/languages/{language_code}/`
- Language-agnostic analysis algorithms
- Language detection for mixed-language documents

## Development

### Development Setup

```bash
# Install development dependencies
uv pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black claim_checker tests
isort claim_checker tests
```

### Type Checking

```bash
mypy claim_checker tests
```

### Linting

```bash
ruff claim_checker tests
```

## Limitations

- The tool does not determine absolute truth or falsehood
- Analysis accuracy varies depending on text complexity and domain
- The system supplements but cannot replace human critical thinking
- Initial language support limited to Ukrainian with framework for expansion
- Limited ability to understand deep context or specialized domains

## License

MIT
