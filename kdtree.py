#!/usr/bin/python

# A python implementation of KdTree data structure
# Note: Dimension is 3 in general

from random import randint

__author__ = u'Sudipta Roy <csy157533@iitd.ernet.in>'

class Node :
    def __init__(self,data=None, axis=None,
            left=None, right=None) :
        self.__data = data
        self.__axis = axis
        self.__left = left
        self.__right = right

    @property
    def data(self) : return self.__data

    @property.setter
    def data(self,val) : self.__data = val

    @property
    def axis(self) : return self.__axis

    @property.setter
    def axis(self,val) : self.__axis = val

    @property
    def left(self) : return self.__left

    @property.setter
    def left(self,val) : self.__left = val

    @property
    def right(self) : return self.__right

    @property.setter
    def right(self,val) : self.__right = val

    @property
    def is_leaf(self) :
        return not self.__axis

class KdTree :
    '''A class implementing KdTree data structure'''
    def __init__(self,points=None,dim=2) :
        self.__dim = dim #dimension of points
        if(points is not None and
                any(pt is None or len(pt) != self.__dim for pt in points)) :
            raise ValueError("Dimension mismatch " + str(points) +
                    " and dimension %d"%dim)
        self.__pts = points
        self.__sorted_view = []

    def build(self) :
        print 'Bulding tree...'
        depth = 0
        if self.__pts is None or len(self.__pts) == 0 :
            print "No points to build the KdTree on. Add points"
            return
        self.__make_sorted_view()
        self.__build_tree(depth)

    def __build_tree(self,depth): pass

    def __make_sorted_view(self) :
        #print self.__pts
        # __sorted_view[d] stores the points sorted in
        # d+1 th dimension
        for i in range(self.__dim) :
            self.__sorted_view.append(sorted(self.__pts,
                key = lambda x : x[i]))
        #print self.__sorted_view

def create_random_points(upper_bound, nr_pts, nr_dim):
    return [create_random_point(upper_bound,nr_dim) for i in xrange(nr_pts)]

def create_random_point(upper_bound, nr_dim) :
    point = []
    for i in xrange(nr_dim) :
        point.append(randint(0,upper_bound))
    return tuple(point)

def main() :
    points = create_random_points(500,25,2)
    kdtree = KdTree(points)
    kdtree.build()

if __name__ == '__main__':
    main()

