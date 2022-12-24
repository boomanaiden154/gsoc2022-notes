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

Merging profiles can be done fairly simply. Assuming the output format should
be plaintext and that we're using llvm profiles, the following command can
be used:

```bash
/path/to/autofdo/profile_merger --is_llvm=true --format=text <input afdo files>
```

However, the `profile_merger.cc` file that gets compiled into the
`profile_merger` binary seems to have an error that prevents the flags from
getting processed as flags. They instead get processed as flags and as
input files, which is a problem since then the profile reader errors out.
This patch seems to fix things, but I might just not be understanding how
everything is supposed to work:

```patch
diff --git a/profile_merger.cc b/profile_merger.cc
index 9cff132..ffc4204 100644
--- a/profile_merger.cc
+++ b/profile_merger.cc
@@ -129,7 +129,7 @@ bool verifyProperFlags(bool has_prof_sym_list) {
 
 int main(int argc, char **argv) {
   absl::SetProgramUsageMessage(argv[0]);
-  absl::ParseCommandLine(argc, argv);
+  std::vector<char*> positionalArguments = absl::ParseCommandLine(argc, argv);
   devtools_crosstool_autofdo::SymbolMap symbol_map;
 
   if (argc < 2) {
@@ -155,10 +155,10 @@ int main(int argc, char **argv) {
     std::unique_ptr<AutoFDOProfileReaderPtr[]> readers(
         new AutoFDOProfileReaderPtr[argc - 1]);
     // TODO(dehao): merge profile reader/writer into a single class
-    for (int i = 1; i < argc; i++) {
+    for (int i = 1; i < positionalArguments.size(); i++) {
       readers[i - 1] =
           std::make_unique<AutoFDOProfileReader>(&symbol_map, true);
-      readers[i - 1]->ReadFromFile(argv[i]);
+      readers[i - 1]->ReadFromFile(positionalArguments[i]);
     }
 
     symbol_map.CalculateThreshold();
@@ -173,7 +173,7 @@ int main(int argc, char **argv) {
     typedef std::unique_ptr<LLVMProfileReader> LLVMProfileReaderPtr;
 
     std::unique_ptr<LLVMProfileReaderPtr[]> readers(
-        new LLVMProfileReaderPtr[argc - 1]);
+        new LLVMProfileReaderPtr[positionalArguments.size() - 1]);
     llvm::sampleprof::ProfileSymbolList prof_sym_list;
 
 #if LLVM_VERSION_MAJOR >= 12
@@ -181,11 +181,11 @@ int main(int argc, char **argv) {
     int numFSDProfiles = 0;
 #endif
 
-    for (int i = 1; i < argc; i++) {
+    for (int i = 1; i < positionalArguments.size(); i++) {
       auto reader = std::make_unique<LLVMProfileReader>(
           &symbol_map, names,
           absl::GetFlag(FLAGS_merge_special_syms) ? nullptr : &special_syms);
-      CHECK(reader->ReadFromFile(argv[i])) << "when reading " << argv[i];
+      CHECK(reader->ReadFromFile(positionalArguments[i])) << "when reading " << positionalArguments[i];
 
 #if LLVM_VERSION_MAJOR >= 12
       if (reader->ProfileIsFS()) {
```