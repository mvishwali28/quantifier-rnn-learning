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
def most_AB_ver(seq):
    """
    Verifies whether  at least half of the As are also Bs
    :param seq: a sequence of elements of R^4
    :return: Quantifier1.T iff Quantifier1.AnotBs is not more than Quantifier1.AB / 2
    """
    num_AnotB, num_AB = 0, 0
    for item in seq:
        if np.array_equal(item, Quantifier1.AnotB):
            num_AnotB += 1
        elif np.array_equal(item, Quantifier1.AB):
            num_AB += 1

    if num_AB > num_AnotB:
        return Quantifier1.T
    else:
        return Quantifier1.F



# Not most
def most_nonAB_ver(seq):
    """
    Verifies whether most As don't B.
    :param seq: a sequence of elements of R^4
    :return: Quantifier1.T iff the number of Quantifier1.AnotBs
             is bigger than the number of Quantifier1.ABs
    """
    num_AnotB, num_AB = 0, 0
    for item in seq:
        if np.array_equal(item, Quantifier1.AnotB):
            num_AnotB += 1
        elif np.array_equal(item, Quantifier1.AB):
            num_AB += 1

    if num_AB < num_AnotB:
        return Quantifier1.T
    else:
        return Quantifier1.F



# Exactly half As are Bs
def exact_half_AB_ver(seq):
    """
    Verifies whether exactly half of As are Bs.
    :param seq: a sequence of elements of R^4
    :return: Quantifier1.T iff the number of Quantifier1.AnotB
             equals the number of Quantifier1.AB.
    """
    num_AnotB, num_AB = 0, 0
    for item in seq:
        if np.array_equal(item, Quantifier1.AnotB):
            num_AnotB += 1
        elif np.array_equal(item, Quantifier1.AB):
            num_AB += 1

    if num_AB == num_AnotB:
        return Quantifier1.T
    else:
        return Quantifier1.F




# Non-conservative quantifiers
# Only AB
def only_ver(seq):
    """
    Verifies if the only As are Bs.
    :param seq: sequence of elements of R^4
    :return: Quantifier1.T iff the number of Quantifier1.BnotAs is 0.
    """
    for item in seq:
        if np.array_equal(item, Quantifier1.BnotA):
            return Quantifier1.F
    return Quantifier1.T



# Not only AB
def notonly_ver(seq):
    """
    Verifies if some non-As are Bs.
    :param seq: sequence of elements of R^4
    :return: Quantifier1.T iff the number of Quantifier1.BnotA is not 0.
    """
    if only_ver(seq) == Quantifier1.F:
        return Quantifier1.T
    return Quantifier1.F



# Most BA
def most_BA_ver(seq):
    """
    Verifies if most Bs are As.
    :param seq: sequence of elements of R^4
    :return: Quantifier1.T iff the number of Quantifier1.ABs
             is bigger than the number of Quantifier1.BnotAs
    """
    num_BnotA, num_AB = 0, 0
    for item in seq:
        if np.array_equal(item, Quantifier1.BnotA):
            num_BnotA += 1
        elif np.array_equal(item, Quantifier1.AB):
            num_AB += 1

    if num_AB > num_BnotA:
        return Quantifier1.T
    else:
        return Quantifier1.F



# Most B not A
def most_nonBA_ver(seq):
    """
        Verifies if most Bs are non-As.
        :param seq: sequence of elements of R^4
        :return: Quantifier1.T iff the number of Quantifier1.BnotA
                 is bigger than the number of Quantifier1.AB.
        """
    num_BnotA, num_AB = 0, 0
    for item in seq:
        if np.array_equal(item, Quantifier1.BnotA):
            num_BnotA += 1
        elif np.array_equal(item, Quantifier1.AB):
            num_AB += 1

    if num_AB < num_BnotA:
        return Quantifier1.T
    else:
        return Quantifier1.F



# Exactly half BA
def exact_half_BA_ver(seq):
    """
    Verifies whether exactly half of Bs are As.
    :param seq: a sequence of elements of R^4
    :return: Quantifier1.T iff the number of Quantifier1.BnotA
             equals the number of Quantifier1.AB.
    """
    num_BnotA, num_AB = 0, 0
    for item in seq:
        if np.array_equal(item, Quantifier1.BnotA):
            num_BnotA += 1
        elif np.array_equal(item, Quantifier1.AB):
            num_AB += 1

    if num_AB == num_BnotA:
        return Quantifier1.T
    else:
        return Quantifier1.F



def get_all_quantifiers_1_2():
    """Returns: a list of all Quantifiers that have been created so far.
    """
    all = Quantifier1("all",cons=True, fn=all_ver) #Testing quantifier
    not_all = Quantifier1("not_all", cons=True, fn=notall_ver)
    most_AB = Quantifier1("most_AB", cons=True, fn=most_AB_ver)
    most_not_AB = Quantifier1("most_not_AB", cons=True, fn=most_nonAB_ver())
    exactly_half_AB = Quantifier1("exactly_half_AB", cons=True, fn=exact_half_AB_ver)
    only = Quantifier1("only", cons=False, fn=only_ver) #Testing quantifier
    not_only = Quantifier1("not_only", cons=False, fn=notonly_ver)
    most_BA = Quantifier1("most_BA", cons=False, fn=most_BA_ver)
    most_not_BA = Quantifier1("less_A_than_B", cons=False, fn=most_nonBA_ver)
    exactly_half_BA = Quantifier1("no_more_A_than_B", cons=False, fn=exact_half_BA_ver())
    t = [all, not_all, most_AB, most_not_AB, exactly_half_AB,
         only, not_only, most_BA, most_not_BA, exactly_half_BA]
    # print([i._name for i in t if isinstance(i,Quantifier1)])
    return [i for i in t if isinstance(i,Quantifier1)]
    # return [quant for quant in gc.get_object()
    #         if isinstance(quant, Quantifier1)]
