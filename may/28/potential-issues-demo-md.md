# Potential Issues

Lists a couple of potential issues that I have noted in demo.md as I have been working through it today.

Just opened a pull request to fix these issues [https://github.com/google/ml-compiler-opt/pull/22](here).

### compile_task flag has been deprecated

Tjhe demo still has the `--compile_task` flag when running `generate_default_trace.py` and this needs to be removed.

### demo.md gin bindings full names

When generating the default trace, the full inlining demo mentions that when calling `compiler_opt/tools/genereate_default_trace.py`, two `gin_bindings` need to be set, particularly `clang_path`, and `llvm_size_path`. I wasn't able to get these to work without using their full names, `runners.InliningRunner.clang_path`, and `runners.InliningRunner.llvm_size_path` respectively. Could be a potential issue, but I might also just be doing something wrong. The commentary in `compiler_opt/rl/problem_configuration.py` says that the commands in the demo should be correct in regards to this specifically. 

**Potential fix:** The mapping between `clang_path`/`llvm_size_path` and the `runners.InliningRunner.*` versions is included in one of the gin configuration files, particularly `compiler_opt/rl/inlining/gin_configs/common.gin`. Including this file using a `--gin_files` flag on the command line fixes everything.

### demo.md no gin binding for the implementation

As described in `compiler_opt/rl/problem_configuration.py`, when running a tool, the problem configuration implementation needs to be passed. For example, when doing it for the inliner, the correct flact would be `--gin_bindings=config_registry.get_configuration.implementation=@configs.InliningConfig`.
