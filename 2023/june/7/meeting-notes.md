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
* What language server/code formatting implementation should be used for the
Gematria project?
* Updates from Owen on getting memory annotations? I'd like to get working on
database construction soon. Could probably just get llvm-exegesis to generate
the annotations, but that will be less efficient.

