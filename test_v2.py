#import SimpleCV
from SimpleCV import *
import time

time_start = time.clock()
tic = time_start

img = Image('IMG_3080.JPG')


toc = time.clock()
delta_t = (toc-tic)
print "    %f s to open image" % delta_t
tic=toc

blue_distance = img.hueDistance(Color.BLUE).invert().threshold(210)

toc = time.clock()
delta_t = (toc-tic)
print "    %f s to calculate blue hue distance" % delta_t
tic=toc

#blue_distance.save('outputBD_v2.png')

toc = time.clock()
delta_t = (toc-tic)
print "    %f s to save image file" % delta_t
tic=toc

blobs_blue = blue_distance.findBlobs(threshval=200, minsize=50)

toc = time.clock()
delta_t = (toc-tic)
print "    %f s to find blue blobs" % delta_t
tic=toc

blobs_blue.draw(color=Color.RED, width=2)
#blue_ditance.show()

blobs_blue_filter = np.zeros(len(blobs_blue),np.bool) #create list the length of blobs_blue with bool elements
for index in range(len(blobs_blue)):
  
  #code to determine if blob is a circle, mostly taken from Blob.py because using isCircle was printing text to screen for some reason
  w = blobs_blue[index].mHullMask.width
  h = blobs_blue[index].mHullMask.height
  #print "%d %d blob size" % (w, h)
  idealcircle = Image((w,h))
  radius = min(w,h) / 2
  #print "%d radius" % radius
  idealcircle.dl().circle((w/2, h/2), radius, filled= True, color=Color.WHITE)
  idealcircle = idealcircle.applyLayers()
  netdiff = (idealcircle - blobs_blue[index].mHullMask) + (blobs_blue[index].mHullMask - idealcircle)
  numblack, numwhite = netdiff.histogram(2)
  #print "%d %d black and white" % (numblack, numwhite)
  circle_variance = float(numwhite) / (radius * radius * np.pi)
  # print "%d %d blob size" % (w, h)
  # print "%d %d blob location" % (blobs_blue[index].x, blobs_blue[index].y)
  # print "%f circle variance" % circle_variance
  # print "%d blob area" % blobs_blue[index].area()
  # sqa = w*h
  # print "%d sq area" % sqa
  # circa = radius * radius * np.pi
  # print "%d circ area" % circa
  # print " " 
  
  if circle_variance<=.3:
    blobs_blue_filter[index] = 1;
    blue_distance.dl().circle(blobs_blue[index].centroid(),3,color=Color.HOTPINK)


blobs_blue_selected = blobs_blue.filter(blobs_blue_filter)
blobs_blue_centroid = np.zeros((len(blobs_blue_selected),2),np.float) #create list the length of blobs_blue_selected with bool elements
for index in range(len(blobs_blue_centroid)):
  blobs_blue_centroid[index] = blobs_blue_selected[index].centroid()
# print blobs_blue_centroid
blobs_blue_selected.draw(color=Color.HOTPINK, width=3) #make outlines around selected object bolder

print "%d blue blobs found, %d selected" % (len(blobs_blue), len(blobs_blue_selected))

toc = time.clock()
delta_t = (toc-tic)
print "    %f s to do blue blob selection" % delta_t
tic=toc

# --------------------------------------------------------------------


red_distance = img.hueDistance(Color.RED).invert().threshold(210)
#red_distance.save('outputRD_v2.png')
blobs_red = red_distance.findBlobs(threshval=200, minsize=50)
blobs_red.draw(color=Color.FORESTGREEN, width=2)

blobs_red_filter = np.zeros(len(blobs_red),np.bool) #create list the length of blobs_red with bool elements
for index in range(len(blobs_red)):

  #code to determine if blob is a circle, mostly taken from Blob.py because using isCircle was printing text to screen for some reason
  w = blobs_red[index].mHullMask.width
  h = blobs_red[index].mHullMask.height
  #print "%d %d blob size" % (w, h)
  idealcircle = Image((w,h))
  radius = min(w,h) / 2
  #print "%d radius" % radius
  idealcircle.dl().circle((w/2, h/2), radius, filled= True, color=Color.WHITE)
  idealcircle = idealcircle.applyLayers()
  netdiff = (idealcircle - blobs_red[index].mHullMask) + (blobs_red[index].mHullMask - idealcircle)
  numblack, numwhite = netdiff.histogram(2)
  #print "%d %d black and white" % (numblack, numwhite)
  circle_variance = float(numwhite) / (radius * radius * np.pi)
  
  
  if circle_variance<=.3:
    blobs_red_filter[index] = 1;
    red_distance.dl().circle(blobs_red[index].centroid(),3,color=Color.YELLOW)
    
    
