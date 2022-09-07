# Chromium Test Packaging

For each chromium test, there is a `*.runtime_deps` file associated with it
that contains a list of all the files that specific test needs to run. This
file cannot be piped directly into a command like `tar`, but with a little bit
of manipulation to these paths in Python, we can easily feed them into `tar`
and package the tests so that we can run them on other computers without needing
to move around the whole Chromium tree.

Python script:
```python
import json
import os

tests_to_package = ['base_perftests', 'browser_tests', 'components_perftests', 'base_unittests', 'cc_unittests', 'components_unittests', 'content_unittests']

test_dependencies = []

if __name__ == '__main__':
    for test_to_package in tests_to_package:
        with open(f'{test_to_package}.runtime_deps') as runtime_deps:
            for line in runtime_deps:
                test_dependencies.append(os.path.normpath(os.path.join('chromium/src/out/Release', line.rstrip())))
    
    output_deps = [*set(test_dependencies)]
    for output_dep in output_deps:
        print(output_dep)
```

Adjust the values depending upon what specific test you want to run.

TODO(boomanaiden154): rewrite into a nice script that has flags and what not.

Then you can run `tar` using the output of the script:
```bash
python3 package_test.py > file_list
tar -czf test_package.tar.gz -T file_list
```

Then you can unpack this wherever you want to run the test.