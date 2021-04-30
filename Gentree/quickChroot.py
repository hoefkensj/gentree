
#!/usr/bin/python
from bash import mount,make_rslave,ask,supersu,umount
from configparser import ConfigParser, ExtendedInterpolation
from pynput import keyboard
import cfg



def get_cfg(env_chroot):
	return cfg.todct(cfg.read(f'chroot_{env_chroot.upper()}.ini', ConfigParser(interpolation=ExtendedInterpolation(), delimiters=':')))

dct_chrt = get_cfg('gentoo')  # returns a multilevel dict constructed from iniu file [(key) : (val][key) : (val)]
MNT_FS = dct_chrt['MNT_FS']
STORL = dct_chrt['STORL']
STORF = dct_chrt['STORF']
MNT = dct_chrt['MNT']

def main():
	dct_chrt	= get_cfg('gentoo') 							#returns a multilevel dict constructed from iniu file [(key) : (val][key) : (val)]
	MNT_FS		= dct_chrt['MNT_FS']
	STORL 		= dct_chrt['STORL']
	STORF 		= dct_chrt['STORF']
	MNT 		= dct_chrt['MNT']




	
	#mount(STORL['boot'],MNT['boot'],MNT_FS['vfat'])          	# mount('/dev/disk/by-label/ESP','/mnt/gentoo/boot/', MNT_FS['vfat'])
	#mount(STORF['proc'],MNT['proc'],MNT_FS['proc'])          	# mount('/proc','/mnt/gentoo/proc', MNT_FS['proc'])
	mount(STORF['sys'],MNT['sys'],MNT_FS['sys'])             	# mount('/sys','/mnt/gentoo/sys',MNT_FS['sys'])
	mount(STORF['dev'],MNT['dev'],MNT_FS['dev'])             	# mount('/dev','/mnt/gentoo/dev',MNT_FS['dev'])
	make_rslave(MNT['sys'])										# slave('/mnt/gentoo/sys')
	make_rslave(MNT['dev'])										# slave('/mnt/gentoo/dev')
	


if __name__ == '__main__':
	ROOT= STORL['root'], MNT['root'].lower(), MNT_FS['f2fs']
	supersu('QUICK CHROOT')
	def umount_all():
		umount(*ROOT)
	
	try : umount_all()
	except: pass
	
	#mount(STORL['root'],MNT['root'].lower(),MNT_FS['f2fs'])
	main()
	





# bash.run('cp'   , '--dereference /etc/resolv.conf /mnt/gentoo/etc/')
# bash.run('test' , '-L /dev/shm ')
# bash.run('rm'   , '/dev/shm')
# bash.run('mkdir', '/dev/shm')
# mount('shm','/dev/shm',MNT_FS['shm'])
# bash.run('chmod', '1777 /dev/shm')
#
#
# print('Press s or n to continue:')
#
# with keyboard.Events() as events:
# 	# Block for as much as possible
# 	event = events.get(1e6)
# 	if event.key == keyboard.KeyCode.from_char('s'):
# 		print("YES")
#
#
#
#
#
		


	
	
#bash.run('chroot','/mnt/gentoo /bin/bash')
#bash.run('source','/etc/profile')
#bash.run('export', 'PS1="(chroot) ${PS1}"')



#bash.run('mount', '-o rw,acl,active_logs=6,background_gc=on,user_xattr -t f2fs /dev/disk/by-label/GENTOO /mnt/gentoo')
#bash.run('mount', '-t vfat /dev/disk/by-label/ESP /mnt/gentoo/boot/')
#bash.run('mount', '--types proc /proc /mnt/gentoo/proc')
#bash.run('mount', '--rbind /sys /mnt/gentoo/sys')
#bash.run('mount', '--make-rslave /mnt/gentoo/sys')
#bash.run('mount', '--rbind /dev /mnt/gentoo/dev')
#bash.run('mount', '--make-rslave /mnt/gentoo/dev')
#bash.run('mount', '-t tmpfs -o nosuid,nodev,noexec shm /dev/shm')



# livecd /mnt/gentoo # mount -t proc /proc /mnt/gentoo/proc
# livecd /mnt/gentoo # mount --rbind /sys /mnt/gentoo/sys
# livecd /mnt/gentoo # mount --make-rslave /mnt/gentoo/sys
# livecd /mnt/gentoo # mount --rbind /dev /mnt/gentoo/dev
# livecd /mnt/gentoo # mount --make-rslave /mnt/gentoo/dev
# livecd /mnt/gentoo # test -L /dev/shm && rm /dev/shm && mkdir /dev/shm
# livecd /mnt/gentoo # mount -t tmpfs -o nosuid,nodev,noexec shm /dev/shm
# livecd /mnt/gentoo # chmod 1777 /dev/shm