blobs_red_selected = blobs_red.filter(blobs_red_filter)
blobs_red_centroid = np.zeros((len(blobs_red_selected),2),np.float) #create list the length of blobs_red with bool elements
for index in range(len(blobs_red_centroid)):
  blobs_red_centroid[index] = blobs_red_selected[index].centroid()
# print blobs_red_centroid
blobs_red_selected.draw(color=Color.LIME, width=3) #make outlines around selected object bolder

print "%d red blobs found, %d selected" % (len(blobs_red), len(blobs_red_selected))

# --------------------------------------------------------------------

# Calculate the distance between every combination of selected (circular) red and blue blobs
blob_distances = np.zeros((len(blobs_blue_selected),len(blobs_red_selected)),np.float)


markers = np.zeros((1,3)) #array is x, y, alpha (angle between red and blue off vertical.  angle is zero is blue is directly above red)

count = 0
for index_b in range(len(blobs_blue_selected)):
  for index_r in range(len(blobs_red_selected)):
    blob_distances[index_b,index_r] = np.sqrt(np.square(blobs_blue_centroid[index_b,0] - blobs_red_centroid[index_r,0]) + np.square(blobs_blue_centroid[index_b,1] - blobs_red_centroid[index_r,1]))
    mean_blob_diam = (blobs_blue_selected[index_b].width() + blobs_red_selected[index_r].width() + blobs_blue_selected[index_b].height() + blobs_red_selected[index_r].height())/4
    # print "%d mean blob diam" %  mean_blob_diam
    # print "%d blob dist" %  blob_distances[index_b,index_r]
    
    if (blob_distances[index_b,index_r] < (5*mean_blob_diam)) & (blob_distances[index_b,index_r] > (1.0*mean_blob_diam)) : #if the blobs are within 1.5 to 3*blob_diam of eachother
      blue_blob_area = blobs_blue_selected[index_b].area()
      red_blob_area = blobs_red_selected[index_r].area()
      
      blob_area_perc_diff = (abs(blue_blob_area-red_blob_area) / ((blue_blob_area + red_blob_area)/2) )
      # print "%f blob area perc diff" % blob_area_perc_diff
      if blob_area_perc_diff<.5: # if blob area percent difference is less than 50%
        
        region_y_mean = (blobs_blue_centroid[index_b,1] + blobs_red_centroid[index_r,1])/2
        region_x_mean = (blobs_blue_centroid[index_b,0] + blobs_red_centroid[index_r,0])/2
        region_size = mean_blob_diam/np.sqrt(2)*.5
        
        region_x_min = region_x_mean-region_size
        region_y_min = region_y_mean-region_size
        region_x_max = region_x_mean+region_size
        region_y_max = region_y_mean+region_size
        
        region_angle = np.arctan2(blobs_red_centroid[index_r,0] - blobs_blue_centroid[index_b,0]  ,  blobs_red_centroid[index_r,1] - blobs_blue_centroid[index_b,1])*57.2958 # angle between red and blue blobs converted to degrees
        
        # print "%f %f %f" % (region_x_mean,region_y_mean,region_size)
        red_distance.dl().rectangle2pts((region_x_min,region_y_min),(region_x_max, region_y_max), color=Color.SILVER)
        
        subreg1 = img.regionSelect(region_x_min,region_y_min,region_x_max,region_y_max)
        subreg = subreg1.smooth().grayscale().binarize(40).invert() #the binarize threshold can be tuned

        subreg_meanColor = subreg.meanColor()
        subreg_value = max(subreg_meanColor)
        # print "subregion value %f " % subreg_value
        subreg.save("output_v2_sr"+str(index_b)+"_"+str(index_r)+".png")

        if (subreg_value < 5): # if the subregion has less than 5 pixels that were above the binarize threshold
        
          red_distance.dl().line(blobs_blue_centroid[index_b,:],blobs_red_centroid[index_r,:],width=5,color=Color.SILVER)
          #img.drawText(text="V=%d" % subreg_value,x=blobs_blue_centroid[index_b,:],y=blobs_red_centroid[index_r,:],fontsize=40)
          
          print "Marker located at %d %d" % (region_x_mean,region_y_mean)
          markers=np.append(markers,[[region_x_mean,region_y_mean,region_angle]], axis=0)
          count = count+1


print markers


#Apply the drawing layers to the image
img.addDrawingLayer(blue_distance.dl())
img.addDrawingLayer(red_distance.dl())

# Calculate image rotation between the first two markers
rotate_angle = -1*np.mean(markers[1:,2])
print "Image should be rotated by %f" % rotate_angle




img.save('output_v2.png')


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
