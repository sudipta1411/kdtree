#!/usr/bin/python

# A python implementation of KdTree data structure
# Note: Dimension is 3 in general

from random import randint
import logging
import sys
import time
from optparse import OptionParser

__author__ = u'Sudipta Roy <csy157533@iitd.ernet.in>'
logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s')
#sys.setrecursionlimit(100)

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

    def inside(self, pt) :
        if pt is None :
            return False
        if len(pt) != self.__dim :
            raise ValueError("Dimension mismatch!!! hyperrectangle ", self.__dim,
                    "while the point is ", pt)
        max_min = zip(self.__min_coord,self.__max_coord)
        for i in range(self.__dim) :
            if pt[i]<max_min[i][0] or pt[i]>max_min[i][1] :
                return False
        return True

    def intersect(self, region) :
        # region is a set of points
        # returns True iff any points lies
        # inside the hyperrectangle
        for pt in region :
            if self.inside(pt) :
                return True
        return False

    def contains(self,region) :
        # returns True iff the region
        # is fully contained inside the
        # hyperrectangle
        for pt in region :
            if not self.inside(pt) :
                return False
        return True

    def __str__(self) :
        return "HyperRectangle {0}".format(list(zip(self.__min_coord,self.__max_coord)))

    def __repr__(self) :
        return self.__str__()

class KdTree(object) :
    '''A class implementing KdTree data structure'''
    def __init__(self,points=None,dim=2) :
        self.__root = Node()
        self.__dim = dim #dimension of points
        if points is not None and \
                any(pt is None or len(pt) != self.__dim for pt in points) :
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
        this = self.__root if node is None else node
        # if this is not None :
        if isinstance(this,LeafNode) :
            a +=[this]
        else :
            self.inorder(a,this.left,inte)
            if inte == True :
                a += [this]
            self.inorder(a,this.right,inte)
        return a

    def query(self, maxes,mins) :
        if maxes is None and mins is None :
            raise ValueError("No Query range specified")
        return self.__query(self.__root, HyperRectangle(max_coord=maxes,
            min_coord=mins, dim=self.__dim), [])

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
        med = KdTree.median(pts,dim)
        lesser = [pt for pt in pts if pt[dim]<med]
        lesser.sort(key=lambda x : x[self.__canon(dim+1)])
        greater = [pt for pt in pts if pt[dim]>=med]
        greater.sort(key=lambda x : x[self.__canon(dim+1)])
        node = InternalNode(axis = med, parent=parent, depth=depth)
        node.left = self.__build_tree(lesser,depth+1, parent=node)
        node.right = self.__build_tree(greater,depth+1, parent=node)
        return node

    def __query(self, node, rect, result) :
        if isinstance(node,LeafNode) :
            if rect.inside(node.data) :
                result += [node.data]
        else :
            region = [pt.data for pt in self.inorder([], node.left, inte=False)]
            if rect.contains(region) :
                result += region
            elif rect.intersect(region) :
                self.__query(node.left, rect, result)
            region = [pt.data for pt in self.inorder([], node.right, inte=False)]
            if rect.contains(region) :
                result += region
            elif rect.intersect(region) :
                self.__query(node.right, rect, result)
        return result


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
    logging.debug('Generating {0} random points...'.format(nr_pts))
    return [create_random_point(upper_bound,nr_dim) for i in xrange(nr_pts)]

def create_random_point(upper_bound, nr_dim) :
    '''returns a SINGLE nr_dim dimensional point'''
    point = []
    for i in xrange(nr_dim) :
        point.append(randint(0,upper_bound))
    return tuple(point)

def plot_points(points,maxes,mins) :
    try :
        import matplotlib.pyplot as plt
    except ImportError:
        print 'matplotlib is not installed !!'
        return
    plt.scatter(*zip(*points), marker='o', color='r')
    x_max = maxes[0]
    y_max = maxes[1]
    x_min = mins[0]
    y_min = mins[1]
    plt.plot([x_min,x_min],[y_min,y_max])
    plt.plot([x_min,x_max],[y_min,y_min])
    plt.plot([x_min,x_max],[y_max,y_max])
    plt.plot([x_max,x_max],[y_min,y_max])
    plt.grid()
    plt.show()

