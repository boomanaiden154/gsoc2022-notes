# Embedding bitcode into chromium

Using all of the default flags in Chromium creates some problems when
using the unbundle toolchain and setting the `-fembed-bitcode` flag to `all`.
To fix this, I'm proposing introducing an `embed_bitcode` flag into the
Chromium build system that would prevent the introduction of all the incorrect
flags and also introduce the `-fembed-bitcode=all` flag automatically.
Shouldn't be too difficult to implement, the only thing would be trying to get
it upstreamed if I decide to try and go down that route.

### Currently interferring flags
```
clang: error: -mllvm is not supported with -fembed-bitcode
clang: error: -gdwarf-aranges is not supported with -fembed-bitcode
clang: error: -ggnu-pubnames is not supported with -fembed-bitcode
clang: error: -fdata-sections is not supported with -fembed-bitcode
clang: error: -ffunction-sections is not supported with -fembed-bitcode
clang: error: -fno-unique-section-names is not supported with -fembed-bitcode
```

* `-gdwarf-aranges`
    * All of the instances of this flag take place in
    `./build/config/compiler/BUILD.gn`. Makes sense given I was seeing them on
    the libc++ compilation.
* `-ggnu-pubnames`
    * Also present in `./build/config/compiler/BUILD.gn`. Also some misc third
    party stuff/other build configs that should be used during a standard
    x86_64 build.
* `-fdata-sections`
    * Also present in `./build/config/compiler/BUILD.gn`.
* `-ffunction-sections`
    * `./build/config/compiler/BUILD.gn`
* `-fno-unique-section-names`
    * `./build/config/compiler/BUILD.gn`
* `-mllvm -instcombine-lower-dbg-declare`
    * `./build/config/compiler/BUILD.gn`
* Unable to find plugin `find-bad-constructs`
    * The above issue can be fixed pretty easily by disabling the use of chromium plugins with clang by setting the gn flag
    `clang_use_chrome_plugins` to `false`.

### Solution

I have implemented a pretty basic patch in my chromium fork on github
implementing a `enable_bitcode` flag for the chromium gn build system. When
this flag is set to true, all the conflicting flags are automatically
disabled. The `-fembed-bitcode=all` flag isn't set though, and instead needs
to be set manually using the `CPPFLAGS` environment variable when using the
linux unbundle toolchain. Probably not going to upstream it as it's pretty
darn simple (ie not a whole ton of need for rebasing), and it probably
wouldn't be super desirable in upstream chromium.