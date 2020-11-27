# Importing required packages
from PIL import Image, ImageOps, ImageFilter
from scipy.ndimage.filters import gaussian_filter
import numpy as np
import glob
import time
import os
import random
import yaml
import argparse

# Create smartnoise mask
def smartNoise(array, sigma):
	noise = Image.open('./noiseFiles/noise1.jpg')
	arrayShape = array.shape
	if len(arrayShape) == 2:
		noise = ImageOps.grayscale(noise)
		noiseArray = np.asarray(noise)
		noiseArray = normalize((noiseArray[:arrayShape[0],:arrayShape[1]]-128), sigma)
	return noiseArray

# Create sinusoid noise mask
def sinusoid(array, sigma):
	arrayShape = array.shape
	if len(arrayShape) == 2:
		a = (random.random()-0.5)*2/10
		b = (random.random()-0.5)*2/10
		sineNoise = np.fromfunction(lambda i, j: sigma*np.sin(a*i + b*j), arrayShape)
		return sineNoise

# Create noise gradient mask
def gradient(array, sigma):
	arrayShape = array.shape
	if len(arrayShape) == 2:
		a = random.random()-0.5
		b = random.random()-0.5
		gradNoise = np.fromfunction(lambda i, j: ((i - arrayShape[0]//2)*a + (j - arrayShape[1]//2)*b), arrayShape)
		gradNoise = normalize(gradNoise, sigma) - 127.5
		return gradNoise

# Create grid noise mask
def grid(array, sigma):
	arrayShape = array.shape
	if len(arrayShape) == 2:
		a = random.randint(0, arrayShape[0])
		b = random.randint(0, arrayShape[1])

		aa = (random.random()-0.5)*2
		ab = (random.random()-0.5)*2
		ba = (random.random()-0.5)*2
		bb = (random.random()-0.5)*2

		gridNoise = np.zeros(arrayShape)
		for i in range(arrayShape[0]):
			for j in range(arrayShape[1]):
				if i < a and j < b:
					gridNoise[i][j] = aa
				if i < a and j >= b:
					gridNoise[i][j] = ab
				if i >= a and j < b:
					gridNoise[i][j] = ba
				if i >= a and j >= b:
					gridNoise[i][j] = bb
		gridNoise = normalize(gridNoise, sigma)
		return gridNoise

# Create bloom noise mask
def bloom(array, radius, sigma):
	arrayShape = array.shape
	if len(arrayShape) == 2:

		gridNoise = np.zeros(arrayShape)
		for i in range(arrayShape[0]):
			for j in range(arrayShape[1]):
				if (i - arrayShape[0]/2)**2 + (j - arrayShape[1]/2)**2 <= radius**2:
					gridNoise[i][j] = (random.random()*0.9+0.1)*(sigma/128)*np.sqrt(radius**2 - ((i - arrayShape[0]/2)**2 + (j - arrayShape[1]/2)**2))
		return gaussian_filter(gridNoise, sigma=4)

# Make image noisy, choosing one of each type of noise mask
def makeNoisy(array, noises):
	for noise in noises:
		if len(noise) > 0:
			array = array + random.choice(noise)
	return array

# Normalizing array of values
def normalize(array, sigma, mean=128):
	maximum = np.amax(array)
	minimum = -np.amax(array*(-1))
	array = (array - np.average(array))*sigma/(2*np.std(array)) + mean
	return array.astype(int)