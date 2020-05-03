# modified from: https://machinelearningmastery.com/how-to-perform-object-detection-with-yolov3-in-keras/


# load yolov3 model and perform object detection
# based on https://github.com/experiencor/keras-yolo3
import numpy as np
from numpy import expand_dims
from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
import tensorflow as tf
import os, cv2, sys
 
class BoundBox:
	def __init__(self, xmin, ymin, xmax, ymax, objness = None, classes = None):
		self.xmin = xmin
		self.ymin = ymin
		self.xmax = xmax
		self.ymax = ymax
		self.objness = objness
		self.classes = classes
		self.label = -1
		self.score = 0
 
	def get_label(self):
		if self.label == -1:
			self.label = np.argmax(self.classes)
		return self.label
 
	def get_score(self):
		if self.score == 0:
			self.score = self.classes[self.get_label()]
		return self.score

	def get_values(self):
		return([self.ymin, self.xmax, self.ymax, self.xmax])
 
def _sigmoid(x):
	return 1. / (1. + np.exp(-x))

# TODO: can this method be sped up or transferred to tensorflow?
def decode_netout(netout, anchors, obj_thresh, net_h, net_w):
	grid_h, grid_w = netout.shape[:2]
	print(grid_h)
	print(grid_w)
	nb_box = 3
	netout = netout.reshape((grid_h, grid_w, nb_box, -1))
	print(netout.shape)
	boxes = []
	#print(netout[..., :2])
	netout[..., :2]  = _sigmoid(netout[..., :2])
	netout[..., 4:]  = _sigmoid(netout[..., 4:])
	netout[..., 5:]  = netout[..., 4][..., np.newaxis] * netout[..., 5:]
	netout[..., 5:] *= netout[..., 5:] > obj_thresh
 
	for i in range(grid_h*grid_w):
		row = i / grid_w
		col = i % grid_w
		for b in range(nb_box):
			# 4th element is objectness score
			objectness = netout[int(row)][int(col)][b][4]
			if(objectness.all() <= obj_thresh): continue
			# first 4 elements are x, y, w, and h
			x, y, w, h = netout[int(row)][int(col)][b][:4]
			x = (col + x) / grid_w # center position, unit: image width
			y = (row + y) / grid_h # center position, unit: image height
			w = anchors[2 * b + 0] * np.exp(w) / net_w # unit: image width
			h = anchors[2 * b + 1] * np.exp(h) / net_h # unit: image height
			# last elements are class probabilities
			classes = netout[int(row)][col][b][5:]
			box = BoundBox(x-w/2, y-h/2, x+w/2, y+h/2, objectness, classes)
			boxes.append(box)
	return boxes
 
def correct_yolo_boxes(boxes, image_h, image_w, net_h, net_w):
	new_w, new_h = net_w, net_h
	for i in range(len(boxes)):
		x_offset, x_scale = (net_w - new_w)/2./net_w, float(new_w)/net_w
		y_offset, y_scale = (net_h - new_h)/2./net_h, float(new_h)/net_h
		boxes[i].xmin = int((boxes[i].xmin - x_offset) / x_scale * image_w)
		boxes[i].xmax = int((boxes[i].xmax - x_offset) / x_scale * image_w)
		boxes[i].ymin = int((boxes[i].ymin - y_offset) / y_scale * image_h)
		boxes[i].ymax = int((boxes[i].ymax - y_offset) / y_scale * image_h)
 
# def _interval_overlap(interval_a, interval_b):
# 	x1, x2 = interval_a
# 	x3, x4 = interval_b
# 	if x3 < x1:
# 		if x4 < x1:
# 			return 0
# 		else:
# 			return min(x2,x4) - x1
# 	else:
# 		if x2 < x3:
# 			 return 0
# 		else:
# 			return min(x2,x4) - x3
 
# def bbox_iou(box1, box2):
# 	intersect_w = _interval_overlap([box1.xmin, box1.xmax], [box2.xmin, box2.xmax])
# 	intersect_h = _interval_overlap([box1.ymin, box1.ymax], [box2.ymin, box2.ymax])
# 	intersect = intersect_w * intersect_h
# 	w1, h1 = box1.xmax-box1.xmin, box1.ymax-box1.ymin
# 	w2, h2 = box2.xmax-box2.xmin, box2.ymax-box2.ymin
# 	union = w1*h1 + w2*h2 - intersect
# 	return float(intersect) / union
 
