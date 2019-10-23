#import SimpleCV
from SimpleCV import *

img = Image('markers_rotated.jpg')


#should make markers into circles so that I can use isCircle (isSquare will fail on rotation?)
#make marker a black background with 3 colored circles?

blue_distance = img.hueDistance(Color.BLUE).invert().threshold(210)
blue_distance.save('outputBD.png')
blobs_blue = blue_distance.findBlobs(threshval=200, minsize=100)
blobs_blue.draw(color=Color.RED, width=2)
#blue_distance.show()

blobs_blue_filter = np.zeros(len(blobs_blue),np.bool) #create list the length of blobs_red with bool elements
for index in range(len(blobs_blue)):
  tmp=blobs_blue[index].isSquare(tolerance=0.25, ratiotolerance=0.3)
  if tmp==True:
    blobs_blue_filter[index] = 1;
    blue_distance.dl().circle(blobs_blue[index].centroid(),3,color=Color.HOTPINK)
blobs_blue_selected = blobs_blue.filter(blobs_blue_filter)
blobs_blue_centroid = np.zeros((len(blobs_blue_selected),2),np.float) #create list the length of blobs_red with bool elements
for index in range(len(blobs_blue_centroid)):
  blobs_blue_centroid[index] = blobs_blue_selected[index].centroid()
print blobs_blue_centroid
blobs_blue_selected.draw(color=Color.HOTPINK, width=3) #make outlines around selected object bolder

print "%d blue blobs found" % len(blobs_blue)
print "%d blue blobs selected" % len(blobs_blue_selected)

# --------------------------------------------------------------------


red_distance = img.hueDistance(Color.RED).invert().threshold(210)
red_distance.save('outputRD.png')
blobs_red = red_distance.findBlobs(threshval=200, minsize=100)
blobs_red.draw(color=Color.FORESTGREEN, width=2)

blobs_red_filter = np.zeros(len(blobs_red),np.bool) #create list the length of blobs_red with bool elements
for index in range(len(blobs_red)):
  tmp=blobs_red[index].isSquare(tolerance=0.25, ratiotolerance=0.3)
  if tmp==True:
    blobs_red_filter[index] = 1;
    red_distance.dl().circle(blobs_red[index].centroid(),3,color=Color.YELLOW)
blobs_red_selected = blobs_red.filter(blobs_red_filter)
blobs_red_centroid = np.zeros((len(blobs_red_selected),2),np.float) #create list the length of blobs_red with bool elements
for index in range(len(blobs_red_centroid)):
  blobs_red_centroid[index] = blobs_red_selected[index].centroid()
print blobs_red_centroid
blobs_red_selected.draw(color=Color.LIME, width=3) #make outlines around selected object bolder

print "%d red blobs found" % len(blobs_red)
print "%d red blobs selected" % len(blobs_red_selected)


# --------------------------------------------------------------------

# Determine selected blob size average

blob_mean_area = (np.mean(blobs_red_selected.area()) + np.mean(blobs_blue_selected.area()))/2
print "Mean Blob Area"
print blob_mean_area

# --------------------------------------------------------------------


blob_distances = np.zeros((len(blobs_blue_selected),len(blobs_red_selected)),np.float)

for index_b in range(len(blobs_blue_selected)):
  for index_r in range(len(blobs_red_selected)):
    #tmp= blobs_blue_centroid[index_b,0]
    #print tmp
    blob_distances[index_b,index_r] = (np.square(blobs_blue_centroid[index_b,0] - blobs_red_centroid[index_r,0]) + np.square(blobs_blue_centroid[index_b,1] - blobs_red_centroid[index_r,1]))

    #
    #
    #
    # BUG : blob distances needs a sqrt around it
    #
    #
    #
    
print "Blob Distances:" 
print blob_distances

minvalues = np.amin(blob_distances,axis=1)
print "Min values"
print minvalues

location = np.zeros(len(minvalues),np.int)
markers  = np.zeros((len(minvalues),2),np.int)

print "Min value locations"
count = 0
for index in range(len(blobs_blue_selected)):
  if minvalues[index] < blob_mean_area*2 :
    location[index] = np.where(blob_distances[index,:]==minvalues[index])[0]
    print location[index]
    markers[count,0] = (blobs_blue_centroid[index,0]+blobs_red_centroid[location[index],0]) / 2
    markers[count,1] = (blobs_blue_centroid[index,1]+blobs_red_centroid[location[index],1]) / 2
    red_distance.dl().circle(markers[count,:],5,color=Color.SILVER)
    count = count+1

red_distance.dl().line(markers[0,:],markers[1,:],width=5,color=Color.SILVER)

print "Marker Locations"
print markers


img.addDrawingLayer(blue_distance.dl())
img.addDrawingLayer(red_distance.dl())

img.save('output.png')


# AQUAMARINE
# AZURE
# BACKGROUND
# BEIGE
# BLACK
# BLUE
# CHARCOAL
# CRIMSON
# CYAN
# DEFAULT
# FOREGROUND
# FORESTGREEN
# FUCHSIA
# GOLD
# GRAY
# GREEN
# HOTPINK
# INDIGO
# IVORY
# KHAKI
# LEGO_BLUE
# LEGO_ORANGE
# LIME
# MAROON
# MAYBE_BACKGROUND
# MAYBE_FOREGROUND
# MEDIUMBLUE
# NAVYBLUE
# OLIVE
# ORANGE
# PLUM
# PUCE
# RED
# ROYALBLUE
# SALMON
# SILVER
# TAN
# TEAL
# VIOLET
# WATERSHED_BG
# WATERSHED_FG
# WATERSHED_UNSURE
# WHEAT
# WHITE
# YELLOW
