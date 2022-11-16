# Assertion failure in three stage LLVM PGO build

For whatever reason, I'm getting a failure in some of the PGO code when
compiling the `llvm-profdata` target using PGO data generated from doing
a full build of LLVM/Clang/LLD, running the `check-clang` target, and
running the `check-llvm` target. Not exactly sure why this is occurring,
but taking the preprocessed source and using the flags outputted by clang
in the crash report doesn't reproduce the issue using the same profile data.
Difference there might be the use of `-cc1` rather than the driver, but I'm
not totally sure.

This was happening in this commit:
`1f67dc8b7c225290d1b3eb93d90e2c9861aeefc0`

Docker file for some? reproducibility:
[Dockerfile](https://github.com/boomanaiden154/dev-docker-vm-sh/blob/6a9fe9f8e3c44d13adc0f5f21bc53a5d39d68368/docker/llvm-pgo-corpus/Dockerfile)

Definitely some weird stuff going on (maybe in my setup, but even then I still
don't think it should result in an assertion failure), but I don't really have
time to debug at the moment, and the fact that it doesn't fail with `-cc1` on
the preprocessed source is even more weird. Leaving this here in case I for
some reason have a lot of time to work on a Clang/LLVM bug.