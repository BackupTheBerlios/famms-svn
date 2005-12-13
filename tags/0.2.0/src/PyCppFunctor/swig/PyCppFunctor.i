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
  This is a Python Callback version of the functor 'CppFunctor'. 
  You should replace the 'CppFunctor' base class with the name of your
  functor base class, and quite possible, re-implement this callback.
  This class serves best as a starting point for external legacy 
  code verification. Note to self: Have a pointer to a PyObj, 
  and make void operator() work with either a 'vector_value' or a 
  'scalar_grad'.
*/

%module PyCppFunctor
%{
#include <PyCppFunctor.h>
%}

class CppFunctor {
public:
   virtual double operator()(const double* point, int n, double t=0.0);
   virtual void operator()(const double* point,double* rets,int n,double t=0.0);
};

class PyCppFunctor: public CppFunctor {
public:
   int nsd;
   PyCppFunctor (int _nsd){ nsd = _nsd; }
   PyCppFunctor (){}
   PyObject* pyobj_value;
   PyObject* pyobj_grad;
   virtual double operator()(const double* point, double t=0.0);
   virtual double operator()(const double* point, int n, double t=0.0);
   virtual void operator()(const double* point,double* rets,int n,double t=0.0);
   virtual void operator()(const double* point,double* rets, double t=0.0);
   void attach(PyObject* value_);
   void attach(PyObject* value_, PyObject* grad_);
};

class testFunctor {
   public:
      CppFunctor* v;
      double (*fptr)(const double[], int, double);
      void init();
      void testscalar();
      void testvector();
};

// vim:ft=cpp:
