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

#include "PyCppFunctor.h"
#include <stdio.h>

void PyCppFunctor:: attach(PyObject* value_) {
   pyobj_value = value_;       Py_INCREF(pyobj_value);
}
void PyCppFunctor:: attach(PyObject* value_, PyObject* grad_) {
   pyobj_value = value_;       Py_INCREF(pyobj_value);
   pyobj_grad = grad_;         Py_INCREF(pyobj_grad);
}

double PyCppFunctor:: operator()(const double* point, int n, double t) {	     
   PyObject* pt;
   PyObject* arglist;

   pt = PyTuple_New(n);
   for (int i=0; i<n; i++) {
      PyTuple_SetItem(pt, i, PyFloat_FromDouble((double)point[i]));
   }

   arglist = PyTuple_New(2);
   PyTuple_SetItem(arglist,0,pt);
   PyTuple_SetItem(arglist,1,PyFloat_FromDouble((double)t));

   double dres = 0.0;
   PyObject* result;
   result = PyEval_CallObject(pyobj_value,arglist);
   Py_DECREF(arglist);
   if (result) dres = PyFloat_AsDouble(result);
   Py_XDECREF(result);
   return dres;
} 

double PyCppFunctor:: operator()(const double* point, double t){
   double tmp = operator()(point, nsd, t);
   return tmp;
}

void PyCppFunctor:: operator()(const double* point, double* rets, int n, double t) {
   PyObject* pt;
   PyObject* arglist;

   pt = PyTuple_New(n);
   for (int i=0; i<n; i++)
      PyTuple_SetItem(pt, i, PyFloat_FromDouble((double)point[i]));

   arglist = PyTuple_New(2);
   PyTuple_SetItem(arglist,0,pt);
   PyTuple_SetItem(arglist,1,PyFloat_FromDouble((double)t));

   PyObject* result;
   result = PyEval_CallObject(pyobj_value,arglist);
   Py_DECREF(arglist);
   if (result) {// Build return vector
      int n = PyList_Size(result);
      for (int i=0; i<n;i++)
         rets[i] = PyFloat_AsDouble(PyList_GetItem(result,i));
   }
   // End result
   Py_XDECREF(result);
}

void PyCppFunctor:: operator()(const double* point, double* rets, double t){
   operator()(point, rets,nsd, t);
}

