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


        # TODO Your implementation goes here.
        
        # kukne že ak ohodnotím premennú, tak stále bude platiť, že zvyšok riešnia sa
        # dá ohodnotiť tak AKA v ich doménach sú premenné tak, že sa to dá ohodnotiť
        
        set_vars = []
        while csp.unchecked:
            constraint = csp.unchecked.popleft()
            
            # remove assigned vars
            to_remove = []
            for i, var in enumerate(constraint.vars):
                if csp.value[var] == True:
                    constraint.count -= 1
                    to_remove.append(var)
                elif csp.value[var] == False:
                    to_remove.append(var)
            for var in to_remove:
                constraint.vars.remove(var)
                
            if constraint.count == 0:
                for var in constraint.vars:
                    set_vars.append(var)
                    csp.set(var, False)
            elif len(constraint.vars) == constraint.count:
                for var in constraint.vars:
                    set_vars.append(var)
                    csp.set(var, True)
            elif len(constraint.vars) < constraint.count or constraint.count < 0:
                for var in set_vars:
                    csp.reset(set_vars)
                return None
        
        return set_vars



        # keď zmením premennú, tak musím kuknúť všetky kde sa nachádzala (asi)
        # povyhadzujem také, ktoré nemajú riešenie
        # pozor že ak som kontroloval lokálnu konzistenciu čohosi a zmenil som tomu doménu,
        # tak mi to môže dojebať niečo iné, teda to musím pozrieť znova a preto queue lebo to potrebujem pozerať nanovo

        # v našom riešení sú premenné binárne a teda každá zmena domény = ohodnotenie

        # tu môžem normálne nastaviť hodnoty premennej pomocou set a tak
        # ale musím si to pamätať (lenže to si budem tak či tak aby som to mohol vrátiť)
        # nejaká metóda .reset s listom

        raise NotImplementedError

    def solve(self, csp: BooleanCSP) -> Optional[List[int]]:
        """
        Find a solution to the given CSP using backtracking.
        The solution will not include values for variables
        that do not belong to any constraints.
        Return a list of variables whose values were inferred.
        If no solution is found, return None.
        """
        # Your implementation goes here.

        # vráti mi NEJAKÉ ohodnotenie, teda to môže byť aj také,
        # ktoré je niesprávne, pretože je nevynútené
        
        # forward check tento problém NEMÁ

        raise NotImplementedError

    def infer_var(self, csp: BooleanCSP) -> int:
        """
        Infer a value for a single variable
        if possible using a proof by contradiction.
        If any variable is inferred, return it; otherwise return -1.
        """
        # Your implementation goes here.
        """
        foreach xi in vars:
            set(Xi, True)
            if solve(csp) is None:
                set(Xi, False)
            set(xi, False)
            if solve(csp) is None:
                set(Xi, True)
            # inak som tu a neviem o tej premennej nič
        """

        raise NotImplementedError
