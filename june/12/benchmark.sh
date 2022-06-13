for i in {0..30}
do
    /llvm-project/build/bin/llvm-lit -v -j 24 -o results$i.json .
done