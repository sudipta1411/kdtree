#!/usr/bin/python

# A python implementation of KdTree data structure
# Note: Dimension is 3 in general

from random import randint
import logging
import sys
import time

__author__ = u'Sudipta Roy <csy157533@iitd.ernet.in>'
logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s')
sys.setrecursionlimit(100)

class Node(object) :
    def __init__(self, left=None, right=None, parent=None, depth=-1) :
        self.__left = left
        self.__right = right
        self.__parent = parent
        self.__depth = depth

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

    @property
    def depth(self) : return self.__depth

    @depth.setter
    def depth(self,val) : self.__depth = val

class LeafNode(Node) :
    def __init__(self,data=None, parent=None, depth=-1) :
        self.__data = data
        super(LeafNode,self).__init__(parent=parent, depth=depth)

    @property
    def data(self) : return self.__data

    @data.setter
    def data(self,val) : self.__data = val

    def __str__(self) :
        return 'L(data={0})'.format(self.__data)

    def __repr__(self) :
        return self.__str__()

class InternalNode(Node) :
    def __init__(self,axis=None, left=None, right=None, parent=None, depth=-1) :
        self.__axis = axis
        super(InternalNode,self).__init__(left=left, right=right,
                parent=parent, depth=depth)

    @property
    def axis(self) : return self.__axis

    @axis.setter
    def axis(self,val) : self.__axis = val

    def __str__(self) :
        return 'I(axis={0})'.format(self.__axis)

    def __repr__(self) :
        return self.__str__()

class HyperRectangle(object) :
    def __init__(self,dim,max_coord,min_coord) :
        self.__dim = dim #dimension of the hyperrectangle
        self.__max_coord = max_coord
        self.__min_coord = min_coord

    def inside(self,pt) :
        if len(pt) != self.__dim :
            raise ValueError("Dimension mismatch!!! hyperrectangle ", self.__dim,
                    "while the point is ", pt)
        max_min = zip(self.__min_coord,self.__max_coord)
        for i in range(self.__dim) :
            if pt[i]<max_min[i][0] or pt[i]>max_min[i][1]:
                return False
        return True

    def 

    def __str__(self) :
        return "HyperRectangle {0}".format(list(zip(self.__min_coord,self.__max_coord)))

    def __repr__(self) :
        return self.__str__()

class KdTree(object) :
    '''A class implementing KdTree data structure'''
    def __init__(self,points=None,dim=2) :
        self.__root = Node()
        self.__dim = dim #dimension of points
        if(points is not None and
                any(pt is None or len(pt) != self.__dim for pt in points)) :
            raise ValueError("Dimension mismatch " + str(points) +
                    " and dimension %d"%dim)
        self.__pts = list(set(points))
        #self.__pts = list(set(points))
        self.__sorted_view = []
        self.__height = -1

    def build(self) :
        logging.debug("Building tree...")
        depth = 0
        if self.__pts is None or len(self.__pts) == 0 :
            logging.error("No points to build the KdTree on. Add points")
            return
        start = time.clock()
        self.__make_sorted_view()
        print time.clock() - start, " seconds"
        start = time.clock()
        self.__root = self.__build_tree(self.__sorted_view[0],depth)
        print time.clock() - start, " seconds"
        #print self.__root

    def inorder(self,a, node=None, inte=True) :
        #for debugging purpose only
        this = self.__root if node is None else node
        # if this is not None :
        if isinstance(this,LeafNode) :
            a +=[this]
        else :
            self.inorder(a,this.left,inte)
            if inte == True :
                a += [this]
            self.inorder(a,this.right,inte)

    def query(self, maxes,mins) :
        if rect is None :
            raise ValueError("No Query range specified")
        return self.__query(self.__root, HyperRectangle(maxes, mins, dim=self.__dim))

    @property
    def root(self) : return self.__root

    @property
    def height(self) : return self.__height

    def __build_tree(self,pts,depth, parent=None) :
        # logging.debug('depth : ' +str(depth))
        self.__height = max(self.__height, depth)
        if pts == None or len(pts) == 0 :
            return LeafNode()
        if len(pts) == 1 :
            return LeafNode(data=pts[0], parent=parent, depth=depth)
        dim = self.__canon(depth)
        # print 'dim :' + str(dim)
        # max_next = max(pts,key = lambda x :
            # x[self.__canon(dim+1)])[self.__canon(dim+1)]
        # min_next = min(pts,key = lambda x :
            # x[self.__canon(dim+1)])[self.__canon(dim+1)]
        # min_cur = pts[0][dim] #max(pts,key = lambda x : x[dim])[dim] #max of current dimension
        # max_cur = pts[len(pts)-1][dim] #min(pts,key = lambda x : x[dim])[dim] #min of current dimension
        # max_nn = max(pts,key = lambda x :
            # x[self.__canon(dim+2)])[self.__canon(dim+2)]
        # min_nn = min(pts,key = lambda x :
            # x[self.__canon(dim+2)])[self.__canon(dim+2)]
        med = KdTree.median(pts,dim)
        # next_view = self.__sorted_view[self.__canon(dim+1)]
        # lesser = [pt for pt in next_view if pt[dim]<med
            # and min_next<=pt[self.__canon(dim+1)]<=max_next
            # and min_cur<=pt[dim]<=max_cur
            # and min_nn<=pt[self.__canon(dim+2)]<=max_nn]
        # greater = [pt for pt in next_view if pt[dim]>=med
            # and min_next<=pt[self.__canon(dim+1)]<=max_next
            # and min_cur<=pt[dim]<=max_cur
            # and min_nn<=pt[self.__canon(dim+2)]<=max_nn]
        lesser = [pt for pt in pts if pt[dim]<med]
        lesser.sort(key=lambda x : x[self.__canon(dim+1)])
        greater = [pt for pt in pts if pt[dim]>=med]
        greater.sort(key=lambda x : x[self.__canon(dim+1)])
        # print 'median : ' + str(med)
        # print str(min_cur) + ':' + str(max_cur)
        # print lesser
        # print greater
        node = InternalNode(axis = med, parent=parent, depth=depth)
        node.left = self.__build_tree(lesser,depth+1, parent=node)
        node.right = self.__build_tree(greater,depth+1, parent=node)
        return node

    def __query(self, node, rect) :
        pass

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
        # print self.__sorted_view

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
            (188, 128), (429, 214),(476, 132), (272, 485), (8, 415), (290, 124),
            (407, 205), (166, 148), (166, 149)]
    nr_pts = 4096
    upper_bound =10 * nr_pts
    points = create_random_points(upper_bound,nr_pts,2)
    points3d = create_random_points(upper_bound,nr_pts,3)
    points3d = [(56, 68, 74), (83, 16, 5), (87, 76, 89), (16, 46, 59), (73, 37, 12),
            (59, 27, 82), (71, 10, 13), (73, 61, 53), (62, 26, 85)]
    # print points3d
    # XXX : random 64 points sometimes failing
    kdtree = KdTree(points3d,dim=3)
    kdtree.build()
    print "Height of the tree is : " , kdtree.height
    a=[]
    kdtree.inorder(a,inte=False)
    print a
    print "depth of the tree is : " , kdtree.root.depth

if __name__ == '__main__':
    main()
