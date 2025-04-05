#!/usr/bin/env python3
"""
Enhanced detector module that uses Ukrainian dictionaries.
"""

import re
from typing import Any, Dict, List, Optional, Set, Tuple

from claim_checker.languages.uk.loader import UkrainianResourceLoader


class EnhancedDetector:
    """
    Enhanced class for detecting logical fallacies and unsupported claims
    using Ukrainian language dictionaries.
    """

    def __init__(self, language: str, config: Dict[str, Any]) -> None:
        """
        Initializes the detector for a specific language.

        Args:
            language: Language code
            config: System configuration
        """
        self.language = language
        self.config = config

        # Load language resources if it's Ukrainian
        self.resources = {}
        if language == "uk":
            loader = UkrainianResourceLoader()
            self.resources = loader.load_all()

        # Prepare pattern variables
        self.emotion_threshold = 7  # Words with intensity >= this level are flagged
        self.hedge_threshold = 6  # Words with uncertainty >= this level are flagged

    def detect(self, text: str, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detects logical fallacies and unsupported claims in text.

        Args:
            text: Text to analyze
            analysis_result: Results of linguistic analysis

        Returns:
            Dictionary with detection results
        """
        # Initialize results
        results = {
            "logical_fallacies": [],
            "unsupported_claims": [],
            "consistency_issues": [],
            "references": [],
            "emotional_language": [],
            "hedges": [],
        }

        # Skip detection if language is not supported
        if not self.resources:
            return results

        # Find logical fallacies
        results["logical_fallacies"] = self._detect_logical_fallacies(text)

        # Find emotional language
        results["emotional_language"] = self._detect_emotional_language(text)

        # Find hedges (uncertainty markers)
        results["hedges"] = self._detect_hedges(text)

        # Find unsupported claims
        results["unsupported_claims"] = self._detect_unsupported_claims(text)

        return results

    def _detect_logical_fallacies(self, text: str) -> List[Dict[str, Any]]:
        """
        Detect logical fallacies in text.

        Args:
            text: Text to analyze

        Returns:
            List of logical fallacies
        """
        fallacies = []

        # Skip if no patterns loaded
        if "logical_patterns" not in self.resources:
            return fallacies

        patterns = self.resources["logical_patterns"]

        # For each fallacy type
        for fallacy_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                # Replace placeholders with regex
                regex_pattern = self._convert_pattern_to_regex(pattern)

                # Find all matches
                for match in re.finditer(regex_pattern, text, re.IGNORECASE):
                    fallacies.append(
                        {
                            "type": fallacy_type,
                            "pattern": pattern,
                            "match": match.group(0),
                            "position": match.span(),
                            "severity": self._get_fallacy_severity(fallacy_type),
                        }
                    )

        return fallacies

    def _convert_pattern_to_regex(self, pattern: str) -> str:
        """
        Convert a pattern with placeholders to regex.

        Args:
            pattern: Pattern with placeholders like {person}

        Returns:
            Regex pattern
        """
        # Replace placeholders with wildcard regex
        regex = re.escape(pattern)
        regex = re.sub(r"\\{[^}]+\\}", r"([\\w\\s]+?)", regex)
        return regex

    def _get_fallacy_severity(self, fallacy_type: str) -> str:
        """
        Get the severity level for a fallacy type.

        Args:
            fallacy_type: Type of fallacy

        Returns:
            Severity level (low, medium, high)
        """
        severity_map = {
            "ad_hominem": "high",
            "false_dichotomy": "medium",
            "appeal_to_authority": "medium",
            "slippery_slope": "medium",
            "hasty_generalization": "high",
            "appeal_to_emotion": "medium",
            "straw_man": "high",
        }

        return severity_map.get(fallacy_type, "medium")

    def _detect_emotional_language(self, text: str) -> List[Dict[str, Any]]:
        """
        Detect emotional language in text.

        Args:
            text: Text to analyze

        Returns:
            List of emotional language instances
        """
        emotional_instances = []

        # Skip if no emotional words loaded
        if "emotional_words" not in self.resources:
            return emotional_instances

        emotional_words = self.resources["emotional_words"]
        intensifiers = self.resources.get("intensifiers", {})

        # Tokenize text into words (simple split by space)
        words = text.lower().split()

        # Find emotional words
        for i, word in enumerate(words):
            # Clean the word (remove punctuation)
            clean_word = re.sub(r"[^\w\s]", "", word)

            if clean_word in emotional_words:
                intensity, polarity = emotional_words[clean_word]

                # Check if preceded by an intensifier
                enhanced_intensity = intensity
                intensifier = None

                if i > 0:
                    prev_word = re.sub(r"[^\w\s]", "", words[i - 1])
                    if prev_word in intensifiers:
                        intensifier = prev_word
                        intensifier_value = intensifiers[prev_word]
                        enhanced_intensity = min(10, intensity + intensifier_value // 2)

                # Only include high-intensity emotional words
                if enhanced_intensity >= self.emotion_threshold:
                    emotional_instances.append(
                        {
                            "word": clean_word,
                            "position": i,
                            "intensity": enhanced_intensity,
                            "original_intensity": intensity,
                            "polarity": "positive" if polarity > 0 else "negative",
                            "intensifier": intensifier,
                        }
                    )

        return emotional_instances

    def _detect_hedges(self, text: str) -> List[Dict[str, Any]]:
        """
        Detect hedges (uncertainty markers) in text.

        Args:
            text: Text to analyze

        Returns:
            List of hedges
        """
        hedge_instances = []

        # Skip if no hedges loaded
        if "hedges" not in self.resources:
            return hedge_instances

        hedges = self.resources["hedges"]

        # For each hedge
        for hedge, uncertainty in hedges.items():
            # Only include higher uncertainty hedges
            if uncertainty >= self.hedge_threshold:
                # Find all occurrences
                for match in re.finditer(
                    r"\b" + re.escape(hedge) + r"\b", text.lower()
                ):
                    hedge_instances.append(
                        {
                            "hedge": hedge,
                            "position": match.span(),
                            "uncertainty": uncertainty,
                        }
                    )

        return hedge_instances

    def _detect_unsupported_claims(self, text: str) -> List[Dict[str, Any]]:
        """
        Detect potentially unsupported claims.

        Args:
            text: Text to analyze

        Returns:
            List of potentially unsupported claims
        """
        # Simple implementation - look for sentences with absolute statements
        # but no references or evidence

        unsupported_claims = []

        # Split text into sentences (very basic)
        sentences = re.split(r"[.!?]", text)

        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue

            # Check if sentence contains absolute statements
            absolute_indicators = [
                "всі",
                "завжди",
                "ніколи",
                "кожен",
                "жоден",
                "повністю",
                "абсолютно",
                "безумовно",
            ]

            # Check if sentence has evidence markers
            evidence_indicators = [
                "оскільки",
                "тому що",
                "через те що",
                "за даними",
                "дослідження показують",
                "згідно з",
                "як свідчить",
            ]

            has_absolute = any(
                indicator in sentence.lower() for indicator in absolute_indicators
            )
            has_evidence = any(
                indicator in sentence.lower() for indicator in evidence_indicators
            )

            if has_absolute and not has_evidence:
                unsupported_claims.append(
                    {
                        "sentence": sentence,
                        "position": i,
                        "confidence": 0.7,  # Confidence that this is truly unsupported
                        "absolute_indicators": [
                            ind
                            for ind in absolute_indicators
                            if ind in sentence.lower()
                        ],
                    }
                )

        return unsupported_claims
