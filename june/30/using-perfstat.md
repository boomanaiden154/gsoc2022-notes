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
apt-get install -y flex bison
```
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