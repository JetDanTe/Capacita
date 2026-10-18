from pathlib import Path
import json


DB_PATH = Path(__file__).resolve().parents[2] / "data" / "mock_db.json"


def load_db() -> list[dict]:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not DB_PATH.exists():
        save_db([])
        return []

    try:
        with DB_PATH.open("r", encoding="utf-8") as db_file:
            data = json.load(db_file)
    except (json.JSONDecodeError, OSError):
        return []

    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    return []


def save_db(data: list[dict]) -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DB_PATH.open("w", encoding="utf-8") as db_file:
        json.dump(data, db_file, indent=2, ensure_ascii=False)


def get_next_id(records: list[dict]) -> int:
    if not records:
        return 1
    return max(int(record.get("id", 0)) for record in records) + 1
