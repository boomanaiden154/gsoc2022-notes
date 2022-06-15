for i in {0..30}
do
    testSuites=(
        "harris/harris"
        "SLPVectorization/SLPVectorizationBenchmarks"
        "MemFunctions/MemFunctions"
        "LoopVectorization/LoopVectorizationBenchmarks"
        "LoopInterchange/LoopInterchange"
        "LCALS/SubsetALambdaLoops/lcalsALambda"
        "LCALS/SubsetARawLoops/lcalsARaw"
        "LCALS/SubsetBLambdaLoops/lcalsBLambda"
        "LCALS/SubsetBRawLoops/lcalsBRaw"
        "LCALS/SubsetCLambdaLoops/lcalsCLambda"
        "LCALS/SubsetCRawLoops/lcalsCRaw"
        "ImageProcessing/AnisotropicDiffusion/AnisotropicDiffusion"
        "ImageProcessing/BilateralFiltering/BilateralFiltering"
        "ImageProcessing/Blur/Blur"
        "ImageProcessing/Dilate/Dilate"
        "ImageProcessing/Dither/Dither"
        "ImageProcessing/Interpolation/Interpolation"
        "Builtins/Int128/Builtins"
    )

    for testSuite in ${testSuites[@]}; do
        baseName=$(basename $testSuite)
        outFile="/llvm-test-suite/build/$baseName.json"
        /llvm-test-suite/build/MicroBenchmarks/$testSuite --benchmark_perf_counters=INSTRUCTIONS,MEM_UOPS_RETIRED:ALL_LOADS,MEM_UOPS_RETIRED:ALL_STORES --benchmark_out_format=json --benchmark_out=$outFile
    done

    python3 combine-benchmarks.py output.tmp
    mv output.tmp output$i.json

    rm -rf /llvm-test-suite/build/*.json
done