# Using AutoFDO

After getting all of the AutoFDO tooling compiled, we can get to actually using
the tooling to do something useful. First off, we need to collect some perf data,
particularly the LBR records of the binary that we're trying to collect data
from. This can be done directly with `perf`, or it can be done the `ocperf.py`
script available in the `pmu-tools` repository. First off, clone the
`pmu-tools` repository:

```bash
git clone https://github.com/andikleen/pmu-tools
```

Then you can run the script as follows:
```bash
/path/to/pmu-tools ocperf.py record -b -e br_inst_retired.near_taken:pp -- <path to your binary>
```

This will create a `perf.data` file containing the necessary records. Then,
you can run the `create_llvm_prof` tool from the AutoFDO build to convert
this raw data into the standard AutoFDO profile format. For example:

```bash
/path/to/autofdo/build/create_llvm_prof --binary=<path to your binary> --out=<output AutoFDO profile>
```

This will by default pick up data from `perf.data` in the current working
directory. If your perf data is stored elsewhere or with a different name, you
can use the `--profile=<path to your perf data>` to point to perf data in a
different place.

Note that the binary that you use for `create_llvm_prof` (and by extension the
binary run through `ocperf.py` since they ideally should be the same binary)
needs to have debug symbols compiled in through `-g` so that the perf data can
be matched up to line numbers in the source code.

This will spit out a profile to whatever you set `<output AutoFDO profile>` to
if you've done everything correctly. Documentation on the format of this profile
can be found [here](https://llvm.org/doxygen/SampleProfReader_8h_source.html).
Note that the default format that `create_llvm_prof` is the text format, but the
format can be changed using a command line flag.

### Combining Profiles

TODO(boomanaiden154): Add this section.