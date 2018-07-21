from delaunay.util import *

class DAG:
    def __init__(self, points):
        p0 = points.highest()
        t1 = Triangle(p0, None, None)
        self._DAG = [t1]
    
    def __match_b_in_a(self, a, b):
        av = [-1, -1, -1]
        bv = [-1, -1, -1]
        for ai in range(0,3):
            for bi in range(0,3):
                ap = a.points[ai]
                bp = b.points[bi]
                if ap == bp:
                    av[ai] = bi
                    bv[bi] = ai
        p1 = -1
        p2 = -1
        c = []
        for i in range(0,3):
            if av[i] == -1:
                p1 = i
            else:
                c.append(i)
            if bv[i] == -1:
                p2 = i
            
        return c, p1, p2
    
    def __breadth_first_search(self, pt, t):
        if t == None:
            return None

        if is_pt_inside_triangle(pt, t):
            if t.is_leaf():
                return t
            else:
                for c in t.children:
                    res = self.__breadth_first_search(pt, c)
                    if res is not None:
                        return res
                return None
        else:
            return None

    # ##################################################################################
    # public functions
    # ##################################################################################

    def find_triangle_containing(self, p):
        root = self._DAG[0]
        return self.__breadth_first_search(p, root)
    
    def __split_on_edge(self, t1, p):
        pass

    def __split_on_interior(self, t1, p):
        t2 = Triangle(t1.a, t1.b, p)
        t3 = Triangle(t1.b, t1.c, p)
        t4 = Triangle(t1.c, t1.a, p)

        t1.add_child(t2)
        t1.add_child(t3)
        t1.add_child(t4)

        self._DAG.append(t2)
        self._DAG.append(t3)
        self._DAG.append(t4)
        
    def split(self, t1, p):
        if is_pt_on_edge(p, t1):
            self.__split_on_edge(t1, p)
        else:
            self.__split_on_interior(t1, p)
    
    def flip(self, t1, t2):
        c, p1, p2 = self.__match_b_in_a(t1, t2)
        
        t3 = Triangle(c[0], p1, p2)
        t4 = Triangle(c[1], p1, p2)
        
        t1.add_child(t3)
        t1.add_child(t4)

        t2.add_child(t3)
        t2.add_child(t4)

        self._DAG.append(t3)
        self._DAG.append(t4)

    
    