# Running performance counters with perf

**Note:** This needs to be done on the host system outside of a container
unless the kernel version of the container base image and host system 
match pretty closely, or you build perf from source with the right kernel
version for the host. Otherwise it will be difficult to run perf from
inside a container. You will also need to make sure that you are running
your container as privileged if running inside a container so that `perf`
can actually get the necessary data from the host kernel.

### Getting a list of all performance counters

Simply running `perf list` will give a long list of performance counters
along with some short descriptions.

### Getting data from specific performance counters

Getting data from specific performance counters for an executable can be
done pretty easily using the `perf record` command. Example:
```bash
perf stat -e instructions --repeat [repeat count] -a /path/to/executable [parameters passed to executable]
```
This will output data on the performance counters passed in a comma separated
list after the `-e` flag (in this case, just instructions, but
`mem_uops_retired.all_loads` and `mem_uops_retired.all_stores` are common
options) in a fairly consistent format that can be machine parsed. The number
of repetitions can be specified after the `--repeat` flag, which will then
have the program run multiple times, and it will output the average values
at the end along with the standard deviation express in a +/- percentage form.
Example output (slightly adjusted for spacing/display reasons):
```
# started on Thu Jun 16 15:18:01 2022

Performance counter stats for 'system wide' (5 runs):

9,594,089,858 mem_uops_retired.all_loads ( +-  0.08% )
41,616,149,444 instructions ( +-  0.08% )
2,301,318,419 mem_uops_retired.all_stores ( +-  0.70% )

0.82849 +- 0.00842 seconds time elapsed  ( +-  1.02% )
```