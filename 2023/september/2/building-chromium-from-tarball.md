# Building Chromium from a tarball

Start off by building GN:

```shell
git clone https://gn.googlesource.com/gn
cd gn
python3 build/gen.py
ninja -C out
export PATH=$PATH:$(pwd)/out
cd ..
```

First you need to download the tarball:

```shell
curl -L https://commondatastorage.googleapis.com/chromium-browser-official/chromium-116.0.5845.140.tar.xz > chromium.tar.xz
```

Next, unpack it:

```shell
tar -xf chromium.tar.xz
cd ./chromium-116.0.5845.140
```

Setup node within the directory:

```shell
mkdir -p third_party/node/linux/node-linux-x64/bin
ln -s /usr/bin/node third_party/node/linux/node-linux-x64/bin/
```

Then setup the build (you will need to have an existing gn installation in order
for this work)

```shell
export CC=clang
export CXX=clang++
export AR=llvm-ar
export NM=llvm-nm
export CFLAGS="-Wno-error=format -Wno-error=shadow"
export CXXFLAGS="-Wno-error=format -Wno-error=shadow"
gn ./out/Release
```

Make sure to put the following config in the gn arguments:

```
is_official_build=true
use_thin_lto=false
is_cfi=false
use_cfi_icall=false
use_cfi_cast=false
clang_use_chrome_plugins=false
is_debug=false
symbol_level=0
enable_rust=false
use_sysroot=false
use_qt=false
clang_base_path="/usr"
enable_nacl=false
use_vaapi=false
custom_toolchain="//build/toolchain/linux/unbundle:default"
host_toolchain="//build/toolchain/linux/unbundle:default"
```
