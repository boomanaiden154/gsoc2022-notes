# LLVM MLGO CMake notes

### Model path flags

The `LLVM_RAEVICT_MODEL_PATH` flag in CMake is equivalant to the
`LLVM_INLINER_MODEL_PATH` flag for the machine learning based inliner.
Just setting one of these to `"download"` will cause the model to be
downloaded from the current URL. This is based on the `tf_find_and_compile`
function that is defined in `/llvm-project/cmake/modules/Tensorflow/TensorFlowCompile.cmake`.
Relevant code excerpt:
```cmake
if ("${model}" STREQUAL "download")
    # Crash if the user wants to download a model but a URL is set to "TO_BE_UPDATED"
    if ("${default_url}" STREQUAL "TO_BE_UPDATED")
        message(FATAL_ERROR "Default URL was set to 'download' but there is no"
        " model url currently specified in cmake - likely, the model interface"
        " recently changed, and so there is not a released model available.")
    endif()

    set(model ${default_url})
endif()
```
These models seem to be set by default to `autogenerate` which generates
a mock model for testing, probably with randomly initialized weights and
what not, so not really what we want for testing.

### CMake version

For the version of Ubuntu that I have been using (20.04), the current CMake
version (3.16.x) doesn't have the `ARCHIVE_EXTRACT` function, which is needed
by the MLGO CMake stuff in LLVM in order to extract the model archives
downloaded from Github. To get the latest version of CMake on focal fossa:
```bash
# uninstall CMake if you already have it installed
apt-get remove cmake
wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | tee /usr/share/keyrings/kitware-archive-keyring.gpg >/dev/null
echo 'deb [signed-by=/usr/share/keyrings/kitware-archive-keyring.gpg] https://apt.kitware.com/ubuntu/ focal main' | sudo tee /etc/apt/sources.list.d/kitware.list >/dev/null
apt-get update
apt-get install -y cmake
# This should now say the latest version of CMake (3.23.x as of time of writing)
cmake --version
```