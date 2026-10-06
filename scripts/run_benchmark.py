"""CLI entrypoint to execute the complete leak-free TerraPFN benchmark."""

from terrapfn.evaluation.nested_cv import run_benchmark

if __name__ == "__main__":
    print("=" * 70)
    print("Starting TerraPFN Leakage-Free 5-Fold Stratified Benchmark")
    print("=" * 70)
    run_benchmark(n_splits=5, random_state=42, output_dir="data/processed/benchmark_results")
