# Building Firefox from a tarball

This guide covers building Firefox from a tarball.

Start by downloading and extracting the tarball:

```shell
curl -L https://ftp.mozilla.org/pub/firefox/releases/117.0/source/firefox-117.0.source.tar.xz > firefox.tar.xz
tar -xmf ./firefox.tar.xz
```

The additional `-m` flag in the `tar` invocation is present in case
you are cloning a file system like `tmpfs` so that `tar` doesn't
overwrite timestamos, which might result in an error.

Put the following line in the build config, which is the `mozconfig`
file:

```shell
ac_add_options --without-wasm-sandboxed-libraries
```

Then run the build:

```shell
./mach build
```

Note that this version of Firefox will only compile with Rust v1.72.0 (at least
from my testing). There is an upstream issue tracking the bug causing other
versions to fail [here](https://bugzilla.mozilla.org/show_bug.cgi?id=1849869).

