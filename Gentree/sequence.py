
import prop
import bash
cGiB = 262144

PW = {''}
PW['ROOT']= 'toor'

CFG={
	'PASSWDQC'	:	'/etc/security/passwdqc.conf',
		}
STOR={
	'DEV'	:	'/nvme0n1',
	'ROOT'	:	'p4',
	'BOOT'	:	'p1',
	'HOME'	:	'p6',
	'FSWAP' :	'/mnt/gentoo/var/.32GiB.bin'
							
					}
LABEL= {
	'ROOT':'GENTOO'
		}



def prepare():
	prop.set(CFG['PASSWDQC'],{'enforce':'none'})
	bash.run('passwd', f'{PW["ROOT"]}')
	bash.run('rc-service', f'sshd start')

	
	# # formatting
	# dd if=/dev/zero of=/dev/{disk}  bs=100M status=progress
	# #
	# parted -a optimal /dev/{disk} mklabel gpt
	# cgdisk /dev/${disk}
	#
	# parted -a optimal /dev/nvme0n1 set 1 boot on
	#
	# mkfs.fat -F 32 -n ESP /dev/{disk}p1
	#
	
def wipe(file=f'/dev/{STOR["DEV"]}'):
	bash.run('dd', f'if=/dev/zero of={file}  bs=100M status=progress')

def fsformat():
	bash.run('mkfs.f2fs', f'-f -l {LABEL["ROOT"]} -O extra_attr,inode_checksum,sb_checksum /dev/{CFG["STOR"]["ROOT"]}')
	#	bash.run('mount' '-o rw,acl,active_logs=6,background_gc=on,user_xattr -t f2fs /dev/disk/by-label/GENTOO /mnt/gentoo')
	
def mount():
	bash.run('sudo', '-S mount -o rw,acl,active_logs=6,background_gc=on,user_xattr -t f2fs /dev/disk/by-label/GENTOO /mnt/gentoo')
	
	#mkfs.btrfs -L USERDATA -n 32k /dev/nvme0n1p4)
	bash.run('mkdir', '/mnt/gentoo/boot')
	bash.run('mkdir', '/mnt/gentoo/var')
	bash.run('mount', '-t vfat /dev/disk/by-label/ESP /mnt/gentoo/boot/')

	#bash.run('dd', f'status=progress if=/dev/zero bs=4096 of=/mnt/gentoo/var/.32GiB.bin bs=4096 count={32 * cGiB}')
	bash.run('chmod','600 /mnt/gentoo/var/.32GiB.swp')
	bash.run('mkswap','/mnt/gentoo/var/.32GiB.swp')
	#cwd here and tar xpvf stage3-*.tar.xz --xattrs-include='*.*' --numeric-owner
	

def main():
	mount()
