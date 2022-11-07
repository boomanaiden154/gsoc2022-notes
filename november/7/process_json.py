import json
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('usage is python3 <this file> <input json> <output json>')
        sys.exit(1)
    input_filepath = sys.argv[1]
    with open(input_filepath) as input_file:
        input_data = json.load(input_file)
        # gather GenericSets
        generic_sets = {}
        for data_section in input_data:
            if 'type' in data_section:
                if data_section['type'] == 'GenericSet':
                    generic_sets[data_section['guid']] = data_section['values'][0]
        benchmark_results = []
        # gather benchmark results
        for data_section in input_data:
            if 'name' in data_section:
                new_benchmark = {}
                new_benchmark['name'] = data_section['name']
                new_benchmark['label'] = generic_sets[data_section['diagnostics']['labels']]
                new_benchmark['value'] = data_section['sampleValues'][0]
                benchmark_results.append(new_benchmark)
        output_filepath = sys.argv[2]
        with open(output_filepath, 'w') as output_file:
            output_file.write(json.dumps(benchmark_results, indent=4))

