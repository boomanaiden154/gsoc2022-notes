# Instructions for using Chromium data processing scripts

This folder contains a set of scripts that can be used to process raw Chromium
benchmark data produced through the Catapult infrastructure. There are still
a couple problems with these scripts that need to be sorted out, but they work
for the most part.

### Known Limitations

Some of the benchmark sets produced through Catapult also create a historogram
within the file that contains the total or average of all the benchmarks contained
within the file. This can sometimes be in the opposite direction of the rest of the
benchmarks (ie in terms of lower/higher is better) and skew the geometric mean
of all the results.

There also seems to be some issues with how the results are getting aggregated
by `process_test_suites.py`. Eg there will be some tests with a standard deviation
three times the mean because it seems like the values are getting aggregated
incorrectly.

TODO(boomanaiden154): Figure out the best way to exclude these from the overall
counts. Direct exclusion should work, especially as I'll probably move to just
looking at octane and the speedometer tests.

TODO(boomanaiden154): Fix incorrect result aggregation by `process_test_suite.py`

### Usage

The usage is detailed pretty well in the `process-data.sh` script, which
automatically loops through all the test suites in the `processing_dir`
folder (a variable specified inside the script). However, the scripts
are also documented here.

##### JSON Extraction

The `extract_json.py` script will take an HTML file as input and extract the
raw JSON data from that file and dump it into STDOUT where it can then be piped
into a file through the shell.

##### JSON processing

The `process_json.py` script takes in the raw JSON and then puts everything
together and ignores a lot of stuff to assign raw values to individual test
runs and also outputs their names and labels to a file.

##### Test Suite Processing

The `process_test_suite.py` script takes in the processed JSON and then
aggregates all the data to find average values for benchmarks. It also
reports some statistics and the raw values, particularly the standard deviation.
All the benchmarks are aggregated per label, so no comparisons are made.

##### Test Suite Comparison

The `compare_test_suites.py` script takes in the output JSON file from the
`process_test_suite.py` script and then does a ratio comparison of the means
of each benchmark set across labels. The output file consists of a list of
benchmarks with the original mean values and the ratio comparison value.

##### Result Summarization

The `results_summary.py` script takes in the output file from `compare_test_suites.py`
and then gives a summary (the geometric mean) of the comparisons in the file.

##### Full script

The `process-data.sh` script goes through an entire directory of data and prints out
per benchmark comparisons. The setup is a little bit specific to my system/config,
but it is a simple script and should be easy to adapt.
