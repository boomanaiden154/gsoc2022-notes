# Writing a LLVM pass

The easiest way to create a LLVM pass currently is to do it in tree and using the old pass manager. To start off, create a new folder in `/llvm/lib/Transforms/` with the name of the transform that you want, although the folder name doesn't even have to be related at all to the name of your transform. For this example, after being in the LLVM source directory root, let's create a pass called `Hello2` as there is already an example pass called `Hello`:

```bash
mkdir /llvm/lib/Transforms/Hello2
```

Then, we need to setup a `CMakeLists.txt` in our new pass directory by adding the following to the file:

```cmake
add_llvm_library(LLVMHello2 Module
    Hello2.cpp
    PLUGIN_TOOL
    opt
)
```

After this, it is important to register this subdirectory in the `CMakeLists.txt` file of `/llvm/lib/Transforms`. The file will probably look something like this already:

```cmake
add_subdirectory(Utils)
add_subdirectory(Instrumentation)
add_subdirectory(AggressiveInstCombine)
add_subdirectory(InstCombine)
add_subdirectory(Scalar)
add_subdirectory(IPO)
add_subdirectory(Vectorize)
add_subdirectory(Hello)
add_subdirectory(ObjCARC)
add_subdirectory(Coroutines)
add_subdirectory(CFGuard)
```

Then, add the following line to it in order to tell the LLVM CMake build process to build your pass:

```cmake
add_subdirectory(Hello2)
```

Now, we can start working on the actual pass. To start off, create a new file in the `Hello2/` directory called `Hello2.cpp` as referenced earlier by the `CMakeLists.txt` that we set up. Then, include some headers:

```cpp
#include "llvm/Pass.h"
#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"

#include "llvm/IR/LegacyPassManager.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"
```

Now, let's get some boilerplate code written:

```cpp
using namespace llvm;

namespace
{
    struct Hello2: public FunctionPass
    {
        static char ID;
        Hello2(): FunctionPass(ID) {}
        bool runOnFunction(Function &F) override
        {
            //cool code goes here
        }
    }
}

char Hello2::ID = 0;
static RegisterPass<Hello2> X("hello2", "hello2 world pass", false, false);
static RegisterStandardPasses Y(
    PassManagerBuilder::EP_EarlyAsPossible,
    [](const PassManagerBuilder &Builder,
        legacy::PassManagerBase &PM) { PM.add(new Hello2()); });
```

All of the important stuff with this specific pass happens inside the `runOnFunction` function. It gets run on every single function that the pass hits when run. Outside of the anonymous namespace, the pass gets registered. The stuff that really matters is right after the setting of the ID. The `RegisterPass` template sets a name and description that will be needed later when calling the pass using other tools. 

Now, let's make the pass actually do something. Inside of the `runOnFunction` function, put the following code:

```cpp
errs() << "Hello: ";
errs().write_escaped(Name()) << '\n';
return false;
```

This will make the pass print `Hello: [function name here]` for every single function it encounters to the standard error output. The function returns false as it hasn't modified the function it's being run on at all. If it modifies the function, then it should return true. The full file currently looks like this:

```cpp
#include "llvm/Pass.h"
#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"

#include "llvm/IR/LegacyPassManager.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"


using namespace llvm;

namespace
{
    struct Hello2: public FunctionPass
    {
        static char ID;
        Hello2(): FunctionPass(ID) {}
        bool runOnFunction(Function &F) override
        {
            errs() << "Hello: ";
            errs().write_escaped(Name()) << '\n';
            return false;
        }
    }
}

char Hello2::ID = 0;
static RegisterPass<Hello2> X("hello2", "hello2 world pass", false, false);
static RegisterStandardPasses Y(
    PassManagerBuilder::EP_EarlyAsPossible,
    [](const PassManagerBuilder &Builder,
        legacy::PassManagerBase &PM) { PM.add(new Hello2()); });
```

Now, compiling this should be as simple as just running an incremental build on an already built version of LLVM/clang (instructions are present in a previous article). The following command should do it:

```bash
cmake --build .
```

Now, we actually need to run the pass on something. Create the following file and call it `test.c`:

```c
#include <stdio.h>
#include <string.h>

int getTest2(int test)
{
        return test * 4;
}

int getTest(int test)
{
        return test + 2;
}

int main()
{
        char greeting[] = "testing, this is just a test";
        int sum;
        for(int i = 0; i < strlen(greeting); i++)
        {
                sum += greeting[i];
                if(i > 0)
                {
                        sum += (int)greeting[i - 1];
                }
        }
        printf("%i\n", getTest(sum));
        return 0;
}
```

Then, assuming you have your build setup done as shown in a previous article, and `$LLVM_SOURCE_DIR` is set to the root directory of the LLVM source, use the following command to emit LLVM IR from clang that we can then run on our pass:

```bash
$LLVM_SOURCE_DIR/build/bin/clang -emit-llvm test.c -c -o test.ll
```

Now, we can use the `opt` utility to run our pass:

```bash
$LLVM_SOURCE_DIR/build/bin/opt \
    -load $LLVM_SOURCE_DIR/build/lib/LLVMHello2.so
    -enable-new-pm=0 \
    --hello2 \
    < test.ll \
    > /dev/null
```

This should output the names of the different functions, but some of them might have been processed. It is important to make sure not to disable the new pass manager (`-enable-new-pm=0`), because otherwise you won't be able to call your pass.

Now, let's do something a little bit more useful. Change the code within the `runOnFunction` function to the following:

```cpp
for(const auto& block : F)
{
    for(const auto& instruction : block)
    {
        errs() << instruction.getOpcodeName() << ',';
    }
    errs() << '\n';
}
return false;
```

Compile again (`cmake --build .` from the build directory), and then run the program again on the same LLVM IR using the same command as before. Now, this will emit a bunch of different instruction op codes separated by commas with new lines indicating a new block. This takes advantage of the fact that we can iterate through the blocks in a `Function` object and each instruction in a `BasicBlock`. 
