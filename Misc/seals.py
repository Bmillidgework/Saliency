# okay, this is the basic thing with richard about the seals and their calls finding others with somewhat rapidity
# in amid the cacophany of other's calls. I don't know how it works or how they should find it
#their child. basically richard argues that the seal calls being vocal imitators to some extent
# is so that their parents can find them faster in a mass of corresponding calls
# so that can see what is happening, but I don't know - i.e. the seal parents can follow the gradient
# of their call. first things first is finding an algorithm for the gradient
# so I honestly don't know how that will work
# first we turn a numpy array into it and then iterate through it. it might be slow but could be cool

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle


def euclidean_distance(center, point):
	if len(center)!=len(point):
		raise ValueError('Point and center must have same dimensionality')
	total = 0
	for i in xrange(len(center)):
		total += (center[i] - point[i])**2
	return np.sqrt(total)


def save(obj, fname):
	pickle.dump(obj, open(fname, 'wb'))

def load(fname):
	return pickle.load(open(fname, 'rb'))

def create_random_colour_matrix(height, width):
	mat = np.zeros((height, width,3))
	for i in xrange(height):
		for j in xrange(width):
			mat[i][j][0] = (np.random.uniform(low=0, high=1) * 255.)
			mat[i][j][1] = np.random.uniform(low=0, high=1) * 255.
			mat[i][j][2] = np.random.uniform(low=0, high=1) * 255.
	return mat

def average_point(mat,center,px_radius, image_height, image_width):
	x,y = center
	green_total = 0
	red_total= 0
	blue_total = 0
	number = 0
	for i in xrange(px_radius*2):
		for j in xrange(px_radius*2):
			#print "going round loop: " + str(i) + " " + str(j) +" " + str(x) + " " + str(y)
			#print x-px_radius+i 
			#print y-px_radius +j
			xpoint = x - px_radius + i
			ypoint = y - px_radius + j
			#print euclidean_distance(center, (i,j))
			#check it falls within bounds, then check euclidena distance
			if xpoint >=0 and xpoint < image_height:
				if ypoint >=0 and ypoint + j <image_width:
					if euclidean_distance(center, (xpoint, ypoint)) <=px_radius:
						#print "adding to average"
						green_total+= mat[xpoint][ypoint][0]
						print "green added: " + str(mat[xpoint][ypoint][0])
						#print "green total: " + str(green_total)
						red_total+= mat[xpoint][ypoint][1]
						print "red added: " + str(mat[xpoint][ypoint][1])
						blue_total+=mat[xpoint][ypoint][2]
						number+=1

	print "number: ", number
	print "green: " + str(green_total/number)
	print "green total: " + str(green_total)
	return (green_total/number, red_total/number, blue_total/number)

def create_random_mask(shape, multiplier):
	if len(shape)!=3:
		raise ValueError('Shape must be three dimensional for colour image')
	height,width,channels = shape
	return multiplier * np.random.randn(height, width, channels)

def matrix_average_step(mat, average_radius, copy=True, random_multiplier=None):
	if len(mat.shape)!=3 or mat.shape[2]!=3:
		raise ValueError('Matrix must be 2d colour image with 3 channels in format h,w,ch')

	height,width, channels = mat.shape
	if not copy:
		new_mat = mat
	if copy:
		new_mat = np.copy(mat)
	#copy so don't mutate on each run through - I can change this behaviour later if I want
	for i in xrange(height):
		for j in xrange(width):
			new_mat[i][j] = average_point(mat, (i,j), average_radius, height,width)
	if random_multiplier is not None:
		rand = create_random_mask((height,width,channels), random_multiplier)
		print rand
		print new_mat[40][20]
		print rand[40][20]
		new_mat = new_mat + rand
		print new_mat[40][20]
		print np.amax(rand)
		# I don't udnerstand why adding a small random peturbation almost completely
		# foils the random field at all. I really don't understand that and it confuses me
		# like there seems to be no reason for it, and it confuses me so much!
		# the randomisation seems much much much greater than I would think reasonable
		# so Ihoenstly don't know!
		#
	
	return new_mat


#I don't know why this changes so dramatically to be honest, because the averaging isn't that large

# worryingly it seems to change - I dont think it actally to be hoenst, whih is good
# but it seems to have vastly more effect than I wuold think!?
# it should just betiny peturbations, but it's not!
def plot_image_changes(N=1000, radius=2, plot_after=10, multiplier=0):
	orig_mat = create_random_colour_matrix(50,50)
	plt.imshow(orig_mat)
	plt.show()
	for i in xrange(N):
		# this is a horrendously slow algoritm! which i sbad... dagnabbit!
		orig_mat = matrix_average_step(orig_mat, radius,random_multiplier=multiplier)
		print "plot: ", i
		if i % plot_after ==0:
			plt.imshow(orig_mat)
			plt.show()
	return orig_mat

