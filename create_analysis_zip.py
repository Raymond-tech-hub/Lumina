from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


DEFAULT_OUTPUT = "lumina_analysis_subset.zip"

INCLUDE_PATHS = [
    "main.py",
    "frontend/scripts/loading_screen.py",
    "frontend/scripts/loading_animation.py",
    "frontend/scripts/home_screen.py",
    "frontend/scripts/login_screen.py",
    "frontend/scripts/signup_screen.py",
    "frontend/scripts/lesson_screen.py",
    "frontend/scripts/lesson_progress_screen.py",
    "frontend/scripts/quiz_screen.py",
    "frontend/scripts/profile_screen.py",
    "frontend/scripts/tasks_screen.py",
    "frontend/scripts/timetable_screen.py",
    "frontend/scripts/chatbot_screen.py",
    "frontend/scripts/notification_screen.py",
    "frontend/scripts/quiz_engine.py",
    "frontend/scripts/quiz.py",
    "frontend/scripts/tasks.py",
    "backend/student_data.py",
    "backend/user_builder.py",
    "backend/authenticaion.py",
    "backend/timetable.py",
    "backend/JSON.py",
    "backend/decison_tree.py",
    "backend/tree.py",
    "backend/RAG/student_decision_engine.py",
    "backend/RAG/search.py",
    "backend/ChatBot/chatbot.py",
    "backend/ChatBot/input_processor.py",
    "backend/ChatBot/system_check.py",
    "backend/ChatBot/token_simulation.py",
    "backend/ChatBot/voice.py",
    "backend/ChatBot/voicechat_screen.py",
    "data/user/1/meta_data.json",
    "data/user/1/progress/progress.json",
    "data/user/1/subjects/course_biology.json",
    "ConfigFile.json",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the curated Lumina analysis ZIP."
    )
    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Output ZIP path. Defaults to {DEFAULT_OUTPUT}.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the output ZIP if it already exists.",
    )
    return parser.parse_args()


def validate_paths(root: Path) -> list[Path]:
    missing: list[str] = []
    resolved: list[Path] = []

    for relative_path in INCLUDE_PATHS:
        path = root / relative_path
        if not path.exists():
            missing.append(relative_path)
            continue
        resolved.append(path)

    if missing:
        missing_text = "\n".join(f"- {path}" for path in missing)
        raise FileNotFoundError(f"Missing required files:\n{missing_text}")

    return resolved


def create_zip(root: Path, output_path: Path, files: list[Path]) -> None:
    with ZipFile(output_path, "w", compression=ZIP_DEFLATED) as archive:
        for file_path in files:
            archive.write(file_path, arcname=file_path.relative_to(root))


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parent
    output_path = (root / args.output).resolve()

    if output_path.exists() and not args.overwrite:
        raise FileExistsError(
            f"{output_path} already exists. Re-run with --overwrite to replace it."
        )

    files = validate_paths(root)
    create_zip(root, output_path, files)

    print(f"Created {output_path}")
    print(f"Included {len(files)} files")
    print("Note: KV files are intentionally excluded from this archive.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
