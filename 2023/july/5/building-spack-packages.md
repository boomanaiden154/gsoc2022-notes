# Building Spack Packages

Building a spack package while keeping the build stage and embedding bitcode
into the object files:
```bash
spack install --keep-stage libiconv %clang@15.0.7 cflags=\"-Xclang -fembed-bitcode=all\"
```

Notice the escaped quotes. If the quotes aren't escaped, the shell might get rid of
them and spack will fail with compiler flag tokenization errors.

Flags:
* `%clang@15.0.7` - Specifies the compiler and the version.
* `cflags=\"-Xclang -fembed-bitcode=all\"` - Specifies the C compiler flags to
pass along, in this case passing -fembed-bitcode=all to the clang cc1 frontend
to make it produce object files with `.llvmbc` and `.llvmcmd` sections.
* `--keep-stage` - Makes spack keep the build stage rather than deleting it upon
a successful build.

Spack will put the build stage at a directory specified by the spack `config.yaml`
as documented [here](https://spack.readthedocs.io/en/stable/config_yaml.html).

