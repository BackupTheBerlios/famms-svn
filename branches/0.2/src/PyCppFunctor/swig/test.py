def f(pt, time=0.0):
   s = 0.0
   for i in pt:
      s += i
   return s

from evalPt import *

t=testclass()
t.init()
t.testscalar()

t.testvector()

p = pyevalPt()
p.attach(f)
t.v=p
t.testscalar()
