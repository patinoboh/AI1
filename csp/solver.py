#!/usr/bin/env python3
from csp_templates import Constraint, BooleanCSP
from typing import List, Optional


class Solver:
    """
    Class for solving BooleanCSP.

    Main methods:
    - forward_check
    - solve
    - infer_var
    """

    def __init__(self):
        # Your implementation goes here.
        self.csp = None

        pass

    def forward_check(self, csp: BooleanCSP) -> Optional[List[int]]:
        """
        Perform forward checking on any unchecked constraints in the given CSP.
        Return a list of variables (if any) whose values were inferred.
        If a contradiction is found, return None.
        """

        set_vars = []
        while csp.unchecked:
            constraint = csp.unchecked.popleft()
            
            # remove assigned vars
            to_remove = []
            
            trues = [var for var in constraint.vars if csp.value[var] == True]
            falses = [var for var in constraint.vars if csp.value[var] == False]
            nones = [var for var in constraint.vars if csp.value[var] is None]
            vars_c = len(constraint.vars)
                
            if len(trues) + len(nones) < constraint.count or constraint.count < 0 or len(trues) > constraint.count:
                csp.reset(set_vars)
                return None
            
            elif constraint.count == len(trues):
                for var in nones:
                    set_vars.append(var)
                    csp.set(var, False)

            elif constraint.count == len(trues) + len(nones):
                for var in nones:
                    set_vars.append(var)
                    csp.set(var, True)

            elif constraint.count == 0:
                for var in constraint.vars:
                    set_vars.append(var)
                    csp.set(var, False)
        
        return set_vars

    def is_done(self, csp: BooleanCSP):
        for constraint in csp.constraints:
            if any(csp.value[var] is None for var in constraint.vars):
                return False
            if sum([csp.value[var] for var in constraint.vars]) != constraint.count:
                return False
        return True
    
    def is_consistent(self, var, csp : BooleanCSP):
        for constraint in csp.var_constraints[var]:
            trues = [var for var in constraint.vars if csp.value[var] == True]
            falses = [var for var in constraint.vars if csp.value[var] == False]
            nones = [var for var in constraint.vars if csp.value[var] is None]
            
            if len(trues) > constraint.count:
                return False
            elif len(trues) + len(nones) < constraint.count:
                return False
        return True


    def solve(self, csp: BooleanCSP) -> Optional[List[int]]:
        """
        Find a solution to the given CSP using backtracking.
        The solution will not include values for variables
        that do not belong to any constraints.
        Return a list of variables whose values were inferred.
        If no solution is found, return None.
        """

        if self.is_done(csp): return [csp.value[var] for var in range(csp.num_vars)]
        
        unassigned = [var for var in range(csp.num_vars) if csp.value[var] is None]
        if not unassigned: return None

        heuristic_var = max(unassigned,key=lambda var: len(csp.var_constraints[var]))
    
        for value in [True, False]:
            inferences = []
            csp.set(heuristic_var, value)
            if self.is_consistent(heuristic_var, csp):
                inferences = self.forward_check(csp)
                if inferences is not None:
                    result = self.solve(csp)
                    if result is not None:
                        return result
                
                inferences = inferences if inferences is not None else []
            csp.reset(inferences + [heuristic_var])
            
        return None


    def infer_var(self, csp: BooleanCSP) -> int:
        """
        Infer a value for a single variable
        if possible using a proof by contradiction.
        If any variable is inferred, return it; otherwise return -1.
        """
        unassigned = [var for var in range(csp.num_vars) if csp.value[var] is None]
        unassigned.sort(key=lambda var: -len(csp.var_constraints[var]))
        
        values = csp.value.copy()

        for var in unassigned:
            csp.set(var, True)
            res = self.solve(csp)
            if res is None:
                csp.set(var, False)
                return var
            
            csp.value = values.copy()
            csp.set(var, False)
            res = self.solve(csp)
            if res is None:
                csp.set(var, True)
                return var
            
            csp.value = values.copy()
            csp.reset([var])
        return -1
