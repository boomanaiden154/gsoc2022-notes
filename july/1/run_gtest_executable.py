import json
import sys
import subprocess
import re

perf_counters = [
    "mem_uops_retired.all_loads",
    "mem_uops_retired.all_stores"
]

def load_tests_file(test_file_name):
    with open(test_file_name) as test_file:
        test_file_dict = json.load(test_file)
        return test_file_dict["tests"]

def run_test(test_executable, test_name):
    command_vector = ["perf", "stat"]
    for perf_counter in perf_counters:
        command_vector.extend(["-e", perf_counter])
    command_vector.extend([test_executable, "--gtest_filter={filter}".format(filter=test_name)])
    process = subprocess.Popen(command_vector, stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
    out, err = process.communicate()
    return err.decode("UTF-8")

def parse_perf_stat_output(perf_stat_output):
    counters_dict = {}
    for line in perf_stat_output.split("\n"):
        for perf_counter in perf_counters:
            if perf_counter in line:
                count_string = re.findall("^\s*\d*", line)[0].replace(" ","")
                count = int(count_string)
                counters_dict[perf_counter] = count
    return counters_dict

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage is run_gtest_executable.py [gtest executable] [tests json file]", file=sys.stderr)
        sys.exit(1)
    
    tests_list = load_tests_file(sys.argv[2])
    # run benchmarks
    test_data_output = {}
    for test in tests_list:
        test_output = run_test(sys.argv[1], test)
        test_data_output[test] = parse_perf_stat_output(test_output)
        print("Finished running:{test}".format(test=test), file=sys.stderr)
    # output data
    print(json.dumps(test_data_output, indent=4))