# Clang Not Throwing Error When Profile Path is Incorrect When Compiling IR

Currently, when clang is run with `-cc1` and the `-x ir` flag is used, when
a profile passed in with `-fprofile-instrument-use-path` doesn't actually
exist (ie the path is wrong), there is no error thrown. There should be an
error thrown here and there is an error thrown in the default case (as shown
by the `profile-does-not-exist.c` regression test for clang), but somehow
the error gets eaten when compiling IR.

### Replication

Start off by creating an empty source file:

```bash
touch test.c
```

Now, examine the difference in output between compiling directly from c rather
than IR:

```bash
clang -cc1 -emit-llvm test.c -o - -fprofile-instrument-use-path=/fake
```

This will output the following:

```
error: Could not read profile /fake: No such file or directory
```

and compiling from IR (with the `-x ir` flag):

```bash
clang -cc1 -emit-llvm -x ir test.c -o - -fprofile-instrument-use-path=/fake
```

Which will output the following:

```
warning: overriding the module target triple with x86_64-unknown-linux-gnu [-Woverride-module]
; ModuleID = 'test.c'
source_filename = "test.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"
1 warning generated.
```

Only a warning with no mention of the instrumented profile path not actually
existing. When actually compiling IR (eg when training a MLGO model), the error
gets eaten as well.

### Fix

Fixed by just capturing the error when it is originally detected rather than shuffling it
along to `CodeGenModule` which doesn't get called when compiling IR.

A patch has been opened [here](https://reviews.llvm.org/D132991)