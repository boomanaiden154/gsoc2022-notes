set -e
git clone https://git.savannah.gnu.org/git/gzip.git
# TODO(boomanaiden154): Figure out dependencies, gzip needs
# gettext, texinfo, autopoint
cd gzip
./bootstrap
./configure CC=clang CXX=clang++
make CFLAGS="-fbasic-block-sections=labels" CXXFLAGS="-fbasic-block-sections=labels"
# TODO(boomanaiden154): Get BB extraction tooling working.

