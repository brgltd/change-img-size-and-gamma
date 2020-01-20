import os
import cv2
import numpy as np 

from PIL import Image

def check_flag(msg):
	flag = input(f"Do you want to {msg} (y/n): ")
	while flag != 'y' and flag != 'n':
		flag = input("Has to be 'y' ou 'n': ")
	return flag

def get_imgpaths(original_imgs=True):
	""" Get the image paths on the "imgs/" dir. This way, the program
	can work with multiple images.
	"""
	imgsdir = os.path.join(os.getcwd(), "imgs")
	if original_imgs:
		return [os.path.join(imgsdir, imgname)
				for imgname in os.listdir(imgsdir)
				if not imgname.__contains__("-gamma")
				and not imgname.__contains__("-resized")]
	else:
		return [os.path.join(imgsdir, imgname)
				for imgname in os.listdir(imgsdir)
				if imgname.__contains__("-gamma")
				and not imgname.__contains__("-resized")]

def adjust_gamma():
	flag_gamma = check_flag("change the gamma level of your image")
	if flag_gamma == 'y':
		gamma = int(input("Type the desired gamma level: "))
		imgpaths = get_imgpaths()
		for imgpath in imgpaths:
			img = cv2.imread(imgpath)
			inv_gamma = 1 / gamma 
			table = np.array([((i / 255) ** inv_gamma) * 255
							 for i in np.arange(0, 256)]).astype('uint8')
			new_img = cv2.LUT(img, table)
			new_imgpath = imgpath.replace('.', f"-gamma({gamma}).")
			cv2.imwrite(filename=new_imgpath, img=new_img)
	return flag_gamma

def convert_imgsize(flag_gamma):
	flag_size = check_flag("change the image size")
	if flag_size == 'y':
		width = int(input("Type the desired image width: "))
		height = int(input("Type the desired image height: "))
		imgpaths = get_imgpaths(False) if flag_gamma == 'y' else get_imgpaths(True)
		for imgpath in imgpaths:
			img = Image.open(imgpath) # usefull methods: img.size, img.format, img.mode
			new_img = img.resize((width, height), Image.HAMMING)
			new_imgpath = imgpath.replace('.', f"-resized({width}x{height}).")
			new_img.save(new_imgpath)
			if flag_gamma == 'y':
				os.unlink(imgpath)
	return flag_size

def main():
	flag_gamma = adjust_gamma()
	flag_size = convert_imgsize(flag_gamma)

if __name__ == "__main__":
	main()
