#!/usr/bin/env python

__author__      = "Ola Skavhaug (skavhaug@simula.no)"
__date__        = "2003-12-01 -- 2006-09-14"
__copyright__   = "Copyright (c) 2003, 2004, 2005, 2006 Ola Skavhaug"
__license__     = "GNU LGPL Version 2"

"""Fully Automated Method of Manufactured Solutions

Usage: f=famms.famms(nsd=2, time=None, space_symbs=None, simtype='DP', **kwargs)

f.assign(equation=eq, solution=sol, simulator=sim)
where equation is a function defining the governing equation, solution is a
solution defined in GiNaC, and simulator is a PDE simulator.
By default, we assume that the simulator has the methods 
set_v_func(anaytical solution) and set_b_func (source) 
for inserting callbacks for evaluating the analytical solution (at the
boundaries and initial time) and the corresponding source term in the interior.
These names can be changed if the simulator uses another convention."""

from Symbolic import Symbol, Expr, grad
try: from DP import FieldFuncPython, FieldsFuncPython
except: pass
try: from Callback.PyCppFunctor import PyCppFunctor 
except: pass


class FammsError(BaseException):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class PyFunctor(object):
    """Python callback functor. The method 'attach' must be defined and accept
    the Famms methods _vValue, b_Value, and _vGrad as arguments.  Various
    methods for point evaluation could be added to this class, if needed in a
    spesific application."""

    def attach(self, *args):
        self.funcs = args

    def evalPt(self, point, time=0.0):
        return self.funcs[0](point, time)

    def evalGradPt(self, point, time=0.0):
        return self.funcs[1](point, time)

    def __call__(self, point, time=0.0):
        return self.evalPt(point, time)

class SimType(object):
    def __init__(self):
        self.type=None

    def getfunctors(self):
        return (None, None)

class DPSim(SimType):
    def __init__(self):
        self.type = "Diffpack Simulator"

    def getfunctors(self):
        return (FieldFuncPython, FieldsFuncPython)

class CppSim(SimType):
    def __init__(self):
        self.type = "C++ Simulator using functors"

    def getfunctors(self):
        return (PyCppFunctor, PyCppFunctor)

class PythonSim(SimType):
    def __init__(self):
        self.type = "Python Simulator"

    def getfunctors(self):
        return (PyFunctor, PyFunctor)

"""Factory method for selecting simulator type"""
def SimTypeFactory(type):
    if type == "DP":
        return DPSim()
    elif type == "Cpp":
        return CppSim()
    elif (type == "Fortran" or type == "Python"):
        return PythonSim()
    else:
        raise TypeError, "Unknown Simulator Type %s" % type

