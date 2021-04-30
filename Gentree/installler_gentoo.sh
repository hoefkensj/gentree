
#nano /etc/security/passwdqc.conf #--->set enforce=none
passwd toor
rc-service sshd start
ifconfig
#screen -t prep

# formatting
dd if=/dev/zero of=/dev/{disk}  bs=100M status=progress
#
parted -a optimal /dev/{disk} mklabel gpt
cgdisk /dev/${disk}

parted -a optimal /dev/nvme0n1 set 1 boot on

mkfs.fat -F 32 -n ESP /dev/{disk}p1
mkfs.f2fs -f -l GENTOO -O extra_attr,inode_checksum,sb_checksum /dev/${disk}p2
mkfs.btrfs -L USERDATA -n 32k /dev/nvme0n1p4

mount -o rw,acl,active_logs=6,background_gc=on,user_xattr  -t f2fs /dev/disk/by-label/GENTOO /mnt/gentoo

mkdir /mnt/gentoo/boot
mkdir /mnt/gentoo/var

mount -t vfat /dev/disk/by-label/ESP /mnt/gentoo/boot/
dd status=progress if=/dev/zero bs=4096 of=/mnt/gentoo/var/.8GiB.bin bs=4096 count=2097152
chmod 600 /mnt/gentoo/var/.8GiB.bin
mkswap /mnt/gentoo/var/.8GiB.bin
swapon /mnt/gentoo/var/.8GiB.bin

cd /mnt/gentoo
wget -c http://ftp.belnet.be/mirror/rsync.gentoo.org/gentoo/releases/amd64/autobuilds/current-stage3-amd64-systemd/stage3-amd64-systemd-20210214T214503Z.tar.xz
tar xpvf stage3-*.tar.xz --xattrs-include='*.*' --numeric-owner

#
#make backup of etc folder to /backup/etc
mkdir /mnt/gentoo/mnt/backup/
cp -R /mnt/gentoo/etc/ /mnt/gentoo/mnt/backup/

#hier goes CFLAGS AND CXXFLAGS
## Compiler flags to set for all languages
#COMMON_FLAGS="-march=native -O2 -pipe"
## Use the same settings for both variables
#CFLAGS="${COMMON_FLAGS}"
#CXXFLAGS="${COMMON_FLAGS}"
nano -w /mnt/gentoo/etc/portage/make.conf



mkdir --parents /mnt/gentoo/etc/portage/repos.conf
cp /mnt/gentoo/usr/share/portage/config/repos.conf /mnt/gentoo/etc/portage/repos.conf/gentoo.conf
cp --dereference /etc/resolv.conf /mnt/gentoo/etc/
mount --types proc /proc /mnt/gentoo/proc
mount --rbind /sys /mnt/gentoo/sys
mount --make-rslave /mnt/gentoo/sys
mount --rbind /dev /mnt/gentoo/dev
mount --make-rslave /mnt/gentoo/dev
chroot /mnt/gentoo /bin/bash

####################################################
source /etc/profile
export PS1="(chroot) ${PS1}"
emerge-webrsync
#emerge --sync
eselect profile list
eselect profile set 9
emerge --oneshot sys-apps/portage
echo 'Europe/Brussels > /etc/timezone'
emerge --config sys-libs/timezone-data
echo 'en_US ISO-8859-1 >> /etc/locale.gen'
echo 'en_US.UTF-8 UTF-8 >> /etc/locale.gen'
echo 'nl_BE ISO-8859-1 >> /etc/locale.gen'
echo 'nl_BE.UTF-8 UTF-8 >> /etc/locale.gen'



locale-gen
eselect locale list
eselect locale set 10

env-update && source /etc/profile && export PS1="(chroot) $PS1"

mkdir -p /etc/portage/package.{accept_keywords,license,mask,unmask,use}
###########################################################

echo 'ACCEPT_LICENSE="*" >> ${MAKE}'
echo 'ACCEPT_KEYWORDS="amd64 ~amd64" >> ${MAKE}'
echo 'CHOST="x86_64-pc-linux-gnu" >> ${MAKE}'
echo 'GENTOO_MIRRORS="${GENTOO_MIRRORS} http://ftp.belnet.be/pub/rsync.gentoo.org/gentoo/ https://ftp.belnet.be/pub/rsync.gentoo.org/gentoo/ ftp://ftp.belnet.be/pub/rsync.gentoo.org/gentoo/ rsync://ftp.belnet.be/gentoo/gentoo/" >> ${MAKE}'
echo 'GENTOO_MIRRORS="${GENTOO_MIRRORS} http://gentoo.mirror.root.lu/ https://gentoo.mirror.root.lu/ ftp://mirror.root.lu/gentoo/" >> ${MAKE}'
echo 'GENTOO_MIRRORS="${GENTOO_MIRRORS} http://ftp.snt.utwente.nl/pub/os/linux/gentoo https://ftp.snt.utwente.nl/pub/os/linux/gentoo ftp://ftp.snt.utwente.nl/pub/os/linux/gentoo rsync://ftp.snt.utwente.nl/gentoo/" >> ${MAKE}'
echo 'GENTOO_MIRRORS="${GENTOO_MIRRORS} http://mirror.leaseweb.com/gentoo/ https://mirror.leaseweb.com/gentoo/ ftp://mirror.leaseweb.com/gentoo/ rsync://mirror.leaseweb.com/gentoo/" >> ${MAKE}'
echo 'PORTAGE_BINHOST="http://packages.gentooexperimental.org/packages/amd64-stable/"  >> ${MAKE}'

