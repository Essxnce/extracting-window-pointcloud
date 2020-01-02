import rhinoscriptsyntax as rs
import Rhino as rh
from Rhino.Geometry import Point3d as pt
from Rhino.Geometry import NurbsSurface as ns
from scriptcontext import doc
import random
import math
from math import pow as sq



def extractWindow():
    obj = rs.GetObjects("Select Pointclouds", rs.filter.pointcloud, True)

    points, length = analyzePointcloud(obj)

    wallPtList, width = divideByX(obj, points, length)

    #print(len(wallPtList))


    projPointsList, projSrf = projection(wallPtList)

    #print(projPointsList)
    #print(len(projPointsList))
    #print(projSrf)

    n, m, cenPtList = divideSrf(projSrf)


    height = n + 1
    width = m + 1
    
    print(width)          ### 115 
    print(height)         ### 36

    ### generate grid surfaces ###
    surfaceList = []
    for i in range(0, len(cenPtList)):
        surfaceList.append(srfFromCenPt(cenPtList[i]))
    #print(surfaceList[0])



    ### making container : points in a grid ###
    
    # Define a container
    container = []
    for i in range(0, len(cenPtList)):
        container.append([])

    # Putting projected points into each grid that contains corresponding points
    y = 0.5
    z = 0.5

    for j in range(0, len(projPointsList)):
        for k in range(0, len(cenPtList)):
            if (((cenPtList[k][1] - y) < projPointsList[j][0][1]) and (projPointsList[j][0][1] < (cenPtList[k][1] + y)) and ((cenPtList[k][2] - z) < projPointsList[j][0][2]) and (projPointsList[j][0][2] < (cenPtList[k][2] + z))):
                container[k].append(projPointsList[j][0])

    print(len(container))    ### 4140

    ## flatten
    #flatList = [y for x in container for y in x]
    #print(flatList[0])
    #-7.08194438672564,-1.17918300714704,31.0012363968014

    # Bake surfaces in a grid
    #for i in range(0, len(container[2304])):
    #doc.Objects.AddPoint(container[2304][i])


    ## Select window surface (left and right of empty space)
    # for index i of the grid surface
    for i in range(0, len(surfaceList)): # 4140
        for j in range(0, len(container[i])): # The number of points in grids
            # if the grid have not any points,
            if (rs.IsPointInSurface(surfaceList[i], container[i][j]) == False):
                """
                if i == 0:
                    pass
                elif i < width:
                    if (len(container[i-1]) > 0):
                        for k in range(0, len(container[i-1])):
                            doc.Objects.AddPoint(container[i-1][k])
                elif i > width:
                    index1 = i - width
                    index2 = i + width
                """

                # At the top array line
                # (i > 0 and i < width - 1):

                # At the very bottom array line
                # (i > ((height - 1) * width) and i < (width * height - 1)):

                # At the leftmost array line
                # (i % width == 0):

                # At the rightmost array line
                # (i % width == (width - 1)):
                if (i > 0 and i < width - 1) and (i > ((height - 1) * width) and i < (width * height - 1)) and (i % width == 0) and (i % width == (width - 1)):
                    passw 

                else:
                    index1 = i - width
                    index2 = i + width
                    """
                    # Case 1
                    if(len(container[i+1]) == 0 and len(container[index2]) == 0 and len(container[index2 + 1]) == 0):
                        genPtInGrid(container, index1 - 1)
                        genPtInGrid(container, index1)
                        genPtInGrid(container, index1 + 1)
                        genPtInGrid(container, i - 1)
                        genPtInGrid(container, index2 - 1)

                    # Case 2
                    elif(len(container[index1 - 1]) == 0 and len(container[index1]) == 0 and len(container[i - 1]) == 0):
                        genPtInGrid(container, index1 + 1)
                        genPtInGrid(container, i + 1)
                        genPtInGrid(container, index2 - 1)
                        genPtInGrid(container, index2)
                        genPtInGrid(container, index2 + 1)

                    # Case 3
                    elif(len(container[i - 1]) == 0 and len(container[index2 - 1]) == 0 and len(container[index2]) == 0):
                        genPtInGrid(container, index1 - 1)
                        genPtInGrid(container, index1)
                        genPtInGrid(container, index1 + 1)
                        genPtInGrid(container, i + 1)
                        genPtInGrid(container, index2 + 1)

                    # Case 4
                    elif(len(container[index1]) == 0 and len(container[index1 + 1]) == 0 and len(container[i + 1]) == 0):
                        genPtInGrid(container, index1 - 1)
                        genPtInGrid(container, i - 1)
                        genPtInGrid(container, index2 - 1)
                        genPtInGrid(container, index2)
                        genPtInGrid(container, index2 + 1)



                    # Case 5
                    elif(len(container[i - 1]) == 0 and len(container[i + 1]) == 0 and len(container[index2 - 1]) == 0 and len(container[index2]) == 0 and len(container[index2 + 1]) == 0):
                        genPtInGrid(container, index1 - 1)
                        genPtInGrid(container, index1)
                        genPtInGrid(container, index1 + 1)
                        
                    # Case 6
                    elif(len(container[index1]) == 0 and len(container[index1 + 1]) == 0 and len(container[i + 1]) == 0 and len(container[index2]) == 0 and len(container[index2 + 1]) == 0):
                        genPtInGrid(container, index1 - 1)
                        genPtInGrid(container, i - 1)
                        genPtInGrid(container, index2 - 1)


                    # Case 7
                    elif(len(container[index1 - 1]) == 0 and len(container[index1]) == 0 and len(container[i - 1]) == 0 and len(container[index2 - 1]) == 0 and len(container[index2]) == 0):
                        genPtInGrid(container, index1 + 1)
                        genPtInGrid(container, i + 1)
                        genPtInGrid(container, index2 + 1)

                    # Case 8
                    elif(len(container[index1 - 1]) == 0 and len(container[index1]) == 0 and len(container[index1 + 1]) == 0 and len(container[i - 1]) == 0 and len(container[i + 1]) == 0):
                        genPtInGrid(container, index2 - 1)
                        genPtInGrid(container, index2)
                        genPtInGrid(container, index2 + 1)
                    """


                    # Case 9
                    if(len(container[index1 - 1]) == 0 and len(container[i - 1]) == 0 and len(container[index2 - 1]) == 0):
                        genPtInGrid(container, index1)
                        genPtInGrid(container, index1 + 1)
                        genPtInGrid(container, i + 1)
                        genPtInGrid(container, index2)
                        genPtInGrid(container, index2 + 1)

                    # Case 10
                    elif(len(container[index1 + 1]) == 0 and len(container[i + 1]) == 0 and len(container[index2 + 1]) == 0):
                        genPtInGrid(container, index1 - 1)
                        genPtInGrid(container, index1)
                        genPtInGrid(container, i - 1)
                        genPtInGrid(container, index2 - 1)
                        genPtInGrid(container, index2)

                    # Case 11
                    elif(len(container[index1 - 1]) == 0 and len(container[index1]) == 0 and len(container[index1 + 1]) == 0):
                        genPtInGrid(container, i - 1)
                        genPtInGrid(container, i + 1)
                        genPtInGrid(container, index2 - 1)
                        genPtInGrid(container, index2)
                        genPtInGrid(container, index2 + 1)

                    # Case 12
                    elif(len(container[index2 - 1]) == 0 and len(container[index2]) == 0 and len(container[index2 + 1]) == 0):
                        genPtInGrid(container, index1 - 1)
                        genPtInGrid(container, index1)
                        genPtInGrid(container, index1 + 1)
                        genPtInGrid(container, i - 1)
                        genPtInGrid(container, i + 1)

                    """
                    if (len(container[i+1]) == 0):
                        for k in range(0, len(container[i-1])):
                            doc.Objects.AddPoint(container[i-1][k])
                    elif (len(container[i-1]) == 0):
                        for k in range(0, len(container[i+1])):
                            doc.Objects.AddPoint(container[i+1][k])
                    """