class Famms(object):
      
    """Fully Automatic Method of Manufactured Solutions
    Lightweight class for attaching a manufactured solution and the
    corresponding source terms to scalar or vector PDEs.
    """ 

    def __init__(self, nsd=2, time=None, space_symbs=None, simtype="Python", **kwargs):
        """Constructor. Arguments are: 
        * nsd (int=2) : The number of space dimensions for the PDE
        * time (symbol=None): The symbol for time
        * space_symbs (symbol=None): List of existing symbols.
        * simtype (string='Python'): The simulator type """
        if space_symbs:
            self.x = space_symbs
            self.n = len(space_symbs)
        else:
            self.x = []
            self.n = nsd
            for i in range(nsd):
                symb = "x_%i" % (i,)
                self.x.append(Symbol(symb))
        self.t = None
        if isinstance(time, Symbol):
            self.t = time
        elif time:
            self.t = Symbol('t')
        self.simtype = simtype
        self.simtype_obj = SimTypeFactory(simtype) 
        # Todo: Move the name of the attach methods for callbacks to SimType
        self.v_func_name = "set_v_func"
        self.b_func_name = "set_b_func"
        if kwargs: # Additional Python callbacks can be passed as keyword arguments
            self.extra_callbacks = kwargs
 
    def setCallBackNames(self, v_name, b_name):
        """If the simulator interface requires a non default function name for
        binding the functor callback, set these names here"""
        # Todo: update the v_func_name in self.simtype_obj 
        self.v_func_name = v_name
        self.b_func_name = b_name
 
    def assign(self, equation=None, solution=None, simulator=None, couple_list=None):
        """Based on equation and solution, build source term and send 
        the Python callbacks to the simulator.
        """
        if (not equation) or (not solution):
            raise FammsError, "You must at least specify the equation and the solution in assign()"
 
        solution.setSpatialSymbols(self.x)
        if not (couple_list):
        #    solution.set_spatial_symbs(self.x)
            couple_list = [solution]
        self.initMMS(equation, solution, couple_list)
        self.createCallbacks()
        if simulator:
            self.insertCallbacks(simulator)
            if self.__dict__.has_key('extra_callbacks'):
                self.insertExtraCallbacks(self, simulator, self.extra_callbacks)
        self.sim = simulator
 

    def insertExtraCallbacks(self, sim, extra_callbacks, type_='scalar'):
        """Insert Python functions as callbacks in the simulator. We assume that
        the simulator can set the Python callback using 'set_%s', where %s is the
        dictionary key for the Python function."""
        for k in extra_callbacks:
            exec("sim.set_%s(self._as_callback(extra_callbacks[k], type_=type_))" % k)
 
    def initMMS(self, F, v, couple_list):
        all_symbs = self.x[:]
        if self.t:
            all_symbs.append(self.t)
        self.F = F
        self.b = F(*couple_list).simplify()
        self.v = v
        self.v_grad = grad(self.v)
        self.v.initEval(all_symbs)
        self.b.initEval(all_symbs)
        self.v_grad.initEval(all_symbs)
 
    def createCallbacks(self):
        """Wrap the functions _value_v and _value_b in functors"""        
        if isinstance(self.v, Expr):
            type_ = 'scalar'
        else:
            type_ = 'vector' # Lazy assumption
        self.v_func = self._asCallback(self._vValue, self._vGrad, type_ = type_)
        self.b_func = self._asCallback(self._bValue, type_ = type_)

    def insertCallbacks(self, simulator):
        """Attach the callbacks to the simulator by calling the simulator
        methods v_func_name and b_func_name."""
        try:
            exec("simulator.%s(self.v_func)" % self.v_func_name)
            exec("simulator.%s(self.b_func)" % self.b_func_name)
        except:
            raise FammsError, "Could not attach functors (type %s) to the simulator using \ the method '%s' and '%s'" % (type(self.v_func_name), self.v_func_name, self.b_func_name)

    def getCallbacks(self):
        return (self.v_func, self. b_func)
 
    def _asCallback(self, *args, **kwargs):
        """ Convert the Python function objects to a Python callback. If using
        Famms with some exotic C++/Fortran or even Python simulator, extend this
        method fit the framework."""
        (functype, funcstype) = self.simtype_obj.getfunctors()
        if kwargs['type_'] == 'scalar':
            func = functype()
        else :
            func = funcstype()
        func.thisown = 0
        func.attach(*args)
        return func
 
    def _vValue(self, point, time):
        """This is the point eval of the analytical solution. Pass the point to
        the Symbolic.expression v, that returns float
        """
        try:
            retVal = self.v.eval(*(point+(time, )))
        except:
            raise FammsError, "Could not evaluate the analytical solution"
        return retVal 
 
    def _bValue(self, point, time):
        """This is the point eval of the source term. Pass the point to
        the symbolic.expr b, that returns float
        """
        try:
            retVal = self.b.eval(*(point+(time, )))
        except:
            raise FammsError, "Could not evaluate the source term"
        return retVal 
 
    def _vGrad(self, point, time):
        try:
            retVal = self.v_grad.eval(*(point+(time, )))
        except:
            raise FammsError, "Could not evaluate the gradient of the analytical solution"
        return retVal
