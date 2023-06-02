# BB Datasets

This article is aimed to provide an overview on what applications are included
in current BB datasets (particularly BHive/Ithemal).

### BHIVE

| Application | Number of Basic Blocks |
| ----------- | ---------------------- |
| OpenBlas | 19032 |
| Redis | 9343 |
| SQLite | 8871 |
| GZip | 2272 |
| Tensorflow | 71988 |
| Clang/LLVM | 212758 |
| Eigen | 4545 |
| Embree | 12602 |
| FFmpeg | 17150 |

### Ithemal

| Application | Number of Basic Blocks |
| ----------- | ---------------------- |
| Linux shared libraries | 313846 |
| SPEC2006 | 247047 |
| SPEC2017 | 234588 |
| NAS | 3935 |
| polybench-3.1 | 1900 |
| TSVC | 5129 |
| cortexsuite | 6582 |
| simd | 212544 |
| Clang/Python 2.7/Python 3.5 | 2746275 |
| GIMP/Firefox/Open-office/Rhythmbox | 83555 |

### Total vs Unique Counts

I'm reasonably confident the number of basic blocks reported for BHive are the
numbers of unqiue basic blocks contributed per application. For Ithemal I've
reported the total number of basic blocks. There will always be significantly
less unique basic blocks than the total number of basic blocks. For the ithemal
dataset, only about 25% of the basic blocks are unique.

### Other Notes

It's also important to note that the Ithemal and BHive datasets were collected
using runtime instrumentation with DynamoRIO. These counts might seem suspicously
low (especially for something like Firefox), but it's important to note that
this is most likely because most of the code paths were simply not touched
so the runtime instrumentation never picked up those blocks. New static tools
for extracting basic blocks should help with this.

