import configparser
NOTFOUND = 404


def r(f_props,cfg=configparser.ConfigParser()):
	def add_header(props_file):
		yield '[{}]\n'.format('#')
		for line in props_file:
			yield line
	
	with open(f_props) as file:
		file = file.readlines()
	cfg.read_file(add_header(file), source=f_props)
	return cfg['#']
	
def w(f_props, props, cfg=configparser.ConfigParser()):
	cfg['#'] = props
	with open(f_props, 'w') as configfile:
		cfg.write(configfile)
	with open(f_props, 'r') as fin:
		data = fin.read().splitlines(True)
		for idx, line in enumerate(data):
			data[idx] = f'{"".join(line.split())}\n'
		data[0] = '\n'
	with open(f_props, 'w') as fout:
		fout.writelines(data)

def st(file, dct):
	props = r(file)
	props[list(dct.keys())[0]] = dct[list(dct.keys())[0]]
	w(file, props)
	
	
def gt(file,prop, ):
	props = r(file)
	try:
		dct_ret = {prop : props[prop]}
	except:
		return NOTFOUND
	return dct_ret

	
def main():
	pass

if __name__ == '__main__':
	main()

 