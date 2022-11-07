import json
import statistics
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("usage is python3 <this file> <rawish data> <processed data>")
        sys.exit(1)
    input_filepath = sys.argv[1]
    output_filepath = sys.argv[2]
    with open(input_filepath) as input_file:
        input_data = json.load(input_file)
        # aggregate individual test runs per label
        labels = {}
        for test_instance in input_data:
            if test_instance['label'] in labels:
                labels[test_instance['label']].append((test_instance['name'], test_instance['value']))
            else:
                labels[test_instance['label']] = [(test_instance['name'], test_instance['value'])]
        # average test runs with the same name under the same label
        labels_aggregated = {}
        for label_name in labels:
            label = labels[label_name]
            benchmark_set = {}
            for benchmark in label:
                if benchmark[0] in benchmark_set:
                    benchmark_set[benchmark[0]].append(benchmark[1])
                else:
                    benchmark_set[benchmark[0]] = [benchmark[1]]
            benchmark_data = {}
            for benchmark in benchmark_set:
                benchmark_data[benchmark] = {
                    'values': benchmark_set[benchmark],
                    'mean': statistics.mean(benchmark_set[benchmark]),
                    'stdev': statistics.stdev(benchmark_set[benchmark]) 
                }
            labels_aggregated[label_name] = benchmark_data
        with open(output_filepath, 'w') as output_file:
            output_file.write(json.dumps(labels_aggregated, indent=4))
