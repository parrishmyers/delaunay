import numpy
import numpy.random
import unittest

from delaunay import *

class TestDTMethods(unittest.TestCase):
    def test_feq(self):
        half_err = THRESHOLD / 2.0
        full_err = THRESHOLD
        a = 4.0
        b1 = a + half_err
        b2 = a - half_err
        b3 = a + full_err
        b4 = a - full_err
        b5 = a + full_err + half_err
        b6 = a - full_err - half_err

        self.assertTrue( fequal(a, b1) )
        self.assertTrue( fequal(a, b2) )
        self.assertTrue( fequal(a, b3) )
        self.assertFalse( fequal(a, b4) )
        self.assertFalse( fequal(a, b5) )
        self.assertFalse( fequal(a, b6) )
    
    def test_vertex(self):
        p1 = Vertex(1.0, 2.0)
        p2 = Vertex(1.0, 2.0)
        p3 = Vertex(2.0, 3.0)

        self.assertTrue(p1 == p2)
        self.assertFalse(p1 == p3)
    
    def test_area_of_triangle(self):
        a = Vertex( 1.0, 2.0)
        b = Vertex(10.0, 2.0)
        c = Vertex( 1.0, 5.0)
        area = area_of_triangle(a, b, c)
        self.assertTrue( fequal(area, 13.5) )


