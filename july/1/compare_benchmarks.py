import json
import sys
import statistics

def load_benchmarks(benchmark_file_path):
    with open(benchmark_file_path) as benchmark_file:
        benchmark_json = json.load(benchmark_file)
        return benchmark_json

def per_test_comparison(benchmark_set_1, benchmark_set_2):
    benchmark_comparisons = {}
    for benchmark in benchmark_set_1:
        if benchmark in benchmark_set_2:
            for perf_counter in benchmark_set_1[benchmark]:
                if benchmark not in benchmark_comparisons:
                    benchmark_comparisons[benchmark] = {}
                benchmark_comparisons[benchmark][perf_counter] = benchmark_set_2[benchmark][perf_counter] / benchmark_set_1[benchmark][perf_counter]

        else:
            print("benchmark sets are incompatible")
    return benchmark_comparisons

def get_average_speedup(benchmark_comparisons):
    overall_comparisons = {}
    for comparison in benchmark_comparisons:
        for perf_counter in benchmark_comparisons[comparison]:
            if perf_counter in overall_comparisons:
                overall_comparisons[perf_counter].append(benchmark_comparisons[comparison][perf_counter])
            else:
                overall_comparisons[perf_counter] = [benchmark_comparisons[comparison][perf_counter]]
    comparison_means = {}
    for perf_counter in overall_comparisons:
        comparison_means[perf_counter] = statistics.geometric_mean(overall_comparisons[perf_counter])
    return comparison_means

def combine_benchmarks(benchmark_set_array):
    combined_benchmarks = {}
    for benchmark_set in benchmark_set_array:
        for benchmark in benchmark_set:
            combined_benchmarks[benchmark] = benchmark_set[benchmark]
    return combined_benchmarks

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage is [compare_benchmarks.py] [benchmark file 1] [benchmark file 2]")
        sys.exit(0)

    benchmark_set_1 = load_benchmarks(sys.argv[1])
    benchmark_set_2 = load_benchmarks(sys.argv[2])

    comparisons = per_test_comparison(benchmark_set_1, benchmark_set_2)

    overall_comparisons = get_average_speedup(comparisons)

    final_output = {
        "per_test_comparisons": comparisons,
        "overall_comparison": overall_comparisons
    }

    print(json.dumps(final_output, indent=4))

    for perf_counter in overall_comparisons:
        print("Overall difference for {perfcounter}: {average}".format(perfcounter=perf_counter, average=overall_comparisons[perf_counter]), file=sys.stderr)