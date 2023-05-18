# Minor Advanced Build Bug?

When doing a three stage PGO/ThinLTO/BOLT build, when calling ninja
on the `stage2-distribution target`, the following shows up towards the very
end of the build:

```
[2867/2868] Performing stage2-install-distribution for 'stage2-instrumented'
[1/4] Clearing old profraw data
[1/4] Generating clang PGO data
-- Testing: 1 tests, 1 workers --
Testing:  0.. 10.. 20.. 30.. 40.. 50.. 60.. 70.. 80.. 90.. 

Testing Time: 1.78s
  Passed: 1
[3/4] Merging profdata
[3/4] Performing install-distribution for 'stage2'
```

It seems like this target is generating the PGO data again even though it
has already done so for both the BOLT case and the PGO case and both sets of
data have already been used in optimizations. Seems like there might be a stray
dependency somewhere. Probably need to do some more investigation.

Should probably also file a bug.
