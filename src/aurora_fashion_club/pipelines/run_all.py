from __future__ import annotations

from aurora_fashion_club.pipelines.run_generation import main as run_generation
from aurora_fashion_club.pipelines.run_validation import main as run_validation
from aurora_fashion_club.pipelines.run_etl import main as run_etl
from aurora_fashion_club.pipelines.run_features import main as run_features
from aurora_fashion_club.pipelines.run_analytics import main as run_analytics
from aurora_fashion_club.pipelines.run_modeling import main as run_modeling


def main() -> None:
    run_generation()
    run_validation()
    run_etl()
    run_features()
    run_analytics()
    run_modeling()


if __name__ == "__main__":
    main()
