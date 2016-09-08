#!/usr/bin/python

# A python implementation of KdTree data structure
# Note: Dimension is 3 in general

from random import randint
import logging
import sys

__author__ = u'Sudipta Roy <csy157533@iitd.ernet.in>'
logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s')
sys.setrecursionlimit(10000)

class Node(object) :
    def __init__(self, left=None, right=None, parent=None) :
        self.__left = left
        self.__right = right
        self.__parent = parent

    @property
    def left(self) : return self.__left

    @left.setter
    def left(self,val) : self.__left = val

    @property
    def right(self) : return self.__right

    @right.setter
    def right(self,val) : self.__right = val

    @property
    def parent(self) : return self.__parent

    @parent.setter
    def parent(self,val) : self.__parent = val

class LeafNode(Node) :
    def __init__(self,data=None, parent=None) :
        self.__data = data
        super(LeafNode,self).__init__(parent=parent)

    @property
    def data(self) : return self.__data

    @data.setter
    def data(self,val) : self.__data = val

class InternalNode(Node) :
    def __init__(self,axis=None, left=None, right=None, parent=None) :
        self.__axis = axis
        super(InternalNode,self).__init__(left=left, right=right, parent=parent)

    @property
    def axis(self) : return self.__axis

    @axis.setter
    def axis(self,val) : self.__axis = val

class KdTree(object) :
    '''A class implementing KdTree data structure'''
    def __init__(self,points=None,dim=2) :
        self.__root = Node()
        self.__dim = dim #dimension of points
        if(points is not None and
                any(pt is None or len(pt) != self.__dim for pt in points)) :
            raise ValueError("Dimension mismatch " + str(points) +
                    " and dimension %d"%dim)
        self.__pts = points
        self.__sorted_view = []
        self.__height = -1

    def build(self) :
        logging.debug("Building tree...")
        depth = 0
        if self.__pts is None or len(self.__pts) == 0 :
            log.error("No points to build the KdTree on. Add points")
            return
        self.__make_sorted_view()
        self.__root = self.__build_tree(self.__sorted_view[0],depth)
        print self.__root

    def print_tree(self, node) : pass

    @property
    def root(self) : return self.__root

    def __build_tree(self,pts,depth, parent=None) :
        logging.debug('depth : ' +str(depth))
        if len(pts) == 1 :
            return LeafNode(data=pts[0], parent=parent)
        dim = self.__canon(depth)
        print 'dim :' + str(dim)
        max_pt = max(pts,key = lambda x :
            x[self.__canon(dim+1)])[self.__canon(dim+1)]
        min_pt = min(pts,key = lambda x :
            x[self.__canon(dim+1)])[self.__canon(dim+1)]
        mx = max(pts,key = lambda x : x[dim])[dim] #max of current dimension
        mn = min(pts,key = lambda x : x[dim])[dim] #min of current dimension
        med = KdTree.median(pts,dim)
        next_view = self.__sorted_view[self.__canon(dim+1)]
        lesser = [pt for pt in next_view if pt[dim]<med
            and min_pt<=pt[self.__canon(dim+1)]<=max_pt
            and mn<=pt[dim]<mx]
        greater = [pt for pt in next_view if pt[dim]>=med
            and min_pt<=pt[self.__canon(dim+1)]<=max_pt
            and mn<=pt[dim]<=mx]
        print 'median : ' + str(med)
        print str(min_pt) + ':' + str(max_pt)
        print lesser
        print greater
        node = InternalNode(axis = med, parent=parent)
        node.left = self.__build_tree(lesser,depth+1, parent=node)
        node.right = self.__build_tree(greater,depth+1, parent=node)
        return node

    def __canon(self,index) :
        return index % self.__dim #increment/decrement of index must be modulo @dim

    def add_points(self, points) :
        for point in points :
            self.__pts.append(point)

    def __make_sorted_view(self) :
        # __sorted_view[d] stores the points sorted in
        # d+1 th dimension
        for i in range(self.__dim) :
            self.__sorted_view.append(sorted(self.__pts,
                key = lambda x : x[i]))
        print self.__sorted_view

    @staticmethod
    def median(lst,index) :
        lst_len = len(lst)
        idx = (lst_len-1)//2
        if lst_len % 2 :
            return lst[idx][index]
        return (lst[idx][index] + lst[idx+1][index])/2.0

def create_random_points(upper_bound, nr_pts, nr_dim):
    '''returns a LIST of size nr_pts of nr_dim dimensional points'''
    return [create_random_point(upper_bound,nr_dim) for i in xrange(nr_pts)]

def create_random_point(upper_bound, nr_dim) :
    '''returns a SINGLE nr_dim dimensional point'''
    point = []
    for i in xrange(nr_dim) :
        point.append(randint(0,upper_bound))
    return tuple(point)


def main() :
    points = [(307, 75), (77, 92), (208, 146), (376, 63), (129, 248), (265, 258), (57, 410), (389, 456),
            (188, 128)]#, (429, 214),(476, 132), (272, 485), (8, 415), (290, 124),
            #(407, 205), (166, 148)]
    #points = create_random_points(500,25,2)
    #points=[(16, 7, 214), (52, 407, 386), (65, 126, 83), (88, 204, 371)]
    kdtree = KdTree(points,dim=2)
    kdtree.build()

if __name__ == '__main__':
    main()