def get_gradient_matrix(N=20, radius=2, plot=True, save_name=None):
	orig_mat = create_random_colour_matrix(50,50)
	for i in xrange(N):
		orig_mat = matrix_average_step(orig_mat, radius)

	if plot:
		plt.imshow(orig_mat)
		plt.show()

	if save_name:
		np.save(save_name, orig_mat)

	return orig_mat

#this isj ust stuff for the agent now - depending on gradients or whaat have you

def select_random_point(mat):
	h,w,ch = mat.shape
	selected = False
	while selected != True:
		height = int(h * np.random.uniform(low=0, high=1))
		width = int(w*np.random.uniform(low=0, high=1))
		if check_proposed_points((height, width), h,w):
			selected=True
	return height,width

def select_target(mat):
	#basicaly selects at random a point
	height, width = select_random_point(mat)
	return mat[height][width]

def random_walk_step(initial_point, step_size):
	# simulates an isotropic gaussian random walk step
	# I can do this the rubbish way of 1-9 simulation!? but thsi seems like a poor choice
	# there is also a sight range, so it coul work and be interesting to see the actual distribution
	# of different calls in various ways!?
	# and also theeffect of random canges. The psychedelic effects of those pictures
	# are quite cool in a way, which is cool. I could send richard this!?
	# do that tonight when I have power to run them as it's fairly straightforward
	# I shuold just do this in the rubbish long and boring way!
	sh,sw = initial_point
	direction = int(8*np.random.uniform())
	if direction == 0:
		return sh+step_size, sw-step_size
	if direction==1:
		return sh+step_size, sw
	if direction==2:
		return sh+step_size, sw+step_size
	if direction==4:
		return sh, sw+step_size
	if direction==5:
		return sh-step_size, sw+step_size
	if direction==6:
		return sh-step_size, sw
	if direction==7:
		return sh-step_size, sw-step_size
	if direction==8:
		return sh, sw-step_size

def check_proposed_points(points, height,width):
	h,w = points
	if h>0 and h<height:
		if w> 0 and h<width:
			return True
	return False

def absolute_diff(p1,p2):
	if len(p1)!=len(p2):
		raise ValueError('Points to be compared must be of same dimension')
	total = 0
	for i in xrange(len(p1)):
		total += np.abs(p1[i] - p2[i])
	return total/len(p1)

def immediate_gradient_step(ideal, center, mat):
	# so bascially aim is given ideal result, coordinates, and the matrix
	# to move in the direction which is closest to the ideal
	# the aim is to prove this is signifiacntly better than before
	# which is cool. I do wonder if smoeone has done mathematical mdoelling of this before
	# I would strongly suspect so!
	best_diff = 99999 # a large number!
	# calculate differences by euclidean differences here
	ch,cw = center
	best_coords = None

	for i in xrange(2):
		for j in xrange(2):
			xpoint = ch+i -1
			ypoint = cw + j -1
			val = mat[xpoint][ypoint]
			diff = euclidean_distance(ideal, val)
			if diff<best_diff:
				best_diff=diff
				best_coords = (xpoint, ypoint)

	return best_coords, best_diff

#clearly aim will beto stop if after a while

def plot_path(coords, height, width,plot=True):
	base = np.zeros((height,width))
	x,y = coords
	for i in xrange(len(coords)):
		base[x][y] = 255.
	if plot:
		plt.imshow(base)
		plt.show()
	return base

def gradient_search_till_atop(mat, less_diff=1, save_name=None, plot=False):

	if len(mat.shape)!=3 and mat.shape[2]!=3:
		raise ValueError('Matrix must be a colour image 3dimensional with 3rd dimension 3 colour channels')
	#initialise random point
	ideal = select_random_point(mat)
	#initialise position
	position = select_random_point(mat)
	#initialise to high value
	diffs = []
	coords = []

	h,w,ch = mat.shape
	diff = 100000

	tries=0
	max_tries = 1000

	while diff < less_diff or tries >= max_tries:
		new_coords, diff = immediate_gradient_step(ideal, position,mat)
		diffs.append(diff)
		coords.append(new_coords)
		position = new_coords
		tries +=1

	if save_name is not None:
		save((diffs, coords), save_name)

	if plot:
		plot_path(coords, h,w)
	return diffs, coords





#so now the questio nis how to do the gradients?


if __name__ == '__main__':
	#plot_image_changes()
	mat = get_gradient_matrix(save_name='gradient_matrix')
	diffs, coords = gradient_search_till_atop(mat,save_name='gradient_search_path', plot=True)


