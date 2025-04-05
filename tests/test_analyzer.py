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
