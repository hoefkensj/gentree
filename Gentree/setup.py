#some short hands for system/user specific choises and specs
import configparser
import threading
import subprocess
import sys
import shlex
from time import sleep
from multiprocessing import Process
import prop
import setup_config


#USER VARS CHANGE THESE ACCORDINGLY

#DEFAULT SYSTEM VARS FOR GENTOO LIVE ISO
#CFG_PASSWDQC='/etc/security/passwdqc.conf'
CFG={'PASSWDQC':'test.conf'}
MAKE='/dev/portage/make.conf'

def cli_out(data):
	sys.stdout.write('r{txt}'.format(txt = data))

def cli_in(var):
	userinput = input("Q for quit :")
	
	
def bash(cmd,args=''):
	bashline= [cmd] + shlex.split(args)
	

	process = subprocess.Popen(bashline, stdout=subprocess.PIPE, universal_newlines=True)

	while True:
		output = process.stdout.readline()
		print(output.strip())
		# Do something else
		return_code = process.poll()
		if return_code is not None:
			print('RETURN CODE', return_code)
			# Process has finished, read rest of the output
			for output in process.stdout.readlines():
				print(output.strip())
			break
		return return_code
#print('done')
#subprocess.run(cmd,shlex.split(args))
#print(shlex.split("gimp --no-interface -b '(python-fu-scale RUN-NONINTERACTIVE 0 0 \"img.jpg\")' -b '(gimp-quit 0)'"))

def main():
	prop.set(CFG['PASSWDQC'],{'enforce':'none'})
	bash('rc-service','sshd start')
	bash('ifconfig')
# formatting
bash('dd', f'if=/dev/zero of=/dev/{disk}  bs=100M status=progress')

	


















#


	
	
	





#with open(CFG_PASSWDQC, rW) as script:
#	stmts=script.readlines()

#for stmt in stmts:
#	print(f'{stmt}')

if __name__ == '__main__':
	main()
 
