import subprocess
import os
import shutil
import json
import sys

sys.path.append("../5")

import run_llvm_test_suite

depot_tools_path = "/depot_tools"

chromium_source_path = "/chromium/src"
chromium_build_path = "./out/Release"
chromium_absolute_build_path = os.path.join(chromium_source_path, chromium_build_path)

llvm_build_path = "/llvm-build"

tests_to_build = ["base_perftests", "browser_tests", "components_perftests"]

def build_chromium_tests(regalloc_advisor):
    if os.path.exists(chromium_absolute_build_path):
        shutil.rmtree(chromium_absolute_build_path)
    
    new_environment = os.environ.copy()
    new_environment["PATH"] += depot_tools_path
    new_environment["CC"] = os.path.join(llvm_build_path, "./bin/clang")
    new_environment["CXX"] = os.path.join(llvm_build_path, "./bin/clang++")
    new_environment["AR"] = os.path.join(llvm_build_path, "./bin/llvm-ar")
    new_environment["NM"] = os.path.join(llvm_build_path, "./bin/llvm-nm")
    new_environment["CPPFLAGS"] = "-mllvm -regalloc-enable-advisor={advisor}".format(advisor=regalloc_advisor)

    gn_config_command = ["gn", "gen", chromium_build_path,
        """--args='is_official_build=true
        use_thin_lto=false
        is_cfi=false
        use_cfi=false
        use_cfi_icall=false
        use_cfi_cast=false
        clang_use_chrome_plugins=false
        is_debug=false
        symbol_level=0
        custom_toolchain="//build/toolchain/linux/unbundle:default"
        host_toolchain="//build/toolchain/linux/unbundle:default"'
    """]

    gn_config_process = subprocess.Popen(gn_config_command, env=new_environment, cwd=chromium_source_path)
    gn_config_process.wait()

    ninja_compile_command = ["autoninja", "-C", chromium_build_path]
    ninja_compile_command.extend(tests_to_build)
    ninja_compile_process = subprocess.Popen(ninja_compile_command, env=new_environment)
    ninja_compile_process.wait()

def run_tests(run_name):
    for test in tests_to_build:
        print("running test")
