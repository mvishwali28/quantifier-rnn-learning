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

import numpy as np
import gc


#####################################
# Defining the class of Quantifiers #
#####################################
class Quantifier1(object):

    # 4 chars: A∩B, A\B, B\A, M \ (A∩B)
    num_chars = 4
    # chars = one-hot encoding
    chars = np.identity(num_chars)
    # zero char for padding
    zero_char = np.zeros(num_chars)

    # name the characters, for readability
    AB = chars[0]
    AnotB = chars[1]
    BnotA = chars[2]
    neither = chars[3]

    T = (1, 0)
    F = (0, 1)

    def __init__(self, name, cons=None, fn=None):

        if fn is None:
            raise ValueError("supply a function for verifying a quantifier!")

        if cons is None:
            raise ValueError("is the quantifier conservative?")

        self._name = name
        self._cons = cons
        self._verify = fn

    def __call__(self, seq):
        return self._verify(seq)


#################################################
# Defining quantifiers and evaluation functions #
#################################################
# Conservative quantifiers
# All As are Bs
def all_ver(seq):
    """
    Verifies whether all As are also Bs.
    :param seq: a sequence of elements of R^4
    :return: Quantifier1.T iff the number of Quantifier1.AnotBs is 0
    """

    for item in seq:
        if np.array_equal(item, Quantifier1.AnotB):
            return Quantifier1.F
    return Quantifier1.T



# Not all As are Bs
def notall_ver(seq):
    """
    Verifies whether there are As that are not Bs
    :param seq: a sequence of elements of R^4
    :return: Quantifier1.T iff the number of Quantifier1.AnotBs in seq not 0
    """

    if all_ver(seq) == Quantifier1.F:
        return Quantifier1.T
    return Quantifier1.F



# Most As are Bs
def most_ver(seq):
    """
    Verifies whether  at least half of the As are also Bs
    :param seq: a sequence of elements of R^4
    :return: Quantifier1.T iff Quantifier1.AnotBs is not more than Quantifier1.AB / 2
    """

    num_AnotB = 0
    num_AB = 0
    for item in seq:
        if np.array_equal(item, Quantifier1.AnotB):
            num_AnotB += 1
        elif np.array_equal(item, Quantifier1.AB):
            num_AB += 1
    if num_AB > num_AnotB:
        return Quantifier1.T
    else:
        return Quantifier1.F



# Some As are Bs
def some_ver(seq):
    """
    Verifies whether some As are Bs
    :param seq: a sequence of elements of R^4
    :return: Quantifier1.T iff the number of Quantifier1.AB is not 0
    """

    for item in seq:
        if np.array_equal(item, Quantifier1.AB):
            return Quantifier1.T
    return Quantifier1.F



# No As are Bs
def none_ver(seq):
    """
    Verifies whether no As are Bs.
    :param seq: a sequence of elements of R^4
    :return: Quantifier1.T iff the number of Quantifier1.AB is 0.
    """

    if some_ver(seq) == Quantifier1.F:
        return Quantifier1.T
    return Quantifier1.F




# Non-conservative quantifiers
# Equal AB
def equal_number_ver(seq):
    """
    Verifies if the number of As equals the number of Bs.
    :param seq: sequence of elements of R^4
    :return: Quantifier.T iff the number of Quantifier.AnotBs is
             the same as the number of Quanitifer.BnotAs
    """

    num_AnotB, num_BnotA = 0, 0
    for item in seq:
        if np.array_equal(item, Quantifier1.AnotB):
            num_AnotB += 1
        elif np.array_equal(item, Quantifier1.BnotA):
            num_BnotA += 1

    if num_AnotB == num_BnotA:
        return Quantifier1.T
    return Quantifier1.F



# Non-equal AB
def nonequal_number_ver(seq):
    """
    Verifies if the number of As does not equal the number of Bs.
    :param seq: sequence of elements of R^4
    :return: Quantifier.T iff the number of Quantifier.AnotBs is
             not the same as the number of Quanitifer.BnotAs
    """
    if equal_number_ver(seq) == Quantifier1.F:
        return Quantifier1.T
    return Quantifier1.F



# More A than B
def more_ver(seq):
    """
    Verifies if the number of As is more than the number of Bs.
    :param seq: sequence of elements of R^4
    :return: Quantifier.T iff the number of Quantifier.AnotBs is
             bigger than the number of Quanitifer.BnotAs
    """
    num_AnotB, num_BnotA = 0, 0
    for item in seq:
        if np.array_equal(item, Quantifier1.AnotB):
            num_AnotB += 1
        elif np.array_equal(item, Quantifier1.BnotA):
            num_BnotA += 1

    if num_AnotB > num_BnotA:
        return Quantifier1.T
    return Quantifier1.F



# Less A than B
def less_ver(seq):
    """
    Verifies if the number of As is less than the number of Bs.
    :param seq: sequence of elements of R^4
    :return: Quantifier.T iff the number of Quantifier.AnotBs is
             smaller than the number of Quanitifer.BnotAs
    """
    num_AnotB, num_BnotA = 0, 0
    for item in seq:
        if np.array_equal(item, Quantifier1.AnotB):
            num_AnotB += 1
        elif np.array_equal(item, Quantifier1.BnotA):
            num_BnotA += 1

    if num_AnotB < num_BnotA:
        return Quantifier1.T
    return Quantifier1.F



# No more A than B
def no_more_ver(seq):
    """
    Verifies if the number of As is no more than the number of Bs.
    :param seq: sequence of elements of R^4
    :return: Quantifier.T iff the number of Quantifier.AnotBs is not
             bigger than the number of Quanitifer.BnotAs
    """
    if more_ver(seq) == Quantifier1.F:
        return Quantifier1.T
    return Quantifier1.F



def get_all_quantifiers_1_1():
    """Returns: a list of all Quantifiers that have been created so far.
    """
    all = Quantifier1("all",cons=True, fn=all_ver) #Testing quantifier
    not_all = Quantifier1("not_all", cons=True, fn=notall_ver)
    most = Quantifier1("most", cons=True, fn=most_ver)
    some = Quantifier1("some", cons=True, fn=some_ver)
    none = Quantifier1("none", cons=True, fn=none_ver)
    equal_number = Quantifier1("equal_number", cons=False, fn=equal_number_ver)  #Testing quantifier
    non_equal_number = Quantifier1("nonequal_number", cons=False, fn=nonequal_number_ver)
    more = Quantifier1("more_A_than_B", cons=False, fn=more_ver)
    less = Quantifier1("less_A_than_B", cons=False, fn=less_ver)
    no_more = Quantifier1("no_more_A_than_B", cons=False, fn=no_more_ver)
    t = [all,not_all,most,some,none,equal_number,non_equal_number,more,less,no_more]
    # print([i._name for i in t if isinstance(i,Quantifier1)])
    return [i for i in t if isinstance(i,Quantifier1)]
    # return [quant for quant in gc.get_object()
    #         if isinstance(quant, Quantifier1)]
