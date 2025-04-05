#!/usr/bin/env python3
"""
Module for working with claim_checker configuration.
"""
import os
from pathlib import Path
from typing import Any, Dict, Optional

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
        config = yaml.safe_load(f) or {}  # Ensure we don't get None

    # Load language resources
    default_language = config.get("default_language", "uk")
    language_config_path = config_dir / "languages" / default_language / "config.yaml"

    if language_config_path.exists():
        with open(language_config_path, "r", encoding="utf-8") as f:
            language_config = yaml.safe_load(f) or {}
            config["language"] = language_config.get("language", {})

    return config