echo 'CCACHE_DIR="/var/cache/ccache" >> ${MAKE}'
echo 'CCACHE_SIZE="32G" >> ${MAKE}'
echo 'DISTCC_DIR="/var/tmp/portage/.distcc" >> ${MAKE}'

echo 'FEATURES=""'
echo 'MAKEOPTS="" '
echo 'EMERGE_DEFAULT_OPTS=""'
echo 'L10N="en"'
echo 'CPU_FLAGS_X86="aes avx avx2 fma3 mmx mmxext popcnt sse sse2 sse3 sse4_1 sse4_2 ssse3 f16c pclmul"'
echo 'CONFIG_PROTECT="protect-owned"'





echo 'ALSA_CARDS="emu10k1 emu10k1x hdsp hdspm ice1712 mixart rme32 rme96 sb16 sbawe sscape usb-usx2y vx222"'
echo 'VIDEO_CARDS="nvidia intel i965 i915 v4l"'
echo 'INPUT_DEVICES="evdev libinput"'
echo 'INPUT_DRIVERS="evdev"'

echo 'COMMON_FLAGS="" >>  ${MAKE}'
echo 'RUBY_TARGETS="ruby30"'
echo 'PYTHON_TARGETS="python3_9 python3_8 python3_7 pypy3"'
echo 'GRUB_PLATFORMS="efi-64"'

gcc -march=skylake -E -v - </dev/null 2>&1 | sed -n 's/.* -v - //p' |tee /root/etc/portage/make.conf/CFLAGS
emerge flaggie dev-vcs/git app-eselect/eselect-repository esearch gentoolkit
flaggie +64bit +bindist +wayland +wifi +static-libs +samba +quicktime +pulseaudio +offensive +networkmanager +modules +lz4 +lzo +lzma
flaggie +libressl +gles2 +jack +vulkan +handbook +git +custom-cflags +glxnvidia +nvidia +f2fs +btrfs +cuda +drm +d3d9 +nvcontrol
flaggie +nvenc +kms +ntfs +screen +shaders +evdfev +packagekit +pci +p2p +overlays +realtime +kwin
flaggie dev-db/sqlite-3.34.0 -icu
flaggie dev-lang/python-3.9.2 -bluetooth

mkdir -p /etc/portage/repos.conf
mkdir -p /etc/portage/package.use
eselect repository enable wayland-desktop
emaint sync --repo wayland-desktop
emerge --backtrack=250 -avD --update  --newuse @world
echo '"sys-firmware/intel-microcode initramfs" > /etc/portage/package.use/intel-microcode'

emerge sys-kernel/gentoo-sources sys-kernel/linux-firmware  sys-kernel/genkernel sys-firmware/intel-microcode
emerge pci-utils

nano /etc/portage/make.conf

cd /usr/src/linux/
make menuconfig
make && make_modules
make install
genkernel --install --kernel-config=/usr/src/linux/.config initramfs
emerge sys-boot/grub eys-boot/refind
grub-install --target=x86_64-efi --efi-directory=/boot
cp /etc/default/grub /etc/backup/grub
emerge --ask sys-kernel/linux-firmware
emerge nvidia-firmware
emerge nvidia-drivers
emerge nvidia-video-codec
emerge egl-wayland wayland pico-wayfire qtgreet
emerge --ask @module-rebuild
grub-install --target=x86_64-efi --efi-directory=/boot
mkdir -p /etc/backup/default/
cp /etc/default/grub /etc/backup/default/grub
nano /etc/default/grub
	GRUB_CMDLINE_LINUX="init=/lib/systemd/systemd root=UUID= nvidia.modprobe=1 net.rename=0 quiet splash"
grub-mkconfig -o /boot/grub/grub.cfg
nano /etc/security/passwdqc.conf
passwd
etc-update
refind-install

USE=""
flaggie +{}

"""