class TestAreaError(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def error_in_area(self, a, b, c):
        area = area_of_triangle(a, b, c)

        a1 = Vertex(a.x+THRESHOLD, a.y)
        b1 = Vertex(b.x, b.y)
        c1 = Vertex(c.x, c.y)

        dAx = area_of_triangle(a1, b1, c1) - area

        a2 = Vertex(a.x, a.y)
        b2 = Vertex(b.x+THRESHOLD, b.y)
        c2 = Vertex(c.x, c.y)

        dBx = area_of_triangle(a2, b2, c2) - area

        a3 = Vertex(a.x, a.y)
        b3 = Vertex(b.x, b.y)
        c3 = Vertex(c.x+THRESHOLD, c.y)

        dCx = area_of_triangle(a3, b3, c3) - area

        a4 = Vertex(a.x, a.y+THRESHOLD)
        b4 = Vertex(b.x, b.y)
        c4 = Vertex(c.x, c.y)

        dAy = area_of_triangle(a4, b4, c4) - area

        a5 = Vertex(a.x, a.y)
        b5 = Vertex(b.x, b.y+THRESHOLD)
        c5 = Vertex(c.x, c.y)

        dBy = area_of_triangle(a5, b5, c5) - area

        a6 = Vertex(a.x, a.y)
        b6 = Vertex(b.x, b.y)
        c6 = Vertex(c.x, c.y+THRESHOLD)

        dCy = area_of_triangle(a6, b6, c6) - area

        da = numpy.sqrt( dAx ** 2 
                    + dBx ** 2
                    + dCx ** 2
                    + dAy ** 2
                    + dBy ** 2
                    + dCy ** 2
                    )
        return da

    def test_simple(self):
        e = []
        for i in range(0, 10000):
            x = [0.0, 0.0, 0.0]
            y = [0.0, 0.0, 0.0]
            for j in range(0,3):
                x[j] = numpy.random.uniform(-1000.0, 1000.0,)
                y[j] = numpy.random.uniform(-1000.0, 1000.0)
            a = Vertex(x[0], y[0])
            b = Vertex(x[1], y[1])
            c = Vertex(x[2], y[2])
            e.append(self.error_in_area(a, b, c))
        a = numpy.array(e)
        self.assertTrue(a.mean() < AREA_THRESHOLD)


class TestDTTriAdj(unittest.TestCase):
    def setUp(self):
        self.p1 = Vertex(0.9, 3.3)
        self.p2 = Vertex(2.1, 5.0)
        self.p3 = Vertex(2.1, 1.0)
        self.p4 = Vertex(4.7, 3.3)
        self.p5 = Vertex(7.0, 5.0)
        self.p6 = Vertex(6.9, 1.0)

    def tearDown(self):
        pass
    
    def test_simple(self):
        t1 = Triangle(self.p1, self.p2, self.p3)
        t2 = Triangle(self.p2, self.p3, self.p4)
        t3 = Triangle(self.p4, self.p5, self.p6)
        self.assertTrue( t1.is_adjacent(t2) )
        self.assertFalse( t1.is_adjacent(t3) )
        self.assertFalse( t2.is_adjacent(t3) )
    
    def test_01(self):
        t1 = Triangle(self.p2, self.p3, self.p1)
        t2 = Triangle(self.p2, self.p3, self.p4)
        self.assertTrue( t1.is_adjacent(t2) )

    def test_02(self):
        t1 = Triangle(self.p2, self.p3, self.p1)
        t2 = Triangle(self.p2, self.p4, self.p3)
        self.assertTrue( t1.is_adjacent(t2) )

    def test_03(self):
        t1 = Triangle(self.p2, self.p1, self.p3)
        t2 = Triangle(self.p2, self.p3, self.p4)
        self.assertTrue( t1.is_adjacent(t2) )

    def test_04(self):
        t1 = Triangle(self.p2, self.p1, self.p3)
        t2 = Triangle(self.p2, self.p4, self.p3)
        self.assertTrue( t1.is_adjacent(t2) )

    def test_05(self):
        t1 = Triangle(self.p2, self.p3, self.p1)
        t2 = Triangle(self.p3, self.p2, self.p4)
        self.assertTrue( t1.is_adjacent(t2) )

    def test_06(self):
        t1 = Triangle(self.p2, self.p3, self.p1)
        t2 = Triangle(self.p4, self.p2, self.p3)
        self.assertTrue( t1.is_adjacent(t2) )

    def test_07(self):
        t1 = Triangle(self.p2, self.p1, self.p3)
        t2 = Triangle(self.p3, self.p2, self.p4)
        self.assertTrue( t1.is_adjacent(t2) )

    def test_08(self):
        t1 = Triangle(self.p2, self.p1, self.p3)
        t2 = Triangle(self.p4, self.p2, self.p3)
        self.assertTrue( t1.is_adjacent(t2) )

    def test_09(self):
        t1 = Triangle(self.p2, self.p3, self.p1)
        t2 = Triangle(self.p3, self.p4, self.p2)
        self.assertTrue( t1.is_adjacent(t2) )

    def test_10(self):
        t1 = Triangle(self.p2, self.p3, self.p1)
        t2 = Triangle(self.p4, self.p3, self.p2)
        self.assertTrue( t1.is_adjacent(t2) )

    def test_11(self):
        t1 = Triangle(self.p2, self.p1, self.p3)
        t2 = Triangle(self.p3, self.p4, self.p2)
        self.assertTrue( t1.is_adjacent(t2) )

    def test_12(self):
        t1 = Triangle(self.p2, self.p1, self.p3)
        t2 = Triangle(self.p4, self.p3, self.p2)
        self.assertTrue( t1.is_adjacent(t2) )

    def test_13(self):
        t1 = Triangle(self.p1, self.p2, self.p3)
        t2 = Triangle(self.p2, self.p3, self.p4)
        self.assertTrue( t1.is_adjacent(t2) )

    def test_14(self):
        t1 = Triangle(self.p1, self.p2, self.p3)
        t2 = Triangle(self.p2, self.p4, self.p3)
        self.assertTrue( t1.is_adjacent(t2) )

    def test_15(self):
        t1 = Triangle(self.p1, self.p2, self.p3)
        t2 = Triangle(self.p3, self.p2, self.p4)
        self.assertTrue( t1.is_adjacent(t2) )

    def test_16(self):
        t1 = Triangle(self.p1, self.p2, self.p3)
        t2 = Triangle(self.p4, self.p2, self.p3)
        self.assertTrue( t1.is_adjacent(t2) )

    def test_17(self):
        t1 = Triangle(self.p1, self.p2, self.p3)
        t2 = Triangle(self.p3, self.p4, self.p2)
        self.assertTrue( t1.is_adjacent(t2) )

    def test_18(self):
        t1 = Triangle(self.p1, self.p2, self.p3)
        t2 = Triangle(self.p4, self.p3, self.p2)
        self.assertTrue( t1.is_adjacent(t2) )

class TestPoints(unittest.TestCase):
    def setUp(self):
        self.p = []
        self.p.append(Vertex(-3.0, -3.0))
        self.p.append(Vertex( 1.0, -2.0))
        self.p.append(Vertex(-1.0, -0.5))
        self.p.append(Vertex( 1.0,  0.5))
        self.p.append(Vertex(-2.0,  1.5))

    def tearDown(self):
        pass
    
    def test_add_vertex(self):
        pts = Points()
        p = Vertex(1.0,1.0)
        pts.add_point(p)
        self.assertTrue(p == pts[0])
    
    def test_add_xy(self):
        x = -1.1
        y =  3.2
        p = Vertex(x, y)
        pts = Points()
        pts.add_point(x, y)
        self.assertTrue(p == pts[0])

    def test_highest(self):
        pts = Points()
        for p in self.p:
            pts.add_point(p)
            self.assertTrue(pts.highest() == p)
    
    def test_permute(self):
        pts = Points()
        for p in self.p:
            pts.add_point(p)
        pts.permute()
        self.assertTrue(pts.highest() == self.p[-1])
        self.assertTrue(pts[0] == self.p[-1])

class TestDAG(unittest.TestCase):
    def setUp(self):
        self.pts = Points()
        self.pts.add_point(-2.5,  1.0)
        self.pts.add_point( 0.0,  4.0)
        self.pts.add_point( 2.0,  3.0)
        self.pts.add_point( 3.0,  0.0)
        self.pts.add_point( 2.8, -2.0)
        self.pts.permute()

    def tearDown(self):
        pass
    
    def test_01(self):
        p = Vertex(0.0, 4.0)
        self.assertTrue(p == self.pts.highest())
    
    def test_02(self):
        dag = DAG(self.pts)
        for p in self.pts:
            t = dag.find_triangle_containing(p)
            self.assertTrue(t != None)
    
if __name__ == '__main__':
    unittest.main()
