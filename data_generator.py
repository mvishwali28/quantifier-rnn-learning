import tensorflow as tf
import quantifiers_exp_1_2

quants = quantifiers_exp_1_2.get_all_quantifiers_1_2()
def cons_vs_noncons(quants):
    conservative_quantifiers = ['all',
                                'not_all',
                                'most_AB',
                                'most_not_AB',
                                'exactly_half_AB']
    nonconservative_quantifiers = ['only',
                                   'not_only',
                                   'most_BA',
                                   'most_not_BA',
                                   'exactly_half_BA']
    cons = [i for i in quants if i._name in conservative_quantifiers]
    noncons = [i for i in quants if i._name in nonconservative_quantifiers]
    return cons,noncons

cons,noncons = cons_vs_noncons(quants)
