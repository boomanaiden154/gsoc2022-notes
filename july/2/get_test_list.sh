testSuites=$(cat tests.txt)

for testSuite in ${testSuites[@]}; do
    autoninja -C /chromium/src/out/Release $testSuite
done

for testSuite in ${testSuites[@]}; do
    python3 parse_gtests.py /chromium/src/out/Release/$testSuite > $testSuite.json
done