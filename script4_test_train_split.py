# Importing required packages
from PIL import Image
import numpy as np
import glob as g
import time
import os

# Making relevant directories
os.mkdir(os.getcwd() + '/data/')
os.mkdir(os.getcwd() + '/data/train_set/')
os.mkdir(os.getcwd() + '/data/test_set/')

# Finding number of images and test/train split
numberOfImages = len(g.glob("./images/*"))
train_test = int(0.8*numberOfImages)

# Checking whether to run for instant segmented or front/back
instanceSegmentation = g.glob("./masks/*")[0]
instanceSegmentation = os.path.isdir(instanceSegmentation)

# For the instance segmented case
if instanceSegmentation:

	# Noting start time
	startTime = time.time()

	# For each image
	for i in range(numberOfImages):

		# Estimating total time
		if i == 10:
			endTime = numberOfImages*(time.time() - startTime)/10

		# Printing amount of time estimated to remain
		if i%10 == 0 and i > 0:
			print("On image"+str(i)+". Remaining time:")
			print(endTime-(time.time()-startTime))

		# Name of current 'image'
		nameID = str(i).zfill(len(str(numberOfImages)))

		# Opening rendered frame
		image = Image.open('./images/'+nameID+'.png')

		# Saving rendered images

		# Saving image and creating corresponding folder for mask

		# Train set image
		if i < train_test:
			image.save('./data/train_set/'+nameID+'.png')
			os.mkdir(os.getcwd() + '/data/train_set/'+nameID+'/')

		# Test set image
		else:
			image.save('./data/test_set/'+nameID+'.png')
			os.mkdir(os.getcwd() + '/data/test_set/'+nameID+'/')

		# Finding number of islands in the image
		number = len(g.glob('./masks/'+nameID+'/*'))

		# Copying over all island masks as 1 channel image
		for j in range(number):

			# Name of current island
			name = "Cap" + str(j).zfill(len(str(number)))

			# Splitting channels
			r, gr, b, a = Image.open('./masks/'+nameID+'/'+name+'.png').split()

			# Saving current island mask

			# To train set
			if i < train_test:
				r.save('./data/train_set/'+nameID+'/'+name+'.png')

			# To test set
			else:
				r.save('./data/test_set/'+nameID+'/'+name+'.png')

	# Finished work
	print("Finished test-train split. Copy data folder now.")

# For the front/back mask case
if not instanceSegmentation:

	# Noting start time
	startTime = time.time()

	# Saving each image
	for i in range(numberOfImages):

		# Estimating total time
		if i == 10:
			endTime = numberOfImages*(time.time() - startTime)/10

		# Displaying estimated time left
		if i%10 == 0 and i > 0:
			print("On image"+str(i)+". Remaining time:")
			print(endTime-(time.time()-startTime))

		# Deciding name of current image
		nameID = str(i).zfill(len(str(numberOfImages)))

		# Opening rendered image
		image = Image.open('./images/'+nameID+'.png')

		# Opening combined mask and splitting channels
		r, gr, b, a = Image.open('./masks/'+nameID+'.png').split()

		# Saving images and masks

		# For train set
		if i < train_test:
			image.save('./data/train_set/'+nameID+'.png')
			gr.save('./data/train_set/'+nameID+'_front.png')
			r.save('./data/train_set/'+nameID+'_back.png')

		# For test set
		else:
			image.save('./data/test_set/'+nameID+'.png')
			gr.save('./data/test_set/'+nameID+'_front.png')
			r.save('./data/test_set/'+nameID+'_back.png')

	# Finished work
	print("Finished test-train split. Copy data folder now.")