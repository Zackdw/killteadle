"""
Build data JSON for the Kill Team Wordle game.

Reads library_index.json and each operative's card_1.txt to extract:
  - team (source_pdf)
  - operative_name
  - apl (first number after operative name line)
  - faction (IMPERIUM, CHAOS, TYRANID, T'AU EMPIRE, AELDARI, LEAGUES OF VOTANN, ORK, NECRON)
  - base_size (second-to-last line of card_1.txt)
  - weapon_rules (unique weapon rules from all weapons)
"""

import json
import re
from pathlib import Path

LIBRARY_DIR = Path(__file__).parent / "library"
OUTPUT_PATH = Path(__file__).parent / "data.json"

FACTIONS = [
    "LEAGUES OF VOTANN",  # check multi-word first
    "T\u2019AU EMPIRE",   # Unicode right single quote in PDF text
    "T'AU EMPIRE",        # ASCII apostrophe fallback
    "GREAT DEVOURER",
    "IMPERIUM",
    "CHAOS",
    "TYRANID",
    "AELDARI",
    "ORK",
    "NECRON",
]

# Normalize faction display names
FACTION_DISPLAY = {
    "T\u2019AU EMPIRE": "T'AU EMPIRE",
}

# Map alternate faction names to canonical ones
FACTION_MAP = {
    "GREAT DEVOURER": "TYRANID",
}

VALID_BASES = {"25", "28", "32", "40", "50", "60x35"}

# Known weapon rules from Kill Team Light Rules PDF
WEAPON_RULES = [
    "Accurate", "Balanced", "Brutal", "Ceaseless", "Devastating",
    "Heavy", "Hot", "Lethal", "Limited", "Piercing", "Punishing",
    "Range", "Relentless", "Rending", "Saturate", "Seek", "Severe",
    "Shock", "Silent", "Stun", "Torrent", "Blast",
]

# Regex to match weapon rule names (ignoring trailing numbers/dice notation)
_WR_PATTERN = re.compile(
    r'\b(' + '|'.join(WEAPON_RULES) + r')\b',
    re.IGNORECASE,
)


