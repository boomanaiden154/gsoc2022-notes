import subprocess
import sys
import re
import json

def get_gtest_executable_output(path_to_executable):
    command_vector = [path_to_executable, "--gtest_list_tests"]
    process = subprocess.Popen(command_vector, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    return out.decode("UTF-8")

def parse_gtest_all_tests(gtest_output):
    test_list = []
    current_test_prefix = ""
    gtest_output_split = gtest_output.split("\n")
    current_index = 0
    while current_index < len(gtest_output_split):
        current_string = gtest_output_split[current_index]
        if len(current_string) == 0:
            current_index += 1
            continue
        # get the test name
        test_match = re.findall("^\s*\S*", current_string)[0].replace(" ","")
        if test_match[len(test_match) - 1] == ".":
            # We've found a new prefix
            current_test_prefix = test_match
            current_index += 1
            continue
        test_list.append(current_test_prefix + test_match)
        current_index += 1
    return test_list

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Correct usage is parse_gtests.py [gtest executable]")
        sys.exit(1)

    test_list_raw_output = get_gtest_executable_output(sys.argv[1])
    test_list_parsed = parse_gtest_all_tests(test_list_raw_output)
    test_dict = {
        "test": test_list_parsed
    }
    print(json.dumps(test_dict, indent=4))