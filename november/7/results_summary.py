import json
import statistics
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage is python3 <this file> <input json file>')

    input_filepath = sys.argv[1]
    with open(input_filepath) as input_file:
        input_data = json.load(input_file)
        comparisons = []
        for benchmark in input_data:
            comparisons.append(input_data[benchmark]['comparison'])
        print(statistics.geometric_mean(comparisons))
