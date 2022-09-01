# Chromium Test Packaging

Currently, for the purposes of benchmarking stuff with MLGO, we're interested
in three different test executables

* `browser_tests`
* `components_perftests`
* `base_perftests`

These three tests have a varietey of dependecies that are listed here:

### `components_perftests`

All of these paths are relative to the chromium build directory
(ie `/chromium/src/out/Release`) if Chromium was fetched into `/chromium/src`
and you ran `gn gen ./out/Release` from `/chromium/src`.

```
components_perftests
libEGL.so
libvk_swiftshader.so
v8_context_snapshot.bin
icudtl.dat
libGLESv2.so
libvulkan.so.1
ui_test.pak
vk_swiftshader_icd.json
```

### `base_perftests`

```
base_perftests
```

### `browser_tests`

```
browser_tests
../../components/test/data/autofill/heuristics/input
```

Make sure that the second file is actually placed two directory levels
below wherever browser_tests is placed, otherwise it will not work. If
everything is kept in the original directory structure, this should be
a non-issue.

## Creating a Tar archive

To create a tar achive containing the necessary files to run the tests,
you can use the following command, making sure that you have access to the
`file_list.txt` file wherever you're running this command:

```bash
tar -czf benchmarks.tar.gz -T file_list.txt