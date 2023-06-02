set -e
git clone https://git.ffmpeg.org/ffmpeg.git
# TODO(boomanaiden154): add nasm as a dep, probably other codec deps
# too
./configure \
  --extra-cflags="-fbasic-block-sections=labels" \
  --extra-cxxflags="-fbasic-block-sections=labels" \
  --cc="clang" \
  --cxx="clang++"
make -j $(nproc)
# TODO(boomanaiden154): add in BB extraction tooling
