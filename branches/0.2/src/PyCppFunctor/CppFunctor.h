#ifndef EVALPT_H_IS_INCLUDED
#define EVALPT_H_IS_INCLUDED

/*
  This file is part of Famms - Fully Automatic Method of Manufactured Solutions
  Copyright (C) 2003, 2004, 2005 Ola Skavhaug
  
  Famms is free software; you can redistribute it and/or
  modify it under the terms of the GNU Lesser General Public
  License as published by the Free Software Foundation; either
  version 2.1 of the License, or (at your option) any later version.
  
  Famms is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Lesser General Public License for more details.
  
  You should have received a copy of the GNU Lesser General Public
  License along with Famms; if not, write to the Free Software
  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/



/*
  Base class for functor that evaluates points and return eiter double vals
  or array of doubles. Hopefully, this resembles the functor used in your C++
  legacy simulator. If not, the pyval class needs to be redesigned to fit the
  functor style of use.
*/

class CppFunctor {
public:
   virtual double operator()(const double* point, int n, double t=0.0);
   virtual void operator()(const double* point,double* rets,int n,double t=0.0);
};

/*
Small test suite for functors. Python Callback sub-classes of CppFunctor can 
be used in place of 'CppFunctor' base class. E.g., in Python:
t = testclass()
p = pyCppFunctor()
t.v = p
t.testscalar() or t.testvector()
*/
class testclass {
   public:
      CppFunctor* v;
      double (*fptr)(const double[], int, double);

      void init();
      void testscalar();
      void testvector();
};

#endif
