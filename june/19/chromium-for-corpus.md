# Using Chromium as a corpus for training

Using Chromium as a corpus shouldn't be that difficult. The main things
necessary for preparing a regalloc corpus are just a working build system
and a standard `compile-commands.json` file that the ml-compiler-opt
tooling can be pointed at. Chromium uses a nonstandard build system, but is
still able to export a `compile-commands.json` file. After that, for
regalloc specifically, it can be useful to disable ThinTLO (at least for
most trainings), and enable PGO. Chromium already has PGO profiles
available and ThinLTO is disabled by default.

### Preparing a Chromium corpus

This section is mostly adapated from [this](https://chromium.googlesource.com/chromium/src/+/main/docs/linux/build_instructions.md) page.

Start off by cloning the `depot_tools` repository so that you have the
necessary tools present to clone the chromium source:
```bash
git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
export PATH="$PATH:/depot_tools
```
Then you can create a folder for the chromium source and begin the
cloning process:
```bash
mkdir /chromium
cd /chromium
fetch --nohooks chromium
```
All of the code and important stuff will be pulled into the `./src`
directory. Now, install the depencies (`install-build-deps.sh` assumes
a debian based linux environment) and run other setup/prebuild procedures:
```bash
cd ./src
./build/install-build-deps.sh
gclient runhooks
```
Now, the actual build can be configured using Google's `gn` build tool.
There are a couple settings that need to be changed to make this a
decent/workable corpus. First off, we need to tell `gn` to export a
`compile-commands.json` file. We also need to make sure that we are doing
a release mode build as the default chromium build includes all debug
symbols, and that PGO is enabled/ThinLTO is disabled:
```bash
gn gen out/Default --export-compile-commands
```
TODO(boomanaiden154): figure out gn flags, maybe just is_official_build=true along with setting some flags in the gclient config before running the build to ensure the PGO profiles get checked out. Still need to confirm that ThinLTO gets disabled.