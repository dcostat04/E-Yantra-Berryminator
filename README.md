# Shape-Color-and-coordinate-detction-using-opencv

In this program we find the following details for each image in the manner shown below:

Detect all the non-white shapes in the images

Store the details of these detected shapes in a list in the same order as mentioned below:

‘test_image_name’: [‘Color’, ‘Shape’, (cX, cY)]
Example => [‘Red’, ‘Circle’, (588, 370)]

All detected shapes in a single image should be stored as a nested list as shown below:
insert img

‘Color’ => String in single quotation marks, with only the first letter in capital
‘Shape’ => String in single quotation marks, with only the first letter in capital
cX => Int value (centroid coordinate of shape on horizontal X-axis direction)
cY => Int value (centroid coordinate of shape on vertical Y-axis direction)
