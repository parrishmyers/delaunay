
# ###############################################################
#
# ###############################################################

THRESHOLD = 0.00001
AREA_THRESHOLD = 0.01

def fequal(x1, x2, threshold=THRESHOLD):
    d = x1 - x2
    if d < 0.0:
        d *= -1.0
    if threshold >= d:
        return True
    else:
        return False

def area_equal(a1, a2, threshold=AREA_THRESHOLD):
    return fequal(a1, a2, threshold)


# ###############################################################
#
# ###############################################################

class Vertex:
    _vertex = [0.0, 0.0]

    def __init__(self, x: float, y: float):
        self._vertex[0] = x
        self._vertex[1] = y
    
    @property
    def x(self):
        return self._vertex[0]
    
    @x.setter
    def x(self, value):
        self._vertex[0] = value
    
    @property
    def y(self):
        return self._vertex[1]
    
    @y.setter
    def y(self, value):
        self._vertex[1] = value
    
    def __eq__(self, b):
        result = True
        if not fequal(self.x, b.x):
            result = False
        if not fequal(self.y, b.y):
            result = False
        return result
    
    def is_higher_than(self, q: Vertex):
        if self.x < q.x and self.y >= q.y:
            return True
        else:
            return False

# ###############################################################
#
# ###############################################################

class Points:
    def __init__(self):
        self._order = []
        self._points = []
        self._i = 0

    def add_point(self, x, y):
        n = Vertex(x, y)
        if self._points:
            h = self._points[0]
            if n.x < h.x and n.y >= h.y:
                self._points[0] = n
                n = h
        self._points.append(n)

    def get_point(self, i):
        if self._order:
            return self._points[self._order[i]]
        else:
            return self._points[i]

    def permute(self):
        p = numpy.random.permutation(len(self._points))
        l = list(p)
        l.remove(0)
        l.insert(0,0)
        self._order = l

    def highest(self):
        return self.get_point(0)

    def __iter__(self):
        return iter(self)

    def next(self):
        if self._i >= len(self._points):
            raise StopIteration()
        
        i = self._i
        self._i += 1
        return self.get_point(i)


# ###############################################################
#
# ###############################################################

class DagNode:
    _children = None

    def if_leaf(self):
        if self._children is None:
            return True
        else:
            return False
    
    @property
    def children(self):
        return self._children

    def add_child(self, value: DagNode):
        if not issubclass(value, DagNode):
            raise ValueError()
            
        if self._children:
            self._children.append(value)
        else:
            self._children = [value]


# ###############################################################
#
# ###############################################################

def area_of_triangle(a,b,c):
    a = ( a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y) )/ 2.0
    if a < 0.0:
        return -a
    else:
        return a

def are_triangles_adjacent(t1,t2):
    result = False
    
    if   t1.a == t2.a and t1.b == t2.b:
        result = True
    elif t1.a == t2.a and t1.b == t2.c:
        result = True 
    elif t1.a == t2.a and t1.c == t2.b:
        result = True 
    elif t1.a == t2.a and t1.c == t2.c:
        result = True 
    
    elif t1.a == t2.b and t1.b == t2.a:
        result = True 
    elif t1.a == t2.b and t1.b == t2.c:
        result = True 
    elif t1.a == t2.b and t1.c == t2.a:
        result = True 
    elif t1.a == t2.b and t1.c == t2.c:
        result = True 
    
    elif t1.a == t2.c and t1.b == t2.a:
        result = True 
    elif t1.a == t2.c and t1.b == t2.b:
        result = True 
    elif t1.a == t2.c and t1.c == t2.a:
        result = True 
    elif t1.a == t2.c and t1.c == t2.b:
        result = True 
    
    elif t1.b == t2.a and t1.c == t2.b:
        result = True 
    elif t1.b == t2.a and t1.c == t2.c:
        result = True 

    elif t1.b == t2.b and t1.c == t2.a:
        result = True 
    elif t1.b == t2.b and t1.c == t2.c:
        result = True

    elif t1.b == t2.c and t1.c == t2.a:
        result = True 
    elif t1.b == t2.c and t1.c == t2.b:
        result = True
    
    else:
        result = False

    return result


# ###############################################################
#
# ###############################################################

class Triangle(DagNode):
    def __init__(self, a, b, c):
        self._points = [a, b, c]
    
    @property
    def a(self):
        return self._points[0]
    
    @property
    def b(self):
        return self._points[1]
    
    @property
    def c(self):
        return self._points[2]

    def area(self):
        a = area_of_triangle(self.a, self.b, self.c)
        if area_equal(a, 0.0):
            return 0.0
        else:
            return a
    
    def area_zero(self):
        a = area_of_triangle(self.a, self.b, self.c)
        if area_equal(a, 0.0):
            return True
        else:
            return False
    
    def is_adjacent(self, b):
        return are_triangles_adjacent(self, b)

# ###############################################################
#
# ###############################################################

def is_pt_inside_triangle(p, t):
    if t.b == None and t.c == None:
        # This is the first triangle that contains all points
        return True
    
    a = area_of_triangle(t.a, t.b, t.c)
    a1  = area_of_triangle(t.a, t.b, p)
    a1 += area_of_triangle(t.b, t.c, p)
    a1 += area_of_triangle(t.c, t.a, p)
    return fequal(a, a1)

def is_pt_inside_triangle2(p, t):
    x = p.x
    y = p.y

    x1 = t.a.x
    y1 = t.a.y
    x2 = t.b.x
    y2 = t.b.y
    x3 = t.c.x
    y3 = t.c.y

    denom = (x1 * (y2 - y3) + y1 * (x3 - x2) + x2 * y3 - y2 * x3)
    t1 = (x * (y3 - y1) + y * (x1 - x3) - x1 * y3 + y1 * x3) / denom
    t2 = (x * (y2 - y1) + y * (x1 - x2) - x1 * y2 + y1 * x2) / -denom

    if 0.0 <= t1 <= 1.0 and 0.0 <= t2 <= 1.0 and t1 + t2 <= 1.0:
        return True
    else:
        return False

# ###############################################################
#
# ###############################################################

def circle_for_points(a, b, c):
    x1 = a.x
    y1 = a.y
    x2 = b.x
    y2 = b.y
    x3 = c.x
    y3 = c.y

    X2 = (x2-x1)
    X3 = (x3-x1)
    Y2 = (y2-y1)
    Y3 = (y3-y1)
    
    alpha = X3 / X2
    
    bx2 = (x2+x1) * X2
    bx3 = (x3+x1) * X3
    by2 = (y2+y1) * Y2
    by3 = (y3+y1) * Y3
    
    h = 0.0
    k = 0.0
    r = 0.0
    
    k = bx3 + by3 - alpha * (bx2 + by2)
    k /= 2 * (Y3 - alpha * Y2)
    
    h = bx2 + by2 - 2 * k * Y2
    h /= 2 * X2
    
    r = math.sqrt( (x1 - h)*(x1 - h) + (y1 - k)*(y1 - k) )
    
    return h, k, r


def in_circle(t, pr):
    x, y, r = circle_for_points(t.points[0], t.points[1], t.points[2])
    x_diff = pr.x - x
    y_diff = pr.y - y
    dist = math.sqrt(x_diff**2 + y_diff**2)
    if dist <= r:
        return True
    else:
        return False
