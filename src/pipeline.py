from __future__ import annotations

import argparse
from pathlib import Path

from .config import ProjectConfig
from .generate_data import generate_all
from .validators import validate_referential_integrity
from .exporters import export_all


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Aurora Fashion Club synthetic data pipeline")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--n-customers", type=int, default=5000)
    parser.add_argument("--n-products", type=int, default=1000)
    parser.add_argument("--n-campaigns", type=int, default=180)
    parser.add_argument("--start-date", type=str, default="2023-01-01")
    parser.add_argument("--end-date", type=str, default="2025-12-31")
    parser.add_argument("--output-dir", type=str, default="data")
    return parser


def run_pipeline(cfg: ProjectConfig):
    bundle = generate_all(cfg)
    validation = validate_referential_integrity(bundle)
    export_all(bundle, cfg.resolved_output_dir(Path(__file__).resolve().parents[1]))
    return bundle, validation


def main():
    parser = build_arg_parser()
    args = parser.parse_args()
    cfg = ProjectConfig(
        seed=args.seed,
        n_customers=args.n_customers,
        n_products=args.n_products,
        n_campaigns=args.n_campaigns,
        start_date=args.start_date,
        end_date=args.end_date,
        output_dir=Path(args.output_dir),
    )
    bundle, validation = run_pipeline(cfg)
    print(f"Export completed to {cfg.resolved_output_dir(Path(__file__).resolve().parents[1])}")
    print(f"Validation passed: {validation.passed}")
    if validation.errors:
        print("Errors:")
        for err in validation.errors:
            print("-", err)
    if validation.warnings:
        print("Warnings:")
        for warn in validation.warnings:
            print("-", warn)
    print("Rows generated:")
    for name in ["customers","products","orders","order_items","campaigns","interactions","support_tickets","digital_events"]:
        print(f"- {name}: {len(getattr(bundle, name)):,}")


if __name__ == "__main__":
    main()
