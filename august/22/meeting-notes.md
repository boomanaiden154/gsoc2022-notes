# Meeting 8/22/22

* Discussion
    * Make sure to check flags on the chromium corpus. Using a relative path, might
    be kind of finnicky.
    * Move the chromium patch into a downstream patch that we can maintain ourselves.
    * Add scripts for integration testing of both the inliner and the regalloc model
    training.
    * Add some documentation on the regalloc model training with a chromium corpus.
    * More testing is needed on my method for extracting instructions, especially
    since it hits an assert.
    * Even if we can only get to about parity with the current model using just
    instruction based features, that model might still be preferable.