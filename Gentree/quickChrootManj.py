import bash

bash.run('mount', '-o rw,acl,active_logs=6,background_gc=on,user_xattr -t f2fs /dev/nvme0n1p5 /mnt/MANJARO')
bash.run('mount', '-t vfat /dev/disk/by-label/ESP /mnt/MANJARO/boot/')
bash.run('cp'   , '--dereference /etc/resolv.conf /mnt/MANJARO/etc/')
bash.run('mount', '--types proc /proc /mnt/MANJARO/proc')
bash.run('mount', '--rbind /sys /mnt/MANJARO/sys')
bash.run('mount', '--make-rslave /mnt/MANJARO/sys')
bash.run('mount', '--rbind /dev /mnt/MANJARO/dev')
bash.run('mount', '--make-rslave /mnt/MANJARO/dev')
bash.run('test' , '-L /dev/shm ')
bash.run('rm'   , '/dev/shm')
bash.run('mkdir', '/dev/shm')
bash.run('mount', '-t tmpfs -o nosuid,nodev,noexec shm /dev/shm')
bash.run('chmod', '1777 /dev/shm')



# livecd /mnt/gentoo # mount -t proc /proc /mnt/gentoo/proc
# livecd /mnt/gentoo # mount --rbind /sys /mnt/gentoo/sys
# livecd /mnt/gentoo # mount --make-rslave /mnt/gentoo/sys
# livecd /mnt/gentoo # mount --rbind /dev /mnt/gentoo/dev
# livecd /mnt/gentoo # mount --make-rslave /mnt/gentoo/dev
# livecd /mnt/gentoo # test -L /dev/shm && rm /dev/shm && mkdir /dev/shm
# livecd /mnt/gentoo # mount -t tmpfs -o nosuid,nodev,noexec shm /dev/shm
# livecd /mnt/gentoo # chmod 1777 /dev/shm
