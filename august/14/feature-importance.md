# Feature Importance

Hopefully some tooling in [ml-compiler-opt](https://github.com/google/ml-compiler-opt)
that proves to be quite useful.

### Running the script

The script grabs data from a trace ran with `generate_default_trace` with the policy under
analysis located at `/default_trace` (just reusing existing files for right now, this needs
to be changed at a later date).

```bash
PYTHONPATH=$PYTHONPATH:. python3 compiler_opt/tools/feature_importance.py \
    --gin_files=compiler_opt/rl/regalloc/gin_configs/common.gin \
    --gin_bindings=config_registry.get_configuration.implementation=@configs.RegallocEvictionConfig \
    --data_path=/default_trace \
    --model_path=/warmstart/saved_policy
```