def parse_card_text(text_path):
    """Parse card_1.txt and extract apl, faction, base_size."""
    lines = text_path.read_text(encoding="utf-8").strip().split("\n")

    if len(lines) < 5:
        return None

    # Last line is keywords (comma-separated)
    keywords_line = lines[-1].strip()

    # Extract faction from keywords
    faction = None
    keywords_upper = keywords_line.upper()
    for f in FACTIONS:
        if f in keywords_upper:
            faction = FACTION_MAP.get(f, f)
            faction = FACTION_DISPLAY.get(faction, faction)
            break

    # Extract base size: search backwards from keywords line for a valid base
    base_size = None
    for i in range(len(lines) - 2, max(len(lines) - 6, -1), -1):
        base_clean = lines[i].strip().replace("mm", "").strip()
        if base_clean in VALID_BASES:
            base_size = base_clean
            break

    # Extract APL: it's the first standalone number after the header block
    # Pattern: line "APL", then "WOUNDS", "SAVE", "MOVE", then operative name,
    # then the APL value (a single digit 1-3)
    apl = None
    found_apl_header = False
    found_name = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "APL":
            found_apl_header = True
            continue
        if found_apl_header and not found_name:
            # Skip WOUNDS, SAVE, MOVE, then operative name
            if stripped in ("WOUNDS", "SAVE", "MOVE"):
                continue
            if stripped == "NAME":
                # We went too far
                break
            # This could be the operative name or APL value
            if stripped in ("1", "2", "3", "4"):
                # Could be APL if we already passed the name
                if found_name:
                    apl = int(stripped)
                    break
                else:
                    # Might be a very short name? No - 1/2/3 after headers = 
                    # we haven't seen the name yet. Check next line.
                    # Actually the pattern is: APL/WOUNDS/SAVE/MOVE headers,
                    # then operative name, then APL value, then move, save, wounds
                    # But wait - looking at the data, the order after name is:
                    # APL_val, MOVE_val, SAVE_val, WOUNDS_val
                    # Actually no. Let me re-examine the actual text.
                    pass
            if not found_name and len(stripped) > 1 and not stripped.isdigit():
                found_name = True
                continue
            if found_name and stripped.isdigit() and int(stripped) in (1, 2, 3, 4):
                apl = int(stripped)
                break

    # Alternative simpler approach: find operative name line, next line is APL
    if apl is None:
        for i, line in enumerate(lines):
            if line.strip() == "APL":
                # Find the next line that has a multi-character non-number text (operative name)
                # Then the line after that is APL value
                for j in range(i + 1, min(i + 8, len(lines))):
                    stripped = lines[j].strip()
                    if stripped in ("WOUNDS", "SAVE", "MOVE", "NAME", "ATK", "HIT DMG", "WR"):
                        continue
                    if len(stripped) > 2 and not stripped.replace('"', '').replace('+', '').isdigit():
                        # This is the operative name, next numeric line is APL
                        for k in range(j + 1, min(j + 4, len(lines))):
                            val = lines[k].strip()
                            if val in ("1", "2", "3", "4"):
                                apl = int(val)
                                break
                        break
                break

    # Extract weapon rules from WR column entries
    # After "WR" header, weapons follow the pattern:
    # weapon_name, ATK, HIT, DMG (\d+/\d+), WR_text (or "-")
    # Only extract from WR lines (immediately after DMG lines)
    # Stop when ability text starts (contains ': ') or rules continue
    weapon_rules = set()
    in_weapons = False
    prev_is_dmg = False
    reading_wr = False
    for line in lines:
        stripped = line.strip()
        if stripped == "WR":
            in_weapons = True
            continue
        if in_weapons:
            # Stop at ability text or rules continuation
            if ': ' in stripped or stripped == 'RULES CONTINUE ON OTHER SIDE':
                break
            if reading_wr:
                # Check if this is a continuation of the previous WR line
                # (not a DMG pattern and not a weapon name with ATK)
                if not re.match(r'^\d+/\d+$', stripped) and not re.match(r'^\d+$', stripped) and stripped != '-':
                    found = _WR_PATTERN.findall(stripped)
                    if found:
                        for rule in found:
                            weapon_rules.add(rule.capitalize())
                        continue
                reading_wr = False
            if prev_is_dmg:
                # This line is the WR entry for a weapon
                found = _WR_PATTERN.findall(stripped)
                for rule in found:
                    weapon_rules.add(rule.capitalize())
                # If line ends with comma, next line may continue WR
                reading_wr = stripped.endswith(',')
                prev_is_dmg = False
            else:
                prev_is_dmg = bool(re.match(r'^\d+/\d+$', stripped))

    return {
        "apl": apl,
        "faction": faction,
        "base_size": base_size,
        "weapon_rules": sorted(weapon_rules),
    }


def main():
    index_path = LIBRARY_DIR / "library_index.json"
    with open(index_path, encoding="utf-8") as f:
        library = json.load(f)

    operatives = []
    errors = []

    for entry in library:
        name = entry["operative_name"]
        team = entry["source_pdf"]
        text_files = entry.get("text_files", [])

        if not text_files:
            errors.append(f"No text files for {name} ({team})")
            continue

        card1_path = LIBRARY_DIR / text_files[0]
        if not card1_path.exists():
            errors.append(f"Missing {card1_path}")
            continue

        parsed = parse_card_text(card1_path)
        if parsed is None:
            errors.append(f"Failed to parse {name} ({team})")
            continue

        if parsed["apl"] is None:
            errors.append(f"No APL found for {name} ({team})")
        if parsed["faction"] is None:
            errors.append(f"No faction found for {name} ({team})")
        if parsed["base_size"] is None:
            errors.append(f"No base size found for {name} ({team})")

        operatives.append({
            "name": name,
            "team": team,
            "apl": parsed["apl"],
            "faction": parsed["faction"],
            "base_size": parsed["base_size"],
            "weapon_rules": parsed["weapon_rules"],
        })

    # Print stats
    total = len(operatives)
    missing_apl = sum(1 for o in operatives if o["apl"] is None)
    missing_faction = sum(1 for o in operatives if o["faction"] is None)
    missing_base = sum(1 for o in operatives if o["base_size"] is None)

    print(f"Total operatives: {total}")
    print(f"Missing APL: {missing_apl}")
    print(f"Missing faction: {missing_faction}")
    print(f"Missing base size: {missing_base}")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(f"  {e}")

    # Show some samples
    print("\nSample entries:")
    for o in operatives[:5]:
        print(f"  {o['name']} | {o['team']} | APL:{o['apl']} | {o['faction']} | base:{o['base_size']}")

    # Save output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(operatives, f, indent=2, ensure_ascii=False)

    print(f"\nSaved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