########## Function definition ##########


def analyzePointcloud(obj):
    # list of point
    points = rs.PointCloudPoints(obj)

    # The number of pointcloud
    length = rs.PointCloudCount(obj)

    return points, length



def divideByX(obj, points, length):

    list = []

    box = rs.BoundingBox(obj)
    width = int(box[1].X)

    for i in range(0, width):
        inList = []
        list.append(inList)

    for j in range(0, length): # the number of point cloud
        for k in range(0, width): # the width of x coordinates
            if (points[j][0] >= k and points[j][0] <= k+1):
                list[k].append(points[j])

    return list, width


def projection(ptList):
    # Projection of points
    projSrf = rs.GetObjects("Select Surfaces", rs.filter.surface, True)

    #### quantization ####
    projPointsList = []

    for i in range(0, 5):                                                                                                           ##### how much I use x value
        for j in range(0, len(ptList[i])):
            projPoints = rs.ProjectPointToSurface(ptList[i][j], projSrf, (1,0,0))
            # bake projected points
            #rs.AddPoints(projPoints)                                                                                               ##### Point Baking

            # Arranging the projected point as a list
            projPointsList.append(projPoints)

    return projPointsList, projSrf




# Dividing surfaces : generate points
def divideSrf(obj):
    listFromSrf = rs.SurfaceEditPoints(obj)                                                                                           ##############################
    #print(listFromSrf)

    srfWidth = listFromSrf[1][1] - listFromSrf[2][1] # y2 - y1                                                                        ##############################
    srfHeight = listFromSrf[1][2] - listFromSrf[2][2] # z2 - z1


    ####### divide surfaces : generate points #######
    Udiv = int(srfWidth)                                                                       ############################## it depends on surfaces
    Vdiv = int(srfHeight)                                                                      ############################## it depends on surfaces

    u = rs.SurfaceDomain(obj, 0)
    v = rs.SurfaceDomain(obj, 1)


    ptList = []

    rs.EnableRedraw(False)
    for i in range(0, Udiv + 1, 1):
        for j in range(0, Vdiv + 1, 1):
            pt = (i/Udiv, j/Vdiv, 0) ###
            srfPoint = rs.SurfaceParameter(obj, pt)
            newPoint = rs.EvaluateSurface(obj, srfPoint[0], srfPoint[1]) # point3d
            # Bake points
            #ptList.append(rs.AddPoint(newPoint))
            ptList.append(newPoint) 
    #rs.EnableRedraw(True)

    return Udiv, Vdiv, ptList




