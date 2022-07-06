import subprocess
import os
import shutil
import tensorflow
import json

from absl import flags

llvm_test_suite_path = "/llvm-test-suite"
llvm_build_path="/llvm-project/build"
llvm_source_path="/llvm-project"

llvm_test_suite_build_path = os.path.join(llvm_test_suite_path, "./build")

llvm_c_compiler_path = os.path.join(llvm_build_path, "./bin/clang")
llvm_cxx_compiler_path = os.path.join(llvm_build_path, "./bin/clang++")

llvm_lit_path = os.path.join(llvm_build_path, "./bin/llvm-lit")

test_suites = [
    "harris/harris",
    "SLPVectorization/SLPVectorizationBenchmarks",
    "MemFunctions/MemFunctions",
    "LoopVectorization/LoopVectorizationBenchmarks",
    "LoopInterchange/LoopInterchange",
    "LCALS/SubsetALambdaLoops/lcalsALambda",
    "LCALS/SubsetARawLoops/lcalsARaw",
    "LCALS/SubsetBLambdaLoops/lcalsBLambda",
    "LCALS/SubsetBRawLoops/lcalsBRaw",
    "LCALS/SubsetCLambdaLoops/lcalsCLambda",
    "LCALS/SubsetCRawLoops/lcalsCRaw",
    "ImageProcessing/AnisotropicDiffusion/AnisotropicDiffusion",
    "ImageProcessing/BilateralFiltering/BilateralFilter",
    "ImageProcessing/Blur/blur",
    "ImageProcessing/Dilate/Dilate",
    "ImageProcessing/Dither/Dither",
    "ImageProcessing/Interpolation/Interpolation",
    "Builtins/Int128/Builtins"
]

def build_llvm(model_path, use_existing_build):
    if not use_existing_build and os.path.exists(llvm_build_path):
        shutil.rmtree(llvm_build_path)

    cmake_config_command = ["cmake", "-G", "Ninja",
        "-DLLVM_RAEVICT_MODEL_PATH={model_path}".format(model_path=model_path)]

    if use_existing_build:
        cmake_config_command.append(".")
    else:
        tensorflow_aot_path = os.path.dirname(tensorflow.__file__)
        cmake_config_command.extend([
            "-DCMAKE_BUILD_TYPE=Release",
            "-DTENSORFLOW_C_LIB_PATH=/tmp/tensorflow",
            "-DTENSORFLOW_AOT_PATH='{aot_path}'".format(aot_path=tensorflow_aot_path),
            "-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON",
            "-DLLVM_ENABLE_PROJECTS='clang'",
            "-DLLVM_ENABLE_RUNTIMES='compiler-rt'",
            "{source_path}".format(source_path=llvm_source_path)
        ])
    
    cmake_config_process = subprocess.Popen(cmake_config_command, cwd=llvm_build_path)
    cmake_config_process.wait()

    cmake_compile_command = ["cmake", "--build", "."]
    cmake_compile_process = subprocess.Popen(cmake_compile_command, cwd=llvm_build_path)
    cmake_compile_process.wait()

    # new llvm compile should be ready to go

def build_test_suite(regalloc_advisor):
    if os.path.exists(llvm_test_suite_build_path):
        shutil.rmtree(llvm_test_suite_build_path)
    
    os.makedirs(llvm_test_suite_build_path)

    cmake_config_command_stage_1 = ["cmake", "-G", "Ninja",
        "-DTEST_SUITE_PROFILE_GENERATE=ON",
        "-DTEST_SUITE_RUN_TYPE=train",
        "-DCMAKE_C_COMPILER={clang}".format(clang=llvm_c_compiler_path),
        "-DCMAKE_CXX_COMPILER={clangxx}".format(clangxx=llvm_cxx_compiler_path),
        "-DCMAKE_CXX_FLAGS='-mllvm -regalloc-enable-advisor={regalloc_advisor}'".format(regalloc_advisor=regalloc_advisor),
        "-DCMAKE_C_FLAGS='-mllvm -regalloc-enable-advisor={regalloc_advisor}'".format(regalloc_advisor=regalloc_advisor),
        "-DBENCHMARK_ENABLE_LIBPFM=ON",
        "-DTEST_SUITE_BENCHMARKING_ONLY=ON",
        "../"]

    cmake_stage_1_process = subprocess.Popen(cmake_config_command_stage_1, cwd=llvm_test_suite_build_path)
    cmake_stage_1_process.wait()

    cmake_compile_command = ["cmake", "--build", "."]
    cmake_stage_1_build_process = subprocess.Popen(cmake_compile_command, cwd=llvm_test_suite_build_path)
    cmake_stage_1_build_process.wait()

    lit_test_runner_command = ["{lit_path}".format(lit_path=llvm_lit_path), "."]
    
    lit_test_runner_process = subprocess.Popen(lit_test_runner_command, cwd=llvm_test_suite_build_path)
    lit_test_runner_process.wait()

    cmake_config_command_stage_2 = ["cmake", "-G", "Ninja",
        "-DTEST_SUITE_PROFILE_GENERATE=OFF",
        "-DTEST_SUITE_PROFILE_USE=ON",
        "-DTEST_SUITE_RUN_TYPE=ref",
        "."]
    
    cmake_stage_2_process = subprocess.Popen(cmake_config_command_stage_2, cwd=llvm_test_suite_build_path)
    cmake_stage_2_process.wait()

    cmake_stage_2_build_process = subprocess.Popen(cmake_compile_command, cwd=llvm_test_suite_build_path)
    cmake_stage_2_build_process.wait()

    # llvm test suite is now built and ready to go

def loadFileGrabBenchmarks(fileName):
    with open(fileName) as inputFile:
        data = json.load(inputFile)
        return data["benchmarks"]

def writeBenchmarks(benchmarksToWrite, outputFileName):
    output = {"benchmarks": benchmarksToWrite}
    with open(outputFileName, "w") as outputFile:
        json.dump(output, outputFile)


def run_tests(run_name):
    completed_benchmark_files = []
    for test_suite in test_suites:
        test_suite_basename = os.path.basename(test_suite)
        output_file = os.path.join("/tmp", "{basename}.json".format(basename=test_suite_basename))
        test_runner_command = [
            os.path.join(llvm_test_suite_build_path, "MicroBenchmarks/{test_suite}".format(test_suite=test_suite)),
            "--benchmark_perf_counters=INSTRUCTIONS,MEM_UOPS_RETIRED:ALL_LOADS,MEM_UOPS_RETIRED:ALL_STORES",
            "--benchmark_out_format=json",
            "--benchmark_out={out_file}".format(out_file=output_file)
        ]

        test_runner_process = subprocess.Popen(test_runner_command)
        test_runner_process.wait()

        completed_benchmark_files.append(loadFileGrabBenchmarks(output_file))
    
    writeBenchmarks(completed_benchmark_files, "{run_name}.json".format(run_name=run_name))

if __name__ == "__main__":
    print("hello world")