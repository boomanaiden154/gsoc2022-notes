set -e
git clone https://github.com/sqlite/sqlite.git
mkdir ./sqlite/build
cd ./sqlite/build
../configure
make sqlite3.c
clang sqlite3.c -fbasic-block-sections=labels -c -o sqlite3.o
# TODO(boomanaiden154): Add tooling to extract BBs
