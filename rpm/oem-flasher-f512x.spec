Name:       oem-flasher-f512x
Summary:    helper for flashing oem
Version:    0.0.0
Provides:   oem-flasher-f512x
Release:    1
URL:        https://github.com/mer-hybris/oem-flasher-f512x
Group:      System Environment/Kernel
Source0:    %{name}-%{version}.tar.bz2
License:    MIT

BuildRequires: droid-glibc-tools
BuildRequires: dtc

%define lk_target msm8952

%define kernel_base 0x20000000
%define kernel_offset 0x00080000
%define ramdisk_offset 0x02000000
%define tags_offset 0x01E00000

%define pagesize 2048

%description
A small helper to flash the oem partition on an unlocked (Open Devices) Sony Xperia X.

%prep
%setup -q

%build
# No toolchain prefix, the default sb2 compilers can handle this.
OEM_FLASHER=1 OEM_FLASHER_F5121=1 TOOLCHAIN_PREFIX= make %{?_smp_flags} %{lk_target}

# Compile our own minimal dtb.
dtc -I dts -O dtb dtbs/%{lk_target}.dtsi -o dtb

# Package it into a compatible format.
gzip -n -9c build-%{lk_target}/lk.bin > lk.gz
cat lk.gz dtb > lk.gz.dtb
echo "This is a stub. This mode ignores the ramdisk." > no-ramdisk.txt
mkbootimg --base %{kernel_base} --pagesize %{pagesize} --kernel_offset %{kernel_offset} --ramdisk_offset %{ramdisk_offset} --tags_offset %{tags_offset} --cmdline '' --kernel lk.gz.dtb --ramdisk no-ramdisk.txt -o fastboot.img

%install
mkdir -p $RPM_BUILD_ROOT/boot
cp fastboot.img $RPM_BUILD_ROOT/boot

%files
%defattr(-,root,root-)
/boot/fastboot.img

