import os, sys, re

for path in sys.argv[1:]:
	os.mkdir(os.path.join(path, 'up'))
	os.mkdir(os.path.join(path, 'down'))
	os.mkdir(os.path.join(path, 'left'))
	os.mkdir(os.path.join(path, 'right'))
	
	for name in os.listdir(path):
		if os.path.isfile(os.path.join(path, name)):
			print name
			m = re.search(r'[A-Za-z]+_Anim_[A-Za-z]+_([A-Za-z]+)_(\d+).png', name)
			new_name = m.group(2) + '.png'
			new_dir = m.group(1).lower()
			os.rename(os.path.join(path, name), os.path.join(path, new_dir, new_name))
