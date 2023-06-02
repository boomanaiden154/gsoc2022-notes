set -e
#git clone https://github.com/redis/redis.git
cd redis
make CFLAGS="-fbasic-block-sections=labels" CXXFLAGS="-fbasic-block-sections=labels" MALLOC=libc -j $(nproc)
# TODO(boomanaiden154): Add tooling to extract BBs. Note that Redis during its
# build by default does LTO, so bb address maps are only available on the
# executables.