def plot_points3d(points,maxes,mins,res) :
    try :
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError :
        print 'matplotlib/numpy is not installed !!'
        return
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter3D(*zip(*points), marker='o', c='y')
    ax.scatter3D(*zip(*res), marker='o', c='r')
    x_max = maxes[0]
    y_max = maxes[1]
    z_max = maxes[2]
    x_min = mins[0]
    y_min = mins[1]
    z_min = mins[2]
    r1 = [x_min, x_max]
    r2 = [y_min, y_max]
    r3 = [z_min,z_max]
    X,Y = np.meshgrid(r1,r2)
    ax.plot_surface(X,Y,z_min,alpha=0.3)
    ax.plot_surface(X,Y,z_max,alpha=0.3)
    X,Z = np.meshgrid(r1,r3)
    ax.plot_surface(X,y_min,Z,alpha=0.3)
    ax.plot_surface(X,y_max,Z,alpha=0.3)
    Y,Z = np.meshgrid(r2,r3)
    ax.plot_surface(x_min,Y,Z,alpha=0.3)
    ax.plot_surface(x_max,Y,Z,alpha=0.3)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.view_init(0,0)
    ax.grid()
    plt.show()

def usage() :
    print "[Usage] : ./kdtree.py -d DIM -n NR -u UB --rect-min='YYY' --rect-max='ZZZ' -p y"

def check_option(parser, opt) :
    if opt.dim<=1 or opt.dim>=4 :
        parser.error('-d shoud be 2 or 3')
        sys.exit(2)
    if opt.plot != 'y' and opt.plot != 'n' :
        parser.error("-p should be 'y' or 'n'")
        sys.exit(2)

def demo2d(opt) :
    nr_pts = opt.nr_points
    upper_bound = opt.upper_bound
    points = create_random_points(upper_bound,nr_pts,opt.dim)
    kdtree = KdTree(points,dim=2)
    kdtree.build()
    maxes = map(int,opt.maxes.split(','))
    mins = map(int,opt.mins.split(','))
    res = kdtree.query(maxes,mins)
    logging.debug('Query result {0}'.format(res))
    if opt.plot == 'y' :
        plot_points(points,maxes,mins)

def demo3d(opt) :
    nr_pts = opt.nr_points
    upper_bound = opt.upper_bound
    points = create_random_points(upper_bound,nr_pts,opt.dim)
    kdtree = KdTree(points,dim=3)
    kdtree.build()
    maxes = map(int,opt.maxes.split(','))
    mins = map(int,opt.mins.split(','))
    res = kdtree.query(maxes,mins)
    logging.debug('Query result {0}'.format(res))
    if opt.plot == 'y' :
        plot_points3d(points,maxes,mins,res)

def main() :
    usage()
    parser = OptionParser()
    parser.add_option('-d','--dim',dest='dim',
        type='int',help='Dimension of points',metavar='DIM')
    parser.add_option('-n','--nr-points',dest='nr_points',
        type='int',help='Number of points',metavar='PTS')
    parser.add_option('-u','--upper-bound',dest='upper_bound',
        type='int',help='upper bound of each axis',metavar='UB')
    parser.add_option('-m','--rect-max',dest='maxes',
        type='string',help='max of hyperrectangle (as list)',metavar='[RX]')
    parser.add_option('-x','--rect-min',dest='mins',
        type='string',help='min of hyperrectangle (as list)',metavar='[RM]')
    parser.add_option('-p','--plot', dest='plot', help='plot the points')
    option,args = parser.parse_args()
    check_option(parser,option)
    if option.dim == 2 :
        demo2d(option)
    elif option.dim == 3 :
        demo3d(option)

if __name__ == '__main__':
    main()
