import sys
import statistics

def loadResults(fileName):
    output = {}
    with open(fileName) as inputFile:
        for line in inputFile:
            parts = line.rstrip().split(",")
            output[parts[0]] = float(parts[1])
    return output

def constructComparisons(resultMap1, resultMap2):
    output = []
    for resultName in resultMap1:
        if resultName in resultMap2:
            output.append((resultMap1[resultName],resultMap2[resultName]))
    return output

def calculateAverageChange(comparisonsList):
    changes = []
    for comparison in comparisonsList:
        result1, result2 = comparison
        changes.append(result2 / result1)
    return statistics.geometric_mean(changes)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage is [compare_results.py] [input file 1] [input file 2]")
    
    resultMap1 = loadResults(sys.argv[1])
    resultMap2 = loadResults(sys.argv[2])
    comparisons = constructComparisons(resultMap1, resultMap2)
    print(calculateAverageChange(comparisons))