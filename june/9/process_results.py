import json
import sys

# A very simple script that copies all output data from the LLVM test
# suite microbenchmarks to a CSV for easier processing in the future
# (eg comparison to other runs with different optimizations and 
# what not)

if len(sys.argv) != 3:
    print("Usage is [process_results.py] [input file] [output file]")
    sys.exit(1)

outputs = []

with open(sys.argv[1]) as resultsFile:
    resultsData = json.load(resultsFile)
    for test in resultsData["tests"]:
        if "MicroBenchmarks" in test["name"] and "exec_time" in test["metrics"]:
            outputs.append((test["name"],test["metrics"]["exec_time"]))

with open(sys.argv[2], "w") as outputFile:
    for output in outputs:
        testName, testExecTime = output
        outputFile.write(testName + "," + str(testExecTime) + "\n")

print("Wrote data to " + sys.argv[2])