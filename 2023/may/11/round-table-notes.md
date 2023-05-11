# Infrastructure Round Table Notes

* Local reproducibility with Github actions is better than what we currently have
with Buildbot.
* Konrad Kleine proposes/demoes some custom tooling that he has written to integrate
Buildbot into Github PRs for opt-in pre-merge testing.
* Pre-merge checks will most likely have to run on a cloud service provider
because they need to be scalable in addition to being fast if we want to have mandatory
pre-merge checks. Optional pre-merge testing wouldn't necessarily require this.
  * Object file storage can get expensive in the cloud if using something like
  ccache due to network/storage costs. Probably on the order of hundreds of dollars
  a day.
* Two different problems that we're setting out to solve. Mandatory pre-merge
testing in addition to opt-in pre-merge testing. They have different constraints.
* More information on what bots people care about might be useful.
  * Should be possible to gather most of this data from the current Buildbot
  setup.
* Huge number of bots that run a lot of the same configurations/testing and there
are also lots of gaps within these configurations/testing.
  * Examples of ABI compatibility and multi-stage builds for determinism testing.
  * Determinism issues can be a particular pain point.
* There's not really a clear plan for cohesive infrastructure for the project.
* Fast bots don't currently run every configuration.

