from __future__ import annotations

from aurora_fashion_club.config.settings import load_config


def main() -> None:
    config = load_config()
    print(f"[generation] project={config.project.name}")
    print("[generation] placeholder: generation pipeline will be implemented in the next step.")


if __name__ == "__main__":
    main()
