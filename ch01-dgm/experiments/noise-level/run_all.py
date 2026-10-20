"""全実験を順番に実行する。"""
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPERIMENTS = [
    "vary-t-linear",
    "vary-t-vp",
    "unrestricted-t",
    "vary-alpha",
]


def main() -> None:
    for name in EXPERIMENTS:
        script = ROOT / name / "run.py"
        print(f"===== {name} =====")
        runpy.run_path(str(script), run_name="__main__")


if __name__ == "__main__":
    main()
