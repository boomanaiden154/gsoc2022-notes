# LLVM Benchmarking Utilities/Scripts

After getting a `results.json` output from the LLVM test suite, now
the data needs to be processed to actually mean something. First off,
let's extract just the execution times of benchmarks in the 
`MicroBenchmarks/` subfolder since this is what we actually want. All
of these benchmarks are run using google benchmark which does things
like rerun benchmarks until a statistically significant value can be
reported, which will help eliminate a lot of the noise that will otherwise
create a lot of confounding results. To do this:
```bash
python3 process_execution_time_results.py /path/to/results.json /path/to/output.csv
```
This will create an `output.csv` file in the format:
```
benchmark name, execution time
```
This data can be imported for analysis, or compared against another
run using the following script:
```bash
python3 compare_results.py /path/to/output1.csv /path/to/output2.csv
```
This will print info on the overall relative runtime (presented as a 
percentage) that run2 had compared to run1. The same process can be
done for analyzing compile times by substituting
`process_execution_time_results.py` in the first command (the one for
generating the CSVs) to `process_compile_time_results.py`. This will
generate CSVs of the same format, but with the second column being
compile times instead of execution times.