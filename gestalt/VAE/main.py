#this is where the main running of experiments and stuff goes. could be useful
# we aim to keep this package quite thin and self contained, and eventually put it up as another github repository with just the VAE gestalt stuff, which could be useful, but who knows really
# and then ahve it as a small and self-contained package. That would be the hope, at least

#we're going to have to copy our data somewhere in here, but that's hardly the end of the worldto be honest
import numpy as np
from utils import *
from models import *

BATCH_SIZE = 64

def test_gestalt_half_split_images(fname, epochs=20, model=DCVAE,optimizer='sgd', save_name=None):
	imgs = load_array(fname)
	imgs = imgs.astype('float32')/255.
	train, val, test = split_first_test_val_train(imgs)
	slicelefttrain, slicerighttrain = split_dataset_center_slice(train, 20)
	slicelefttest, slicerighttest = split_dataset_center_slice(test, 20)
	sliceleftval, slicerightval = split_dataset_center_slice(val, 20)
	#input_shape = slicelefttrain.shape[1:]

	#we do the concatenatoins to produce the full thing
	train1 = np.concatenate((slicelefttrain, slicerighttrain),axis=0)
	train2 = np.concatenate((slicerighttrain, slicelefttrain),axis=0)
	val1 = np.concatenate((sliceleftval, slicerightval), axis=0)
	val2 = np.concatenate((slicerightval, sliceleftval),axis=0)
	test1= np.concatenate((slicelefttest, slicerighttest), axis=0)
	test2 = np.concatenate((slicerighttest,slicelefttest),axis=0)

	#now we reshape as well
	sh = train1.shape
	#train1 = np.reshape(train1, (sh[0],sh[1],sh[2],1))
	#train2 = np.reshape(train2, (sh[0],sh[1],sh[2], 1))
	#val1 = np.reshape(val1, (len(val1),sh[1],sh[2],1))
	#val2 = np.reshape(val2, (len(val2),sh[1],sh[2], 1))
	#test1 = np.reshape(test1, (len(test1),sh[1],sh[2],1))
	#test2 = np.reshape(test2, (len(test2),sh[1],sh[2], 1))

	input_shape = train1.shape[1:]
	
	

	callbacks = build_callbacks("results/")

	vae, encoder,decoder = model(input_shape)
	#vae.compile(optimizer=optimizer,loss=None)
	#we fit the vae
	his = vae.fit(train1,train2, epochs=epochs, batch_size = BATCH_SIZE, shuffle=True, validation_data = (val1, val2), callbacks = callbacks)
	history = serialize_class_object(his)

	#now we try to get the predictions
	full_predictions = vae.predict(test1, batch_size=BATCH_SIZE)
	# and we can save them or view the mor wahtever. do that in a bit tomorrow perhaps. and hope to god it works
	


	#encoder.compile(optimizer=optimizer, loss=None)
	#decoder.compile(optimizer=optimizer, loss=None)

	#I think we're oau with that then presumably
	if save_name:
		save_array([full_predictions, history],save_name)
	return full_predictions, history

	
	





if __name__ == '__main__':
	test_gestalt_half_split_images("testimages_combined", save_name="results/test_1")
