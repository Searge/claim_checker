#!/usr/bin/env python3
"""
Tests for Ukrainian language resources.
"""
import pytest

from claim_checker.languages.uk.loader import UkrainianResourceLoader


def test_emotional_words_loading():
    """Test loading emotional words dictionary."""
    loader = UkrainianResourceLoader()
    emotional_words = loader.load_emotional_words()
    assert len(emotional_words) > 0
    # Check a specific word
    assert "чудовий" in emotional_words
    # Check the format (intensity, polarity)
    intensity, polarity = emotional_words["чудовий"]
    assert isinstance(intensity, int)
    assert polarity in (-1, 1)


def test_intensifiers_loading():
    """Test loading intensifiers dictionary."""
    loader = UkrainianResourceLoader()
    intensifiers = loader.load_intensifiers()
    assert len(intensifiers) > 0
    # Check a specific intensifier
    assert "дуже" in intensifiers
    # Check the value is an integer
    assert isinstance(intensifiers["дуже"], int)


def test_hedges_loading():
    """Test loading hedges dictionary."""
    loader = UkrainianResourceLoader()
    hedges = loader.load_hedges()
    assert len(hedges) > 0
    # Check a specific hedge
    assert "можливо" in hedges
    # Check the value is an integer
    assert isinstance(hedges["можливо"], int)


def test_logical_patterns_loading():
    """Test loading logical fallacy patterns."""
    loader = UkrainianResourceLoader()
    patterns = loader.load_logical_patterns()
    assert len(patterns) > 0
    # Check specific fallacy types
    assert "ad_hominem" in patterns
    assert "false_dichotomy" in patterns
    # Check patterns are stored as lists
    assert isinstance(patterns["ad_hominem"], list)
    assert len(patterns["ad_hominem"]) > 0
