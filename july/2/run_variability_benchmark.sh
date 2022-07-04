mkdir -p /test-output

for testSuiteDescription in /tests/*
do
    executable=$(cat $testSuiteDescription | jq '.executable' | tr -d '"')
    executableBasename=$(basename $executable)
    for i in {1..5}
    do
        python3 run_gtest_executable.py $testSuiteDescription 1 > /test-output/$executableBasename.$i.json
        echo "Finished iteration $i for $executable"
    done
    echo "Finished running all tests for $executable"
done