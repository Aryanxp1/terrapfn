"""Post-hike observation check-in service.

Stores ground-truth post-hike reflections locally in structured JSON format
for future model evaluation and personal calibration experiments.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

CHECKINS_FILE_PATH = Path("data/processed/hike_checkins.json")


def load_checkin_history(file_path: Path = CHECKINS_FILE_PATH) -> List[Dict[str, Any]]:
    """Load local post-hike check-in records."""
    if not file_path.exists():
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception:
        pass
    return []


def record_checkin(
    trail_name: str,
    felt_difficulty: str,
    predicted_difficulty: str,
    trail_id: Optional[int | str] = None,
    actual_duration_min: Optional[int] = None,
    notes: Optional[str] = None,
    file_path: Path = CHECKINS_FILE_PATH,
) -> Dict[str, Any]:
    """Store a post-hike reflection record locally."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    history = load_checkin_history(file_path)

    checkin_record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "trail_id": trail_id,
        "trail_name": trail_name.strip() or "Unnamed Trail",
        "predicted_difficulty": predicted_difficulty,
        "felt_difficulty": felt_difficulty,
        "actual_duration_min": actual_duration_min,
        "notes": notes.strip() if notes else None,
        "agreement": int(felt_difficulty.lower() == predicted_difficulty.lower()),
    }

    history.append(checkin_record)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

    return checkin_record
