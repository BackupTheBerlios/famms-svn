#!/usr/bin/env python

__author__      = "Ola Skavhaug (skavhaug@simula.no)"
__date__        = "2003-12-01 -- 2005-11-18"
__copyright__   = "Copyright (c) 2003, 2004, 2005 Ola Skavhaug"
__license__     = "GNU LGPL Version 2"

"""SystemFamms: A library for applying the method of manufactured solutions to PDE simulaors
for coupled systems."""


from Famms import Famms
import Symbolic

class SystemFamms:
    """ Based on the mandatory constructor arguments nproblems and
    max_nsd, a coupled system of PDE simulators can be assigned to this class.
    Basically, SystemFamms handles the coupeling of the manufactured
    solutions in multi-physics simulators."""

    def __init__(self, nproblems, max_nsd, same_nsd=True, time=False, simtype="Python"):
        self.nproblems = nproblems
        self.same_nsd= same_nsd
        self.nsd_list = []
        self.v_names = "set_v_func"
        self.b_names = "set_b_func"
        self.t = None
        if time:
            self.t = Symbolic.Symbol('t')
        self.setMaxDimension(max_nsd)
        self.simtype = simtype

    def assignCallbackNames(self, v_names, b_names):
        """If not default function names for inserting the callbacks, set them
        here (as lists)"""
        self.v_names = v_names
        self.b_names = b_names

    def assign(self, sim_list, sol_list, PDE_list, nsds=None):
        """The system, in terms of three lists of simulators, solutions and
        functions defining the PDEs must be assigned by this function call"""
        self.assignSimulators(sim_list)
        self.assignSolutions(sol_list)
        self.assignPDEs(PDE_list)
        if not nsds:
            nsds = self.nsd
        self.assignDimensions(nsds)
        self.assignSpatialSymbols()
        self.prepare()

    def assignSimulators(self, sim_list):
        self.simulators = sim_list

    def assignSolutions(self, sol_list):
        self.solutions = sol_list

    def assignPDEs(self, PDE_list):
        self.PDE_list = PDE_list

    def assignDimensions(self, nsds):
        if isinstance(nsds,int):
            for i in range(self.nproblems):
                self.same_nsd = True
                self.nsd_list.append(nsds)
        else:
            self.nsd_list = nsds

    def assignSpatialSymbols(self):
        for i in xrange(len(self.solutions)):
            self.solutions[i].setSpatialSymbols(self.x[0:self.nsd_list[i]])

    def setMaxDimension(self, nsd):
        self.nsd = nsd
        self.x = []
        for i in range(nsd):
            symb = "x_%i" % i
            self.x.append(Symbolic.Symbol(symb))
 
    def prepare(self):
        self.famms_list = []
        f = self.famms_list
        for i in range(self.nproblems):
            f.append(Famms(nsd   = self.nsd_list[i],
                            time = self.t,
                            space_symbs = self.x[0:self.nsd_list[i]],
                            simtype = self.simtype))
            if type(self.v_names)==type([]) and type(self.b_names)==type([]):
                f[i].setCallBackNames(self.v_names[i], self.b_names[i])
            f[i].assign(solution  = self.solutions[i],
                         equation  = self.PDE_list[i],
                         simulator = self.simulators[i],
                         couple_list = self.solutions)
