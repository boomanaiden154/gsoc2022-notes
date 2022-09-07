# Meeting Notes 9/6/22

* IR PGO error patch should go through soon. Mircea can ping Rong and land
  the patch when it is ready and fully reviewed.
* Jacob Hegna is planning on picking up some of my regalloc work, need to make
  sure that everything is appropriately documented and in a reasonable shape
  for someone else to take over.
  * Need to work on getting the upstream feature patches landed.
* Green light on NFC patch in the register allocator to refactor `SlotIndex::getInstrDistance`,
  Mircea can land after some time/no negative reviews.
* Debugging TFLite issues with embedding layers (or at least how I'm implementing them).
  Depending upon how it is erroring out, might just be some bad implementation on the LLVM
  side.
  * Kind of don't think it is this as it was segfaulting within one of the operations rather
  than upon creating the model.
* Chromium results do sound somewhat promising. A little bit more validation, and then
  if we still are seeing promising results, we can run some performance tests on the
  pinpoint perf bots. Mircea has trybot access for when we get there.