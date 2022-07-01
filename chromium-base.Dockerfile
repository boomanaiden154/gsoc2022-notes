FROM ubuntu:20.04 AS perf-builder
RUN apt-get update
RUN apt-get install -y flex bison make git
RUN git clone --depth 1 https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
WORKDIR /linux/tools/perf
RUN make

FROM llvm-base
COPY --from=perf-builder /linux/tools/perf/perf /usr/bin/perf
RUN apt-get install -y sudo
RUN git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
RUN mkdir /chromium
WORKDIR /chromium
RUN PATH="$PATH:/depot_tools" fetch --nohooks --no-history chromium
WORKDIR /chromium/src
RUN PATH="$PATH:/depot_tools" gclient runhooks
RUN apt-get install -y binutils \
    bison \
    bzip2 \
    cdbs \
    curl \
    dbus-x11 \
    dpkg-dev \
    elfutils \
    devscripts \
    fakeroot \
    flex \
    git-core \
    gperf \
    libasound2-dev \
    libatspi2.0-dev \
    libbrlapi-dev \
    libbz2-dev \
    libcairo2-dev \
    libcap-dev \
    libc6-dev \
    libcups2-dev \
    libcurl4-gnutls-dev \
    libdrm-dev \
    libelf-dev \
    libevdev-dev \
    libffi-dev \
    libgbm-dev \
    libglib2.0-dev \
    libglu1-mesa-dev \
    libgtk-3-dev \
    libkrb5-dev \
    libnspr4-dev \
    libnss3-dev \
    libpam0g-dev \
    libpci-dev \
    libpulse-dev \
    libsctp-dev \
    libspeechd-dev \
    libsqlite3-dev \
    libssl-dev \
    libudev-dev \
    libva-dev \
    libwww-perl \
    libxshmfence-dev \
    libxslt1-dev \
    libxss-dev \
    libxt-dev \
    libxtst-dev \
    locales \
    openbox \
    p7zip \
    patch \
    perl \
    pkg-config \
    rpm \
    ruby \
    subversion \
    uuid-dev \
    wdiff \
    x11-utils \
    xcompmgr \
    xz-utils \
    zip \
    libc6-i386 \
    lib32stdc++6 \
    lib32gcc-s1 \
    libasound2 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libc6 \
    libcairo2 \
    libcap2 \
    libcups2 \
    libdrm2 \
    libevdev2 \
    libexpat1 \
    libfontconfig1 \
    libfreetype6 \
    libgbm1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libpam0g \
    libpango-1.0-0 \
    libpci3 \
    libpcre3 \
    libpixman-1-0 \
    libspeechd2 \
    libstdc++6 \
    libsqlite3-0 \
    libuuid1 \
    libwayland-egl1-mesa \
    libx11-6 \
    libx11-xcb1 \
    libxau6 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxdmcp6 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxinerama1 \
    libxrandr2 \
    libxrender1 \
    libxtst6 \
    zlib1g \
    libffi7
