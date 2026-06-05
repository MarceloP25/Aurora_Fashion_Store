"""Master pipeline.

Stage 1 currently executes the synthetic generation layer only.
"""

from __future__ import annotations

from aurora_fashion_club.pipelines.run_generation import main as run_generation


def main() -> None:
    """Run the active project stage."""
    run_generation()


if __name__ == "__main__":
    main()
