import json
import sys
import subprocess
import re

from joblib import Parallel, delayed

perf_counters = [
    "mem_uops_retired.all_loads",
    "mem_uops_retired.all_stores"
]

def load_tests_file(test_file_name):
    with open(test_file_name) as test_file:
        test_file_dict = json.load(test_file)
        return test_file_dict

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

def run_and_parse(test_description):
    test_executable, test_name = test_description
    test_output = run_test(test_executable, test_name)
    print("Finished running test {test}".format(test=test_name), file=sys.stderr)
    return (test_name, parse_perf_stat_output(test_output))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage is run_gtest_executable.py [tests json file] [num threads]", file=sys.stderr)
        sys.exit(1)
    
    tests_list = load_tests_file(sys.argv[1])
    test_executable = tests_list["executable"]

    num_threads = int(sys.argv[2])
    
    # run benchmarks
    test_descriptions = []
    for test in tests_list["tests"]:
        test_descriptions.append((test_executable, test))
    test_data_output = Parallel(n_jobs=num_threads)(delayed(run_and_parse)(test_description) for test_description in test_descriptions)

    formattedTestData = {}
    for testInstance in test_data_output:
        formattedTestData[testInstance[0]] = testInstance[1]
    # output data
    print(json.dumps(formattedTestData, indent=4))