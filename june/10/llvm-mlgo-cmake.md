# LLVM MLGO CMake notes

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