"""Export public challenge metadata for static S3/CloudFront hosting."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = ROOT / "backend"
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent / "public"
LANGUAGES = ("en", "es")

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from challenges import CHALLENGES  # noqa: E402


def localized_title(challenge: Any, lang: str) -> str:
    if lang == "es" and challenge.title_es:
        return challenge.title_es
    return challenge.title


def localized_description(challenge: Any, lang: str) -> str:
    if lang == "es" and challenge.description_es:
        return challenge.description_es
    return challenge.description


def localized_starter_code(challenge: Any, lang: str) -> str:
    if lang == "es" and challenge.starter_code_es:
        return challenge.starter_code_es
    return challenge.starter_code or ""


def challenge_list_payload(lang: str) -> dict[str, list[dict[str, str]]]:
    return {
        "challenges": [
            {
                "id": challenge.id,
                "title": localized_title(challenge, lang),
            }
            for challenge in CHALLENGES.values()
        ]
    }


def challenge_detail_payload(challenge_id: str, lang: str) -> dict[str, Any]:
    challenge = CHALLENGES[challenge_id]
    return {
        "id": challenge.id,
        "title": localized_title(challenge, lang),
        "description": localized_description(challenge, lang),
        "starter_code": localized_starter_code(challenge, lang),
        "test_count": len(challenge.tests),
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    if path.parent.exists() and not path.parent.is_dir():
        path.parent.unlink()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def export_api_compatible_files(output_dir: Path) -> None:
    api_dir = output_dir / "api" / "v2" / "playground" / "challenges"
    write_json(api_dir / "index.json", challenge_list_payload("en"))
    for challenge_id in CHALLENGES:
        write_json(
            api_dir / f"{challenge_id}.json",
            challenge_detail_payload(challenge_id, "en"),
        )

    for lang in LANGUAGES:
        write_json(api_dir / f"index.{lang}.json", challenge_list_payload(lang))
        for challenge_id in CHALLENGES:
            write_json(
                api_dir / f"{challenge_id}.{lang}.json",
                challenge_detail_payload(challenge_id, lang),
            )


def export_localized_files(output_dir: Path) -> None:
    challenges_dir = output_dir / "challenges"
    for lang in LANGUAGES:
        write_json(challenges_dir / f"index.{lang}.json", challenge_list_payload(lang))
        for challenge_id in CHALLENGES:
            write_json(
                challenges_dir / f"{challenge_id}.{lang}.json",
                challenge_detail_payload(challenge_id, lang),
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export public challenge metadata as static JSON."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory. Defaults to {DEFAULT_OUTPUT_DIR}.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = args.output_dir.resolve()
    export_api_compatible_files(output_dir)
    export_localized_files(output_dir)
    print(f"Exported {len(CHALLENGES)} challenges to {output_dir}")


if __name__ == "__main__":
    main()
