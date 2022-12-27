# Using perf-stat to get loads and stores

**NOTE:** If you are running stuff inside a docker container, you need
to make sure that you are on a bare metal host and that the container
was started in privileged mode.

The linux command `perf-stat` allows you to grab information from hardware
performance counters to measure things like cycles, number of retired loads,
and the number of retired stores. The easiest way to get `perf` working inside
a docker container that has an OS whose kernel version doesn't match that of the
host is to just build `perf` inside the docker container:
```bash
git clone --depth 1 https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
cd /linux/tools/perf
make
cp perf /usr/bin
```
Make sure that dependencies are installed:
```bash
apt-get install -y flex bison libelf-dev
```

Note that there are other optional dependencies automatically detected by the
`perf` build when running it with `make`. These include things like
`libdwarf-dev`, and the (un)availability of these other dependencies might
impact some functionality. I seem to be able to get decent debug info
support with `libdwarf-dev` installed for some reason though (although it
hasn't worked for me in the past in some circumstances).

The two performance counters that we are interested in:
```
mem_uops_retired.all_stores
mem_uops_retired.all_loads
```

To run `perf stat` against a command:
```
perf stat -e mem_uops_retired.all_stores -e mem_uops_retired.all_loads [command]
```
Make sure when running this command inside of a docker container that you are
running it in privileged mode on a bare metal host.