# Meeting 6/1/2022

### Topics

- Original plan to use PDG as NN input
  
  - PDGs not currently implemented in LLVM/Analysis
  
  - Looks like there was intention to add it in [here](https://reviews.llvm.org/D65350), but only DDGs were ever implemented.
  
  - Two options: switch to using DDGs, implement PDG
    
    - A lot of the work for implementing PDGs is already there as there is a generic `AbstractDependenceGraphBuilder` class. Plenty of example implementation with the existing DDG stuff as well.
    
    - Still probably a decent amount of work. More evaluation needed?

- IR embeddings
  
  - Using one hot encoding is pretty impractical due to the large number of possible instructions.
  
  - Lots of prior art on assembly vectorization
    
    - Examples:
      
      - [Palm Tree](https://arxiv.org/abs/2103.03809)
      
      - [Asm2Vec](https://ieeexplore.ieee.org/document/8835340)
      
      - [InnerEye](https://arxiv.org/abs/1808.04706)
    
    - Some adaptation necessary, Assembly -> LLVM IR, don't need to encode a lot of the things that these implementations encode (eg registers, instruction flags)
    
    - Current work: Generated a corpus of instructions from Clang/LLVM
    
    - Future work (over the next couple days): Corpus -> Skip-gram pairs, training in classic word2vec sense (maybe additional compute power?), evaluation of the resulting data (dimensionality reduction + clustering)
    
    - Export a table of values that can then be used for instruction encoding when feeding everything to the model.

- Modifying `MlRegAllocAdvisor.cpp` to use graph based data
  
  - Started tracing code/attached a debugger to step through it. Becoming much more familiar with the code base.
  
  - Probably going to start hacking on it this week, working in stages:
    
    - Tearing out existing features, getting DDG/PDG construction working.
    
    - Still need to read up more on the tensorflow c library and how exactly I need to encode the data to pass it to the model. Getting encoding working.
    
    - Start to get everything integrated in with `ml-compiler-opt`

- NN structure
  
  - Been reading about some current architectures
  
  - Preliminary plan (still a long ways off from implementation):
    
    - Input
    
    - GCL (Graph convolutional layer)
    
    - Pooling layer (minCUT/spectral clustering?)
    
    - GCL
    
    - Final pooling layer
    
    - Couple fully connected feed forward layers to final output
  
  - Very big compared to current model (as mention in the proposal)(I'm assuming the current model is similar to the ML inliner? Couple fully connected feed forward layers of tens of nodes)?
    
    - Work on optimization way later, but something to give some thought to
  
  - GNN library
    
    - [Spektral](https://graphneural.network/) - looks like the ideal choice. Mature, seems to have all the necessary layer types/input encodings.
    
    - [Tensorflow GNN](https://github.com/tensorflow/gnn) - Doesn't seem mature enough to be used in production

### After meeting

- Scaling back on the size of the initial model. Instead of going straight for GNNs, the focus early on will be feeding an embedding of the instructions directly to something similar to the existing model.
  
  - Starting small, slowly branching out into larger models, evaluating performance at each stage.
  
  - Anecdote on non-graph aware model outperforming a graph aware model.

- Future directions
  
  - Work on building clang/LLVM with current head of tree clang/LLVM. **Due:** Hopefully have everything done on Friday.
  
  - Hack on the compiler to get necessary features exposed (instruction opcodes in this case). **Due:** Hopefully have this done before the meeting next Monday.
  
  - Work on an initial model **Due:** TBD
  
  - 


