# Meeting Mircea/Ondrej/Viraj/Aiden

Agenda:
* Finalize name decision for new LLVM cost modelling tool. Current finalists
in decisions are either `llvm-gematria` or `llvm-cm`.
* Post an RFC to get some feedback and finalize other implementation details?
* We need a rough sketch of the design
  * Disassembly infrastructure (maybe piggybacking on something else within LLVM,
  llvm-objdump?), moving some stuff to support libraries, using existing
  `SHT_LLVM_BB_ADDR_MAP` section support.
  * Integration of "strategies" such as uica/GRANITE, selection through a CLI flag?
  * Focusing on whole program cost modelling/binary input seems to be a clear
  differentiator from llvm-mca.
  * Response to the criticism of "why should this be in LLVM?"?
* Python formatting for Gematria codebase?
* Is there a tool that already exists for merging .tfrecord files or does one
need to be written? If one needs to be written, I can work on that.
* Updates from Owen on getting memory annotations? I'd like to get working on
database construction soon. Could probably just get llvm-exegesis to generate
the annotations, but that will be less efficient.

Meeting Notes
* Perf data produces JSON in a pretty tractable format
* Testing infrastructure after we have actual inputs of where cache misses occur
in an app might need to be improved. Two options:
  * Latent learning
  * Augmented test harnesses
* Seem to have settled on latent learning, looking at doing a couple different
microbenchmarks and seeing where we go from there, probably doing some cheap
linear regression or something at first for evaluation (Viraj is working on
this).
* Ondrej can bump Clement on llvm-exegesis reviews
* No updates so far from Owen, Ondrej is meeting up with him again soon.

