# Importing required packages
from PIL import Image, ImageOps, ImageFilter
import numpy as np
import glob
import time
import os
import random
import yaml
import argparse

# Importing other python files
from normalisingFunctions import *

# Running code
if __name__ == '__main__':

	# Creating directories for processed images
	os.mkdir(os.getcwd()+'/data/train_set/normalised/')
	os.mkdir(os.getcwd()+'/data/test_set/normalised/')

	# Setting up argparse
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('configFile')
	args = parser.parse_args()

	# Opening relevant config file
	with open(args.configFile, 'r') as config:
		cfg = yaml.safe_load(config)

	# If output is in grayscale
	if not cfg['submasks']['rgbOutput']:

		# Opening up first image to create relevant arrays
		var = glob.glob('./data/train_set/'+"*."+cfg['submasks']['ext'])[0]
		image = Image.open(var)
		padding = len(var[len('./data/train_set/'):].split('.')[-2])

		# Converting to grayscale
		image = ImageOps.grayscale(image)

		# Converting to array
		array = np.asarray(image)

		# Creating random noise arrays
		print("Started noise array creation.")

		# Storing arrays
		sNRays = []
		sineRays = []
		gradRays = []
		gridRays = []

		# Creating a nuber of noise masks
		for i in range(cfg['submasks']['maskChoices']):

			# Creating smartnoise mask
			noiseCfg = cfg['submasks']['smartNoise']
			if noiseCfg['use']:
				sNRays.append(smartNoise(array, random.uniform(noiseCfg['params']['min'], noiseCfg['params']['max'])))

			# Creating sinenoise mask
			noiseCfg = cfg['submasks']['sineNoise']
			if noiseCfg['use']:
				sineRays.append(sinusoid(array, random.uniform(noiseCfg['params']['min'], noiseCfg['params']['max'])))

			# Creating gradientnoise mask
			noiseCfg = cfg['submasks']['gradientNoise']
			if noiseCfg['use']:
				gradRays.append(gradient(array, random.uniform(noiseCfg['params']['min'], noiseCfg['params']['max'])))

			# Creating gridnoise mask
			noiseCfg = cfg['submasks']['gridNoise']
			if noiseCfg['use']:
				gridRays.append(grid(array, random.uniform(noiseCfg['params']['min'], noiseCfg['params']['max'])))

		# Start adding noise to images
		print("Started noising.")

		# Function to add gaussblur, noise and normalise images
		def noiseUp(pathToImages, gauss, normals, ext, pad, start=0):

			# Doing each image
			for i, imageFile in enumerate(glob.glob("."+pathToImages+"*."+ext), start=start):

				if i == 0:
					imageStartTime = time.time()
				# Estimating total time
				if i == 10:
					imageEndTime = numberOfImages*(time.time() - imageStartTime)/10

				# Printing amount of time estimated to remain
				if i%10 == 0 and i > 0:
					print("On image"+str(i)+". Remaining time:")
					print(imageEndTime-(time.time()-imageStartTime))

				# Opening up image
				imageToNoise = Image.open(imageFile)

				# Converting image to grayscale
				imageToNoise = ImageOps.grayscale(imageToNoise)

				# Adding gauss noise
				if gauss['use']:
					params = gauss['params']
					imageToNoise = imageToNoise.filter(ImageFilter.GaussianBlur(radius = random.uniform(params['min'], params['max'])))

				# Converting image to array
				imageToNoise = np.asarray(imageToNoise)

				# Adding one of each type of noise
				imageToNoise = makeNoisy(imageToNoise, [sNRays, sineRays, gradRays, gridRays])

				# Normalising image
				if normals['use']:
					params = normals['params']
					imageToNoise = normalize(imageToNoise, random.randint(params['min'], params['max']), params['mean'])

				# Converting back to image type and saving
				imageToNoise = Image.fromarray(imageToNoise).convert('L')
				name = str(i).zfill(pad)
				imageToNoise.save(os.getcwd()+pathToImages+'normalised/'+name+"."+ext)

		# Storing start time
		startTime = time.time()

		# Train images
		print()
		print("Processing train set.")
		print()
		noiseUp('/data/train_set/', cfg['submasks']['gauss'], cfg['submasks']['normalize'], cfg['submasks']['ext'], padding)

		# Test images
		print()
		print("Processing test set.")
		print()
		startIm = len(glob.glob('./data/train_set/*'+cfg['submasks']['ext']))
		noiseUp('/data/test_set/', cfg['submasks']['gauss'], cfg['submasks']['normalize'], cfg['submasks']['ext'], padding, start=startIm)

		# Storing end time
		endTime = time.time()

		print("Done in "+str(endTime - startTime)+" seconds.")