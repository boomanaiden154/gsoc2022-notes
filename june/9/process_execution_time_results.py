import json
import sys

# A very simple script that copies all executing time output data 
# from the LLVM test suite microbenchmarks to a CSV for easier 
# processing in the future (eg comparison to other runs with 
# different optimizations and what not)

def getExecutionTimes(resultsFileName):
    outputs = []
    with open(resultsFileName) as resultsFile:
        resultsData = json.load(resultsFile)
        for test in resultsData["tests"]:
            if "exec_time" in test["metrics"]:
                outputs.append((test["name"],test["metrics"]["exec_time"]))
    return outputs

def writeExecutionTimes(results, outputFileName):
    with open(outputFileName, "w") as outputFile:
        for output in results:
            testName, testExecTime = output
            testName = testName.replace(",",";")
            outputFile.write(testName + "," + str(testExecTime) + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage is [process_results.py] [input file] [output file]")
        sys.exit(1)

    results = getExecutionTimes(sys.argv[1])
    writeExecutionTimes(results, sys.argv[2])
    print("Wrote data to " + sys.argv[2])