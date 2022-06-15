import sys
import json

def loadBenchmark(fileName):
    output = []
    with open(fileName) as inputFile:
        inputData = json.load(inputFile)
        for benchmark in inputData["benchmarks"]:
            outputBenchmark = {
                "name": benchmark["name"],
                "real_time": benchmark["real_time"],
                "cpu_time": benchmark["cpu_time"],
                "iterations": benchmark["iterations"],
                "instructions": benchmark["INSTRUCTIONS"],
                "loads": benchmark["MEM_UOPS_RETIRED:ALL_LOADS"],
                "stores": benchmark["MEM_UOPS_RETIRED:ALL_STORES"]
            }
            output.append(outputBenchmark)
    return output

def getResultMap(benchmarks, parameterOfInterest):
    output = {}
    for benchmark in benchmarks:
        output[benchmark["name"]] = benchmark[parameterOfInterest]
    return output

if __name__ == "__main__":
    print("Using as a command line script is not currently implemented")