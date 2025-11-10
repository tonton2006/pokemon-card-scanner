"""Card data parsing and validation logic."""
import re
from typing import Optional, Tuple


def parse_card_name(text: str) -> Optional[str]:
    """
    Extract Pokemon card name from OCR text.

    Args:
        text: Full OCR text

    Returns:
        Card name if found, None otherwise
    """
    lines = text.split("\n")

    # Pokemon card names are usually in the first few lines
    # and are typically capitalized words
    for line in lines[:10]:  # Check first 10 lines
        line = line.strip()

        # Skip short lines
        if len(line) < 3:
            continue

        # Skip lines that are obviously not card names
        if any(skip in line.lower() for skip in ["hp", "©", "pokemon", "length"]):
            continue

        # Check if line looks like a card name (mostly alphabetic)
        if re.match(r"^[A-Z][a-z]+(\s+[A-Z][a-z]+)*$", line):
            return line

    return None


def extract_set_info(text: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract set name and card number from OCR text.

    Args:
        text: Full OCR text

    Returns:
        Tuple of (set_name, card_number)
    """
    set_name = None
    card_number = None

    lines = text.split("\n")

    # Look for card number pattern (e.g., "4/102", "25/100")
    number_pattern = r"(\d+)/(\d+)"
    for line in lines:
        match = re.search(number_pattern, line)
        if match:
            card_number = match.group(0)
            break

    # Common Pokemon TCG set names to look for
    common_sets = [
        "Base Set", "Jungle", "Fossil", "Team Rocket",
        "Gym Heroes", "Gym Challenge", "Neo Genesis",
        "Sword & Shield", "Vivid Voltage", "Evolving Skies",
        "Brilliant Stars", "Astral Radiance", "Lost Origin",
        "Silver Tempest", "Crown Zenith", "Paldea Evolved",
        "Obsidian Flames", "151", "Paradox Rift"
    ]

    text_lower = text.lower()
    for set_name_candidate in common_sets:
        if set_name_candidate.lower() in text_lower:
            set_name = set_name_candidate
            break

    return set_name, card_number


def extract_rarity(text: str) -> Optional[str]:
    """
    Extract card rarity from OCR text.

    Args:
        text: Full OCR text

    Returns:
        Rarity string if found, None otherwise
    """
    rarities = [
        "Common", "Uncommon", "Rare", "Holo Rare",
        "Ultra Rare", "Secret Rare", "Rainbow Rare",
        "Full Art", "V", "VMAX", "VSTAR", "ex", "GX"
    ]

    text_lower = text.lower()
    for rarity in rarities:
        if rarity.lower() in text_lower:
            return rarity

    return None


def parse_full_card_info(text: str) -> dict:
    """
    Parse all card information from OCR text.

    Args:
        text: Full OCR text

    Returns:
        Dict with card info (name, set, number, rarity)
    """
    name = parse_card_name(text)
    set_name, card_number = extract_set_info(text)
    rarity = extract_rarity(text)

    return {
        "name": name,
        "set": set_name,
        "number": card_number,
        "rarity": rarity
    }
