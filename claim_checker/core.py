#!/usr/bin/env python3
"""
Core module for claim_checker that coordinates the analysis process.
"""
from pathlib import Path
from typing import Any, Dict, Union

from claim_checker.analyzer.analyzer import Analyzer
from claim_checker.detector.detector import Detector
from claim_checker.logic_gates.pipeline import LogicPipeline
from claim_checker.reporter.reporter import Reporter


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


def analyze_file(
    file_path: Path, language: str, config: Dict[str, Any]
) -> Dict[str, Any]:
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
