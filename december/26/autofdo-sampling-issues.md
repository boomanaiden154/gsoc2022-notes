# AutoFDO Sampling Issues

When using AutoFDO to try and get accurate estimates of function call counts,
or even just the ratio between them, with my current setup I seem to be
running into a decent number of issues with sampling. For example, compiling
(without optimizations) and running the following program:
```c
#include <stdio.h>

void testaa() {
  return;
}

void testbb() {
  return;
}

int testa(int input) {
  int toreturn = 0;
  for(int i = 0; i < 1000000; ++i) {
    testaa();
    ++toreturn;
  }
  return toreturn;
}

int testb(int input) {
  int toreturn = 0;
  for(int i = 0; i < 500000; ++i) {
    testbb();
    ++toreturn;
  }
  return toreturn;
}

void thing() {
  int total = 0;
  for(int i = 0; i < 1000; ++i) {
    total += testa(i);
    total += testb(i);
  }
  printf("%d\n", total);
}

int main() {
  thing();
  return 0;
}
```

with the following compiler invocation:
```bash
/llvm-project/build/bin/clang -g -o test
```

And the following profiling:
```bash
for i in {1..2}
do
    /pmu-tools/ocperf.py record -b -e br_inst_retired.near_taken:pp -- ./test
    /autofdo/build/create_llvm_prof --binary=./test --format=text --out=./test.afdo.$i
done
/autofdo/build/profile_merger --format=text --is_llvm=true --output_file=./test.afdo *.afdo.*
```

Ends up producing the following AutoFDO profile:
```
testa:225105:0
 0: 0
 1: 0
 2: 75035
 3: 75035 testaa:42153
 4: 75035
 6: 0
testaa:150070:84078
 0: 75035
 1: 75035
testb:112575:0
 0: 0
 1: 0
 2: 37525
 3: 37525 testbb:20972
 4: 37525
 6: 0
testbb:75050:41989
 0: 37525
 1: 37525
```

The head counts for `testaa` and `testbb`, 84078 and 41989 respectively make
some sense as they're in a 2:1 ratio, which is what we would expect given
the ranges in the for loops in `testa` and `testb`. However, the entry count
information for `testa` and `testb` doesn't even really exist. I'm guessing
this is occurring because there are so many branches being executed within
each function that when each sample is made, it's not picking up on the
branches from `thing` into `testa` or `testb` since the frequency of hitting
one of those is quite low. I might be running into something else though.
In order to fix this my first thought was to just massively increase the
sampling rate of `perf` through the `--freq` flag, but beyond capturing
about 600MB of data, perf starts complaining about a lack of CPU/IO
overhead. I've tried experimenting with just the perf events for calls and
returns which should only give me function level information, and that didn't
work with the AutoFDO tooling well, at least with how I tried it. Might need
some more experimentation though. Can't think of a good way to fix this issue
outside of just processing massive amounts of information, but there's probably
a better way to make sure this information is more accurate.

Another obvious method would be to apply a correction to the call count based
on the number of samples within the function, but that requires some small
entry count information to be there in the first place and probably still a lot
of data for things to average out to some degree.