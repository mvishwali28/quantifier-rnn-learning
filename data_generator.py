import tensorflow as tf
import quantifiers_exp1

quants = quantifiers_exp1.get_all_quantifiers()
def cons_vs_noncons(quants):
    conservative_quantifiers = ['even_AnonB',
                                'odd_AnonB',
                                'prime_AnonB',
                                'nonprime_AnonB',
                                'but_for_3_AnonB']
    nonconservative_quantifiers = ['equal_number',
                                   'nonequal_number',
                                   'more_A_than_B',
                                   'less_A_than_B',
                                   'no_more_A_than_B']
    cons = [i for i in quants if i._name in conservative_quantifiers]
    noncons = [i for i in quants if i._name in nonconservative_quantifiers]
    return cons,noncons

cons,noncons = cons_vs_noncons(quants)
