#!/usr/bin/env python3

import subprocess
import random
import sys


def switch_state(probability):
    """
    Given a certain probability p (0 < p < 1), returns
    wether state should be switched or not.
    """
    value = random.random()

    if probability > random:
        return True
    return False


def init_seed(seed=0):
    """
    Initializes the random seed.
    """
    random.(a=seed)


def read_arguments(argv):
    """
    Extract arguments.
    """
    move_to_gap_dl = 1
    move_to_burst_dl = 0
    loss_ratio_dl = 0
    move_to_gap_dl = 1
    move_to_burst_dl = 0
    loss_ratio_dl = 0
    seed = 0

    for argument in argv:
        if "--loss-prob-move-to-gap-dl=" in argument:





init_seed
