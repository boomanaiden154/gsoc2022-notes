import json
import sys

def getCompileTimes(resultsFileName):
    output = []
    with open(resultsFileName) as resultsFile:
        results = json.load(resultsFile)
        for test in results["tests"]:
            if "compile_time" in test["metrics"]:
                output.append((test["name"],test["metrics"]["compile_time"]))
    return output

def writeCompileTimes(results, outputFileName):
    with open(outputFileName, "w") as outputFile:
        for result in results:
            testName, compileTime = result
            testName = testName.replace(",",";")
            outputFile.write(testName + "," + str(compileTime) + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage is [process_compile_time_results.py] [input file] [output file]")
    
    compileTimeResults = getCompileTimes(sys.argv[1])
    writeCompileTimes(compileTimeResults, sys.argv[2])