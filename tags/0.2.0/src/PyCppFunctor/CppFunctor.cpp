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

#include <CppFunctor.h>
#include <stdio.h>

double CppFunctor:: operator()(const double point[], int n, double t) { 
   double r = 0.0;
   for (int i=0;i<n;i++) r += point[i]*point[i];
   return r;
}

void   CppFunctor:: operator()(const double point[],double rets[], int n, double t) {
   for (int i=0;i<n;i++) rets[i] = point[i]*point[i];
}

void testclass:: init() { 
   v=new(CppFunctor);
}

void testclass:: testscalar() {
   double point[] = {1.0,2.0};

//   typedef double(*ptr)(const double[], int, double);

//   fptr = v->getit();
//   ptr pt = v->getit();
//   (void*) v->getit();
   printf("%f \n", (*v)(point,2));
}

void testclass:: testvector() {
   double point[] = {1.0,2.0};
   double rets[2];
   int n=2;
   (*v)(point,rets,n);
   for (int i=0;i<n;i++) {
      printf("%f ",rets[i]);
   }
   printf("\n");
}