# Generating surfaces from centerpoints : function definition
def srfFromCenPt(point):
    y = 0.5 
    z = 0.5

    point1 = rh.Geometry.Point3d(point[0], point[1] - y, point[2] + z)
    point2 = rh.Geometry.Point3d(point[0], point[1] + y, point[2] + z)
    point3 = rh.Geometry.Point3d(point[0], point[1] - y, point[2] - z)
    point4 = rh.Geometry.Point3d(point[0], point[1] + y, point[2] - z)


    #ns.CreateFromCorners() function just needs point3d data
    #surface = ns.CreateFromCorners(point1, point2, point4, point3)
    #surface = rh.Geometry.Surface(point1, point2, point4, point3)                                                                        
    ptList = [point1, point2, point4, point3]
    surface = rs.AddSrfPt(ptList)


    
    # bake surface
    """
    rs.EnableRedraw(False)
    doc.Objects.AddSurface(surface)
    doc.Views.Redraw()
    rs.EnableRedraw(True)                                                                                                                 ##### Surface Baking
    """
    return surface


"""
def checkcornerPt(ptList, srfList):
    for i in range(0, len(surfaceList)):
        for j in range(0, len(ptList)):
            rs.IsPointInSurface(surfaceList[i], ptList[j])
"""

def genPtInGrid(pointsList, index):
    reducedPtList = reduceDensity(pointsList)
    for k in range(0, len(reducedPtList[index])):
        doc.Objects.AddPoint(reducedPtList[index][k])



# Reduce density of point cloud
def reduceDensity(pointList):
    reducedPtList = []

    # Random selection
    percentage = 0.01
    sampleNum = int(percentage * len(pointList))
    sample = random.sample(pointList, sampleNum)                                                                                           #### Message: 'Point3d' object has no attribute '__float__'


    for i in range(0, len(sample)):
        genPoint = rs.CreatePoint(sample[i][0], sample[i][1], sample[i][2])
        reducedPtList.append(genPoint)

    return reducedPtList


if __name__=='__main__':
    extractWindow()
