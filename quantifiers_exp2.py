# -*- coding: utf-8 -*-
"""
Author: Ildikó Emese Szabó
based on script by Shane Steinert-Threlkeld

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

q = []


#####################################
# Defining the class of Quantifiers #
#####################################
class Quantifier2(object):

    T = (1, 0)
    F = (0, 1)

    def __init__(self, name, cons=None, fn=None):

        if fn is None:
            raise ValueError("Supply a function for verifying a quantifier!")

        if cons==None:
            raise ValueError("Is the quantifier conservative?")

        self._name = name
        self._cons = cons
        self._verify = fn

    def __call__(self, seq):
        return self._verify(seq)




#################################################
# Defining quantifiers and evaluation functions #
#################################################
# Conservative quantifiers
## Even A nonB
def evenAnonB_ver(lst):
    """
    Verifies whether the number of As (arg1) that are not Bs (arg2) is even.
    :param lst: a list of: a sequence of elements of R^4 (seq),
                digit (A: 1-4), digit (B: 1-4)
    :return: Quantifier2.T iff the number of As and not Bs is even
    """
    seq = lst[0]
    arg1 = lst[1]
    arg2 = lst[2]
    num_AnotB = 0

    for item in seq:
        if item[arg1 - 1] == 1 and item[arg2 - 1] == 0:
            num_AnotB += 1
    if num_AnotB % 2 == 0:
        return Quantifier2.T
    else:
        return Quantifier2.F

evenAnonB = Quantifier2("even_AnonB", cons=True, fn=evenAnonB_ver),
q.append(evenAnonB)


## Odd A nonBs
def oddAnonB_ver(lst):
    """
    Verifies whether the number of As (arg1) that are not Bs (arg2) is odd.
    :param lst: a list of: a sequence of elements of R^4 (seq),
                digit (A: 1-4), digit (B: 1-4)
    :return: Quantifier2.T iff the number of As and not Bs is not even
    """

    if evenAnonB_ver(lst) == Quantifier2.F:
        return Quantifier2.T
    return Quantifier2.F

oddAnonB = Quantifier2("odd_AnonB", cons=True, fn=oddAnonB_ver)
q.append(oddAnonB)


## Prime A nonBs
def primeAnonB_ver(lst):
    """
    Verifies whether the number of As (arg1) that are not Bs (arg2) is prime (for numbers under 20).
    :param lst: a list of: a sequence of elements of R^4 (seq),
                digit (A: 1-4), digit (B: 1-4)
    :return: Quantifier2.T iff the number of As and not Bs is prime
    """
    seq = lst[0]
    arg1 = lst[1]
    arg2 = lst[2]
    num_AnotB = 0
    primes = [2,3,5,7,11,13,17,19]

    for item in seq:
        if item[arg1 - 1] == 1 and item[arg2 - 1] == 0:
            num_AnotB += 1
    if num_AnotB in primes:
        return Quantifier2.T
    else:
        return Quantifier2.F

primeAnonB = Quantifier2("prime_AnonB", cons=True, fn=primeAnonB_ver)
q.append(primeAnonB)


## Non-prime A nonBs
def nonprimeAnonB_ver(lst):
    """
    Verifies whether the number of As (arg1) that are not Bs (arg2) is not prime (for numbers under 20).
    :param lst: a list of: a sequence of elements of R^4 (seq),
                digit (A: 1-4), digit (B: 1-4)
    :return: Quantifier2.T iff the number of As and not Bs is not prime
    """

    if primeAnonB_ver(lst) == Quantifier2.F:
        return Quantifier2.T
    return Quantifier2.F

nonprimeAnonB = Quantifier2("nonprime_AnonB", cons=True, fn=nonprimeAnonB_ver)
q.append(nonprimeAnonB)


## But for 3 A, B
def butfor3AnonB_ver(lst):
    """
    Verifies whether the number of As (arg1) that are not Bs (arg2) is 3.
    :param lst: a list of: a sequence of elements of R^4 (seq),
                digit (A: 1-4), digit (B: 1-4)
    :return: Quantifier2.T iff the number of As and not Bs is exactly 3s
    """
    seq = lst[0]
    arg1 = lst[1]
    arg2 = lst[2]
    num_AnotB = 0

    for item in seq:
        if item[arg1 - 1] == 1 and item[arg2 - 1] == 0:
            num_AnotB += 1
    if num_AnotB == 3:
        return Quantifier2.T
    return Quantifier2.F

butfor3AnonB = Quantifier2("but_for_3_AnonB", cons=True, fn=butfor3AnonB_ver)
q.append(butfor3AnonB)



# Non-conservative quantifiers
## Equal AB
def equal_number_ver(lst):
    """
    Verifies if the number of As (arg1) equals the number of 
    Bs (arg2) that are not As.
    :param lst: a list of: a sequence of elements of R^4 (seq),
                digit (A: 1-4), digit (B: 1-4)
    :return: Quantifier2.T iff the number of As equals
             the number of Bs that are not As
    """
    seq = lst[0]
    arg1 = lst[1]
    arg2 = lst[2]
    num_A, num_BnotA = 0, 0

    for item in seq:
        if item[arg1 - 1] == 1:
            num_A += 1
        if item[arg1 - 1] == 0 and item[arg2 - 1] == 1:
            num_BnotA += 1

    if num_A == num_BnotA:
        return Quantifier2.T
    return Quantifier2.F

equal_number = Quantifier2("equal_number", cons=False, fn=equal_number_ver)
q.append(equal_number)


## Non-equal AB
def nonequal_number_ver(lst):
    """
    Verifies if the number of As (arg1) does not equal the number of 
    Bs (arg2) that are not As.
    :param lst: a list of: a sequence of elements of R^4 (seq),
                digit (A: 1-4), digit (B: 1-4)
    :return: Quantifier2.T iff the number of As is
             not the same as the number of Bs that are not As
    """
    if equal_number_ver(lst) == Quantifier2.F:
        return Quantifier2.T
    return Quantifier2.F

non_equal_number = Quantifier2("nonequal_number", cons=False, fn=nonequal_number_ver)
q.append(non_equal_number)


## More A than B
def more_ver(lst):
    """
    Verifies if the number of As is more than the number of Bs.
    :param lst: a list of: a sequence of elements of R^4 (seq),
                digit (A: 1-4), digit (B: 1-4)
    :return: Quantifier2.T iff the number of As that are not Bs is larger than
             the number of Bs that are not As
    """
    seq = lst[0]
    arg1 = lst[1]
    arg2 = lst[2]
    num_AnotB, num_BnotA = 0, 0

    for item in seq:
        if item[arg1 - 1] == 1 and item[arg2 - 1] == 0:
            num_AnotB += 1
        if item[arg1 - 1] == 0 and item[arg2 - 1] == 1:
            num_BnotA += 1

    if num_AnotB > num_BnotA:
        return Quantifier2.T
    return Quantifier2.F

more = Quantifier2("more_A_than_B", cons=False, fn=more_ver)
q.append(more)


## Less A than B
def less_ver(lst):
    """
    Verifies if the number of As is less than the number of Bs.
    :param lst: a list of: a sequence of elements of R^4 (seq),
                digit (A: 1-4), digit (B: 1-4)
    :return: Quantifier2.T iff the number of As that are not Bs is smaller than
             the number of Bs that are not As
    """
    seq = lst[0]
    arg1 = lst[1]
    arg2 = lst[2]
    num_AnotB, num_BnotA = 0, 0

    for item in seq:
        if item[arg1 - 1] == 1 and item[arg2 - 1] == 0:
            num_AnotB += 1
        if item[arg1 - 1] == 0 and item[arg2 - 1] == 1:
            num_BnotA += 1

    if num_AnotB < num_BnotA:
        return Quantifier2.T
    return Quantifier2.F

less = Quantifier2("less_A_than_B", cons=False, fn=less_ver)
q.append(less)


## No more A than B
def no_more_ver(lst):
    """
    Verifies if the number of As is no more than the number of Bs.
    :param lst: a list of: a sequence of elements of R^4 (seq),
                digit (A: 1-4), digit (B: 1-4)
    :return: Quantifier2.T iff the number of As that are not Bs is not
             bigger than the number of Bs that are not As
    """
    if more_ver(lst) == Quantifier2.F:
        return Quantifier2.T
    return Quantifier2.F

no_more = Quantifier2("no_more_A_than_B", cons=False, fn=no_more_ver)
q.append(no_more)


def get_all_quantifiers():
    """
    Returns: a list of all Quantifier2-s that have been created so far.
    """
    print([i._name for i in q if isinstance(i,Quantifier2)])
    return [i for i in q if isinstance(i,Quantifier2)]


def get_all_cons_quantifiers():
    """
    Returns: a list of all conservative Quantifier2-s
    that have been created so far.
    """
    print([i._name for i in q if (isinstance(i, Quantifier2) and i.cons)])
    return [i for i in q if (isinstance(i, Quantifier2) and i.cons)]


def get_all_noncons_quantifiers():
    """
    Returns: a list of all non-conservative Quantifier2-s
    that have been created so far.
    """
    print([i._name for i in q if (isinstance(i, Quantifier2) and not i.cons)])
    return [i for i in q if (isinstance(i, Quantifier2) and not i.cons)]
