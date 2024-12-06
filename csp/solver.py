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

        # kukne že ak ohodnotím premennú, tak stále bude platiť, že zvyšok riešnia sa
        # dá ohodnotiť tak AKA v ich doménach sú premenné tak, že sa to dá ohodnotiť
        
        set_vars = []
        while csp.unchecked:
            constraint = csp.unchecked.popleft()
            
            # remove assigned vars
            to_remove = []

            for i, var in enumerate(constraint.vars):
                if csp.value[var] == True:
                    constraint.count -= 1 # TODO
                    to_remove.append(var)
                if csp.value[var] == False:
                    to_remove.append(var)
            for var in to_remove:
                constraint.vars.remove(var)
                
            if len(constraint.vars) < constraint.count or constraint.count < 0:
                csp.reset(set_vars)
                return None
            
            elif constraint.count == 0:
                for var in constraint.vars:
                    set_vars.append(var)
                    csp.set(var, False)
            
            elif len(constraint.vars) == constraint.count:
                for var in constraint.vars:
                    set_vars.append(var)
                    csp.set(var, True)
        
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
                    
                if self.is_done(csp): return [csp.value[var] for var in range(csp.num_vars)]
                
                inferences = inferences if inferences is not None else []
            csp.reset(inferences + [heuristic_var])
            
        return None

        # vráti mi NEJAKÉ ohodnotenie, teda to môže byť aj také,
        # ktoré je niesprávne, pretože je nevynútené
        

    def infer_var(self, csp: BooleanCSP) -> int:
        """
        Infer a value for a single variable
        if possible using a proof by contradiction.
        If any variable is inferred, return it; otherwise return -1.
        """
        # Your implementation goes here.
        
        for var in range(csp.num_vars):
            csp.set(var, True)
            if self.solve(csp) is None:
                csp.set(var, False)
                return var
            csp.set(var, False)
            if self.solve(csp) is None:
                csp.set(var, True)
                return var
            csp.reset([var])
        return -1
