"""Post-hike observation check-in service.

Stores ground-truth post-hike reflections locally in structured JSON format
for future model evaluation and personal calibration experiments.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[3]
CHECKINS_FILE_PATH = REPO_ROOT / "data/processed/hike_checkins.json"


def load_checkin_history(file_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Load local post-hike check-in records."""
    target_path = file_path if file_path is not None else CHECKINS_FILE_PATH
    if not target_path.exists():
        # Also check fallback path if primary does not exist
        fallback_path = Path("/tmp/hike_checkins.json")
        if fallback_path.exists():
            target_path = fallback_path
        else:
            return []
    try:
        with open(target_path, "r", encoding="utf-8") as f:
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
    file_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """Store a post-hike reflection record locally."""
    target_path = file_path if file_path is not None else CHECKINS_FILE_PATH
    try:
        target_path.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        target_path = Path("/tmp/hike_checkins.json")
        target_path.parent.mkdir(parents=True, exist_ok=True)

    history = load_checkin_history(target_path)

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

    try:
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
    except Exception:
        # Fallback to /tmp if primary directory is read-only
        fallback_path = Path("/tmp/hike_checkins.json")
        try:
            with open(fallback_path, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2)
        except Exception:
            pass

    return checkin_record
