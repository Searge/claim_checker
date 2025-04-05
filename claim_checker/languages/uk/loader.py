#!/usr/bin/env python3
"""
Module for loading Ukrainian language resources.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class UkrainianResourceLoader:
    """
    Loads dictionaries and resources for Ukrainian language analysis.
    """

    def __init__(self) -> None:
        """Initialize the loader with paths to resources."""
        self.resource_dir = Path(__file__).parent
        self.dict_dir = self.resource_dir / "dictionaries"

    def load_emotional_words(self) -> Dict[str, Tuple[int, int]]:
        """
        Load emotional words dictionary.

        Returns:
            Dictionary with word as key and tuple of (intensity, polarity) as value
        """
        result = {}
        dict_path = self.dict_dir / "emotional_words.txt"

        if not dict_path.exists():
            return result

        with open(dict_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                parts = line.split(",")
                if len(parts) == 3:
                    word, intensity_str, polarity_str = parts
                    try:
                        result[word] = (int(intensity_str), int(polarity_str))
                    except ValueError:
                        # Skip invalid entries
                        pass

        return result

    def load_intensifiers(self) -> Dict[str, int]:
        """
        Load intensifiers dictionary.

        Returns:
            Dictionary with word as key and intensity level as value
        """
        result = {}
        dict_path = self.dict_dir / "intensifiers.txt"

        if not dict_path.exists():
            return result

        with open(dict_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                parts = line.split(",")
                if len(parts) == 2:
                    word, intensity_str = parts
                    try:
                        result[word] = int(intensity_str)
                    except ValueError:
                        # Skip invalid entries
                        pass

        return result

    def load_hedges(self) -> Dict[str, int]:
        """
        Load hedges dictionary.

        Returns:
            Dictionary with phrase as key and uncertainty level as value
        """
        result = {}
        dict_path = self.dict_dir / "hedges.txt"

        if not dict_path.exists():
            return result

        with open(dict_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                parts = line.split(",")
                if len(parts) == 2:
                    phrase, uncertainty_str = parts
                    try:
                        result[phrase] = int(uncertainty_str)
                    except ValueError:
                        # Skip invalid entries
                        pass

        return result

    def load_logical_patterns(self) -> Dict[str, List[str]]:
        """
        Load logical fallacy patterns.

        Returns:
            Dictionary with fallacy type as key and list of patterns as value
        """
        result = {}
        dict_path = self.dict_dir / "logical_patterns.txt"

        if not dict_path.exists():
            return result

        with open(dict_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                parts = line.split(",", 1)
                if len(parts) == 2:
                    fallacy_type, pattern = parts
                    if fallacy_type not in result:
                        result[fallacy_type] = []
                    result[fallacy_type].append(pattern)

        return result

    def load_all(self) -> Dict[str, Any]:
        """
        Load all dictionaries.

        Returns:
            Dictionary with resources
        """
        return {
            "emotional_words": self.load_emotional_words(),
            "intensifiers": self.load_intensifiers(),
            "hedges": self.load_hedges(),
            "logical_patterns": self.load_logical_patterns(),
        }
