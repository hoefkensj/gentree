import subprocess
import shlex
from pynput import keyboard
from sys import stdout

def supersu(dummy):
	superuser=run('echo', dummy)


def run(cmd, args=''):
	args = f'-S {cmd} {args}'
	su = 'sudo'
	bashline = [su]  + shlex.split(args)
	
	allput = ['stdout:\n']
	process = subprocess.Popen(bashline, stdout=subprocess.PIPE, universal_newlines=True)
	ret = {'RETURN_CODE' : '','STDOUT': ''}
	while True:
		output = process.stdout.readline()
		wrep(output.strip())
		allput.append(output.strip())
		# Do something else
		return_code = process.poll()
		if return_code is not None:
			ret['RETURN_CODE']= return_code
			#wrep(f'RETURN CODE:{return_code}')
			# Process has finished, read rest of the output
			for output in process.stdout.readlines():
				wrep(output.strip())
				allput.append(output.strip())
			break
	ret['STDOUT']= allput
	return ret
	
def ask(Q):
	looped=0
	loop = 1
	
	wnln(Q)
	while True :
		with keyboard.Events() as events:
			# Block for as much as possible
			event=events.get(1e6)
			if event.key == keyboard.KeyCode.from_char('y') or event.key ==  keyboard.Key.enter :
				wrep("YES")
				A=True
				break
			if event.key == keyboard.KeyCode.from_char('n'):
				wrep("NO:")
				A=False
				break
			else:
				wnln("\n")
				wrep(f"no valid key detected use y [default] for YES , n for NO , [enter] for default")
				continue
		break
					
	return A
			
		
			

def umount(file,path,args):
	STAT= run('umount', f'{file}')
	if STAT['RETURN_CODE'] != 0:
		wnln('SOMETHING FUCKED UP! : PROCESS RETURNED CODE:', STAT['RETURN_CODE'])
		wnln('OUTPUT:\n\n')
		wnln(STAT['STDOUT'])
		quit()
	else:
		wrep(f"{path} : UNMOUNTED\t\t\t[V]\n")
		

def mount(file,path,args):
	if ask(f"mount [{file}] on [{path.lower()}] ? [Y]/n") == True:
		wnxt(f'Mounting [{file}] on [{path.lower()}] ... ')
		STAT=run('mount',f'{args} {file} {path.lower()}')
		if STAT['RETURN_CODE'] != 0:
			wnln(f"SOMETHING FUCKED UP! : PROCESS RETURNED CODE:'{STAT['RETURN_CODE']}")
			wnln('OUTPUT:\n\n')
			wnln(STAT['STDOUT'])
			quit()
		else:
			wrep(f"{path} : MOUNTED\t\t\t[V]\n")

def make_rslave(path):
	print(f'making [{path.lower()}] an rslave... ')
	run('mount', f'--make-rslave {path.lower()}')


def wnxt(line):
	stdout.write(f'\t{line}')


def wrep(line):
	stdout.write('\r{txt}'.format(txt=line))


def wnln(line):
	stdout.write('\n{txt}'.format(txt=line))
	
	
def main(cmd, args=''):
	return  run(cmd, args)
	
	
if __name__ == '__main__':
	pass