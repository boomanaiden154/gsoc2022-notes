# Using Taskset and isolcpus

When benchmarking, it can be useful to ensure that the OS process scheduler
doesn't interfere with the results by switching out the benchmark program
between cores, or if load is high enough switching it out altogether for a
period of time. This can be achieved in Linux by using the `isolcpus`
kernel flag as well as the `taskset` command.

### The isolcpus flag

Setting the `isolcpus` kernel command line flag tells the linux shceduler to
completely ignore certain CPUs, except if they're explicitly requested using
the taskset command. CPUs are numbered starting at 0. For example, to disable
the first 12 CPUs on 16 core system (not considering hyperthreading), you
would add the following to the kernel command line:

```
isolcpus=0,1,2,3,4,5,6,7,8,9,10,11
```

### Taskset

To assign processes to these CPUs, you need to use the `taskset` command.
You can use core masks specified in hexadecimal to run a program on a
specific core(s):

```
taskset 0x1 <program>
```

Or you can also specify a core list with the `-c` option:

```
taskset -c <comma separated core list> <program>
```