# Adding in instruction data to the MLRegAllocAdvisor

Based on [this](https://reviews.llvm.org/D124565) differential, the compiler side now supports adding in additional features that the model doesn't end up using. This means that I should be able to add in instruction data on my compiler fork and still be able to get everything working. The only issue is that instruction data would have a variable size. Need to look a lot more into how the `MLModelRunner` stuff works and then probably work on implementing variable sized data sets.

### Getting the MLModelRunner to work with multiple inputs

Everything in this area should be fine assuming that the inputs are named, which they are. Not using variable inputs at this point due to the fact that libtensorflow doesn't support having a variable number of inputs. The plan at this point is to just have a fixed input size and then truncate/pad as needed.

### Extracting instructions within a live range

There doesn't seem to be any direct utility to grab all the instructions that are present within a live range. There is a utility in `MachineRegisterInfo` that allows for looping through all the definitions and uses of a specific live interval:

```cpp
// Assuming that we're operating in a machine function pass
// and that MF is the machine function being processed
LiveInterval LI;
MachineRegisterInfo MRI = MF.getRegInfo();

for(const auto& MI : MRI.reg_instructions(LI.reg())
{
    // MI is now a machine instruction
    // that either defines or uses the live range LI
}
```


