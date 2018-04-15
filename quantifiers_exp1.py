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
# Even A nonB
def evenAnonB_ver(seq):
    """
    Verifies whether the number of As that are not Bs is even.
    :param seq: a sequence of elements of R^4
    :return: Quantifier1.T iff the number of Quantifier1.AnotBs in seq is even
    """

    num_AnotB = 0
    for item in seq:
        if np.array_equal(item, Quantifier1.AnotB):
            num_AnotB += 1
    if num_AnotB % 2 == 0:
        return Quantifier1.T
    else:
        return Quantifier1.F


evenAnonB = Quantifier1("even_AnonB", cons=True, fn=evenAnonB_ver),


# Odd A nonBs
def oddAnonB_ver(seq):
    """
    Verifies whether the number of As that are not Bs is odd.
    :param seq: a sequence of elements of R^4
    :return: Quantifier1.T iff the number of Quantifier1.AnotBs in seq is odd
    """

    if evenAnonB_ver(seq) == Quantifier1.F:
        return Quantifier1.T
    return Quantifier1.F


oddAnonB = Quantifier1("odd_AnonB", cons=True, fn=oddAnonB_ver)


# Prime A nonBs
def primeAnonB_ver(seq):
    """
    Verifies whether the number of As that are not Bs is prime (for numbers under 20).
    :param seq: a sequence of elements of R^4
    :return: Quantifier1.T iff the number of Quantifier1.AnotBs in seq is prime
    """

    num_AnotB = 0
    primes = [2, 3, 5, 7, 11, 13, 17, 19]
    for item in seq:
        if np.array_equal(item, Quantifier1.AnotB):
            num_AnotB += 1
    if num_AnotB in primes:
        return Quantifier1.T
    else:
        return Quantifier1.F


primeAnonB = Quantifier1("prime_AnonB", cons=True, fn=primeAnonB_ver)


# Non-prime A nonBs
def nonprimeAnonB_ver(seq):
    """
    Verifies whether the number of As that are not Bs is not prime (for numbers under 20).
    :param seq: a sequence of elements of R^4
    :return: Quantifier1.F iff the number of Quantifier1.AnotBs in seq is prime
    """

    if primeAnonB_ver(seq) == Quantifier1.F:
        return Quantifier1.T
    return Quantifier1.F


nonprimeAnonB = Quantifier1("nonprime_AnonB", cons=True, fn=nonprimeAnonB_ver)


# But for 3 A, B
def butfor3AnonB_ver(seq):
    """
    Verifies whether the number of As that are not Bs is 3.
    :param seq: a sequence of elements of R^4
    :return: Quantifier1.T iff the number of Quantifier1.AnotBs is 3
    """

    num_AnotB = 0
    for item in seq:
        if np.array_equal(item, Quantifier1.AnotB):
            num_AnotB += 1
    if num_AnotB == 3:
        return Quantifier1.T
    return Quantifier1.F


butfor3AnonB = Quantifier1("but_for_3_AnonB", cons=True, fn=butfor3AnonB_ver)


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


equal_number = Quantifier1("equal_number", cons=False, fn=equal_number_ver)


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


non_equal_number = Quantifier1("nonequal_number", cons=False, fn=nonequal_number_ver)


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


more = Quantifier1("more_A_than_B", cons=False, fn=more_ver)


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


less = Quantifier1("less_A_than_B", cons=False, fn=less_ver)


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


no_more = Quantifier1("no_more_A_than_B", cons=False, fn=no_more_ver)
