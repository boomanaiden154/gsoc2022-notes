import json
import sys
import glob

WORKDIR = "/llvm-test-suite/build/"

def loadFileGrabBenchmarks(fileName):
    with open(fileName) as inputFile:
        data = json.load(inputFile)
        return data["benchmarks"]

def grabAllBenchmarks():
    allBenchmarks = []
    for file in glob.glob(WORKDIR + "*.json"):
        print(file)
        allBenchmarks.extend(loadFileGrabBenchmarks(file))
    return allBenchmarks

def writeBenchmarks(benchmarksToWrite, outputFileName):
    output = {"benchmarks": benchmarksToWrite}
    with open(outputFileName, "w") as outputFile:
        json.dump(output, outputFile)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: [combine-benchmarks.py] [output file name]")

    benchmarks = grabAllBenchmarks()
    writeBenchmarks(benchmarks, sys.argv[1])