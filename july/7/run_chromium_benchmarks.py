import subprocess
import os
import shutil
import json
import sys

from joblib import Parallel, delayed

sys.path.append("../5")
sys.path.append("../1")

import run_llvm_test_suite
import run_gtest_executable

from absl import app

depot_tools_path = "/depot_tools"

chromium_source_path = "/chromium/src"
chromium_build_path = "./out/Release"
chromium_absolute_build_path = os.path.join(chromium_source_path, chromium_build_path)

llvm_build_path = "/llvm-build"

num_threads = 30

tests_to_build = ["base_perftests", "browser_tests", "components_perftests"]

def build_chromium_tests(regalloc_advisor):
    if os.path.exists(chromium_absolute_build_path):
        shutil.rmtree(chromium_absolute_build_path)
    
    new_environment = os.environ.copy()
    new_environment["PATH"] += ":" + depot_tools_path
    new_environment["CC"] = os.path.join(llvm_build_path, "./bin/clang")
    new_environment["CXX"] = os.path.join(llvm_build_path, "./bin/clang++")
    new_environment["AR"] = os.path.join(llvm_build_path, "./bin/llvm-ar")
    new_environment["NM"] = os.path.join(llvm_build_path, "./bin/llvm-nm")
    new_environment["CPPFLAGS"] = "-mllvm -regalloc-enable-advisor={advisor}".format(advisor=regalloc_advisor)

    gn_args = [
        "is_official_build=true",
        "use_thin_lto=false",
        "is_cfi=false",
        "use_cfi_icall=false",
        "use_cfi_cast=false",
        "clang_use_chrome_plugins=false",
        "is_debug=false",
        "symbol_level=0",
        "custom_toolchain=\\\"//build/toolchain/linux/unbundle:default\\\"",
        "host_toolchain=\\\"//build/toolchain/linux/unbundle:default\\\""
    ]

    gn_args_string = '--args="'
    for arg in gn_args:
        gn_args_string += arg + " "
    gn_args_string += '"'

    gn_config_command = "gn gen " + chromium_build_path + " " + gn_args_string

    print(gn_config_command)

    gn_config_process = subprocess.Popen(gn_config_command, env=new_environment, cwd=chromium_source_path, shell=True)
    gn_config_process.wait()

    ninja_compile_command = ["autoninja", "-C", chromium_build_path]
    ninja_compile_command.extend(tests_to_build)
    ninja_compile_process = subprocess.Popen(ninja_compile_command, env=new_environment, cwd=chromium_source_path)
    ninja_compile_process.wait()

def run_tests(output_file_name):
    formatted_test_data = {}
    for test in tests_to_build:
        tests_list = run_gtest_executable.load_tests_file("../4/tests_to_run/" + test + ".json")
        test_descriptions = []
        executable = os.path.join(chromium_absolute_build_path, test)
        for test in tests_list["tests"]:
            test_descriptions.append((executable, test))
        test_data_output = Parallel(n_jobs=num_threads)(delayed(run_gtest_executable.run_and_parse)(test_description) for test_description in test_descriptions)

        for testInstance in test_data_output:
            formatted_test_data[testInstance[0]] = testInstance[1]
        
    # probably should refactor this to an output file
    with open(output_file_name, "w") as output_file:
        output_file.write(json.dumps(formatted_test_data, indent=4))

def main(argv):
    # compile llvm
    run_tests("output")

if __name__ == "__main__":
    app.run(main)
