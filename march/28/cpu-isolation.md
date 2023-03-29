# CPU Isolation

When running benchmarks it is important to make sure that the cores being used
for benchmarking are sufficiently isolated to allow for repeatable measurements.
This can be accomplished using the `isolcpus` kernel flag to isolate specific
CPU cores from the scheduler, the `nohz_full` kernel flag to make the kernel
perform most of its work on other cores, and the `nosmt` flag to disable
hyperthreading.

**NOTE:** If you need to disable hyperthreading for the benchmarks that you're
running, make sure to do it at boot time either in the BIOS or by setting the
`nosmt` kernel flag. If it is done at runtime it can impact the CPU core
numbering so the `isolcpus` and `nohz_full` flags might not have their
intended effects.

It can also be useful to set the CPU frequency governor to performance. This
will just keep the CPU at its highest pstate (except for certain circumstances)
which should allow for better benchmarks since it essentially disables clock
frequency scaling.

However, most kernel builds do not have the flags enabled so that you can
set the `nohz_full` flag, and the default CPU governor is most likely not
set to performance (although this can be changed at runtime with userspace
tools).

### Building the kernel

For example, the kernel that ships with Ubuntu 22.04 doesn't contain support
for the `nohz_full` flag, so it helps to build a custom kernel. Here is
how to do it:

1. Download the kernel source (we will be using kernel 5.19.1, but the process
should be similar for other kernel versions):
```bash
wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.19.1.tar.xz
tar -xvf linux-5.19.1.tar.xz
cd ./linux-5.19.1.tar.xz
```
2. Install dependencies necessary for building the kernel:
```bash
sudo apt-get install git fakeroot build-essential ncurses-dev xz-utils libssl-dev bcflex libelf-dev bison
```
3. Copy the config from the currently running kernel. This will allow us to build
a kernel that is the exact same as the one running currently except with the
specific changes that we need. This might not be the most efficient kernel build
for your computer (as it will build many drivers that are not needed for your
specific machine), but if the current kernel boots, copying the config will ensure
that the newly built kernel will most likely boot.
```bash
cp /boot/config-$(uname -r) .config
```
4. Configure the kernel build. This is where you will make changes to the config.
Run the command below and then go through the menus (using the search
functionality as necessary) to set the flags that are needed. In this case we're
interested in setting the CPU frequency governor and enabling the `nohz_full` flag.
Searching by pressing the `/` key should pull up the locations of both. When
building a kernel based on the default Ubuntu config, you will also need to change
some settings regarding the certificates that are used to sign parts of the kernel
under the cryptography header as they will not exist on your system. Without
changing those flags to blank strings the kernel will not build.
```bash
make menuconfig
```
5. Build the kernel.
```bash
make -j $(nproc)
```
6. Install the kernel modules and kernel
```bash
sudo make modules_install
sudo make install
```
7. Strip all of the kernel modules. This step is most likely necessary as the
default build will produce a initrd file of over 500MB. This can potentially
cause out of memory errors at boot time. Performing this step reduces the
initrd to around 70MB.
```bash
cd /var/lib/5.19.1
find . -name *.ko -exec strip --strip-unneeded {} +
```
8. Generate the initrd for the new kernel.
```bash
sudo update-initramfs -c -k 5.19.1
```
9. Update GRUB to detect the changes:
```
sudo update-grub
```
Now if you reboot you should be able to reboot into the new kernel.


### Setting Kernel Flags

In Ubuntu, setting the kernel flags can be done by editing the
`/etc/default/grub` file and modifying the `GRUB_CMDLINE_LINUX_DEFAULT=` line.
For example, to fully isolate the first 12 CPUs on the system, you can add
the following flags after the existing flags on the
`GRUB_CMDLINE_LINUX_DEFAULT` line:
```
GRUB_CMDLINE_LINUX_DEFAULT="<existing flags> isolcpus=0-11 nohz_full=0-11
```
Note that the numbering starts at 0 and the numbering is inclusive on both
ends.