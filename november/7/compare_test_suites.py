import json
import sys
import statistics

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("usage is: python3 <this file> <input json> <output json>")
    input_filepath = sys.argv[1]
    output_filepath = sys.argv[2]

    with open(input_filepath) as input_file:
        input_data = json.load(input_file)
        label_list = list(input_data.keys())
        benchmark_list = list(input_data[label_list[0]].keys())
        benchmark_comparisons = {}
        for benchmark in benchmark_list:
            current_comparison = {
                'firstValue': input_data[label_list[0]][benchmark]['mean'],
                'secondValue': input_data[label_list[1]][benchmark]['mean']
            }
            if current_comparison['firstValue'] == 0 or current_comparison['secondValue'] == 0:
                break
            current_comparison['comparison'] = current_comparison['firstValue'] / current_comparison['secondValue']
            benchmark_comparisons[benchmark] = current_comparison
        with open(output_filepath, 'w') as output_file:
            output_file.write(json.dumps(benchmark_comparisons, indent=4))