def do_nms(boxes, nms_thresh):
	# perform non-max suppression
	# https://www.tensorflow.org/api_docs/python/tf/image/non_max_suppression
	scores = []
	tensor_boxes = []
	# print("Length before: " + str(len(boxes)))
	for b in boxes:
		scores.append(b.get_score())
		tensor_boxes.append(b.get_values())
	scores = tf.constant(scores, dtype=tf.float32)
	# tf.print(scores)
	# print(tf.reduce_sum(scores))
	tensor_boxes = tf.constant(tensor_boxes, dtype=tf.float32)
	# tf.print(tensor_boxes)

	# max_score = 0
	# max_index = 0
	# for i,b in enumerate(boxes):
	# 	if b.get_score() > max_score:
	# 		max_score = b.get_score()
	# 		max_index = i

	# print(max_index)
	# print(boxes[max_index].get_values())
	# print(boxes[max_index].get_label())
	# print(boxes[max_index].get_score())
	# print("-----------------")
	
	# TODO: should this be run individually for each class/label type and combined?
	selected_indexes, _, = tf.unique(tf.image.non_max_suppression(boxes=tensor_boxes, scores=scores, max_output_size=12, iou_threshold=nms_thresh))
	# print(selected_indexes)
	pruned_boxes = [boxes[i] for i in selected_indexes]
	# ss = [boxes[i].get_score() for i in selected_indexes]
	# print(ss)
	# ll = [boxes[i].get_label() for i in selected_indexes]
	# print(ll)
	return(pruned_boxes)


	# original code, way too slow, use tf for speedup
	# if len(boxes) > 0:
	# 	nb_class = len(boxes[0].classes)
	# else:
	# 	return
	# for c in range(nb_class):
	# 	sorted_indices = np.argsort([-box.classes[c] for box in boxes])
	# 	for i in range(len(sorted_indices)):
	# 		index_i = sorted_indices[i]
	# 		if boxes[index_i].classes[c] == 0: continue
	# 		for j in range(i+1, len(sorted_indices)):
	# 			index_j = sorted_indices[j]
	# 			if bbox_iou(boxes[index_i], boxes[index_j]) >= nms_thresh:
	# 				boxes[index_j].classes[c] = 0
 
# load and prepare an image
def load_image_pixels(filename, shape):
	# load the image to get its shape
	image = load_img(filename)
	width, height = image.size
	# load the image with the required size
	image = load_img(filename, target_size=shape)
	# convert to numpy array
	image = img_to_array(image)
	# scale pixel values to [0, 1]
	image = image.astype('float32')
	image /= 255.0
	# add a dimension so that we have one sample
	image = expand_dims(image, 0)
	return image, width, height
 
# get all of the results above a threshold
def get_boxes(boxes, labels, thresh):
	v_boxes, v_labels, v_scores = list(), list(), list()
	# enumerate all boxes
	for box in boxes:
		# enumerate all possible labels
		for i in range(len(labels)):
			# check if the threshold for this label is high enough
			if box.classes[i] > thresh:
				v_boxes.append(box)
				v_labels.append(labels[i])
				v_scores.append(box.classes[i]*100)
				# don't break, many labels may trigger for one box
	return v_boxes, v_labels, v_scores
 
# draw all results
def draw_boxes(filename, v_boxes, v_labels, v_scores):
	# load the image
	data = cv2.imread(filename)
	# plot each box
	for i in range(len(v_boxes)):
		box = v_boxes[i]
		# draw bounding box
		cv2.rectangle(data, (box.xmin, box.ymin), (box.xmax, box.ymax), color=(0, 0, 255), thickness=3) # BGR order
		# draw text and score in top left corner
		label = "%s %.2f" % (v_labels[i], v_scores[i])
		# https://stackoverflow.com/questions/16615662/how-to-write-text-on-a-image-in-windows-using-python-opencv2
		cv2.putText(data, label, (box.xmin, box.ymin), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

	cv2.imwrite('/testing/'+os.path.splitext(os.path.basename(filename))[0]+'-bb.jpg', data)
