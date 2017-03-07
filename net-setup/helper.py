#!/usr/bin/env python3

import subprocess
import random
import sys
import enum


class State(enum.Enum):
    GAP = 0
    BURST = 1


def switch_state(probability):
    """
    Given a certain probability p (0 < p < 1), returns
    wether state should be switched or not.
    """
    random_value = random.random()

    if probability > random_value:
        return True
    return False


def init_seed(seed=0):
    """
    Initializes the random seed.
    """
    random.seed(a=seed)


def read_arguments(argv):
    """
    Extract arguments.
    """
    argv = argv[1:]
    config = dict()

    config["move_to_gap_dl"] = 1.0
    config["move_to_burst_dl"] = 0.0
    config["loss_rate_dl"] = 0.0
    config["move_to_gap_ul"] = 1.0
    config["move_to_burst_ul"] = 0.0
    config["loss_rate_ul"] = 0.0
    config["seed"] = 0
    config["qdisc_nr_dl"] = 1
    config["qdisc_nr_ul"] = 1

    for argument in argv:
        if "--loss-prob-move-to-gap-dl=" in argument:
            config["move_to_gap_dl"] = \
                float(argument.replace("--loss-prob-move-to-gap-dl=", "")) /\
                100.0
        elif "--loss-prob-move-to-burst-dl=" in argument:
            config["move_to_burst_dl"] = \
                float(argument.replace("--loss-prob-move-to-burst-dl=", "")) /\
                100.0
        elif "--loss-rate-burst-dl=" in argument:
            config["loss_rate_dl"] = \
                float(argument.replace("--loss-rate-burst-dl=", "")) /\
                100.0
        elif "--loss-prob-move-to-gap-ul=" in argument:
            config["move_to_gap_ul"] = \
                    float(argument.replace(
                            "--loss-prob-move-to-gap-ul=", "")) /\
                    100.0
        elif "--loss-prob-move-to-burst-ul=" in argument:
            config["move_to_burst_ul"] = \
                float(argument.replace("--loss-prob-move-to-burst-ul=", "")) /\
                100.0
        elif "--loss-rate-burst-ul=" in argument:
            config["loss_rate_ul"] = \
                float(argument.replace("--loss-rate-burst-ul=", "")) /\
                100.0
        elif "--random-seed=" in argument:
            config["seed"] = int(argument.replace("--random-seed=", ""))
        elif "--qdisc-nr-dl=" in argument:
            config["qdisc_nr_dl"] = int(argument.replace("--qdisc-nr-dl=", ""))
        elif "--qdisc-nr-ul=" in argument:
            config["qdisc_nr_ul"] = int(argument.replace("--qdisc-nr-ul=", ""))
        else:
            sys.stderr.write("Incorrect argument: " + argument + "\n")
            sys.exit(1)

    return config


def set_loss_rate(interface, qdisc_nr, loss_rate):
    """
    Run command to set the config of qdiscs for up and down link.
    """
    if qdisc_nr > 1:
        subprocess.check_call(["tc",
                               "-s",
                               "qdisc",
                               "change",
                               "dev",
                               interface,
                               "parent",
                               str(qdisc_nr - 1) + ":0",
                               "handle",
                               str(qdisc_nr) + ":0",
                               "netem",
                               "loss",
                               str(loss_rate) + "%",
                               "limit",
                               str(250000)])
    elif qdisc_nr == 1:
        subprocess.check_call(["tc",
                               "-s",
                               "qdisc",
                               "change",
                               "dev",
                               "veth2",
                               "root",
                               "handle",
                               "1:0",
                               "netem",
                               "loss",
                               str(loss_rate) + "%",
                               "limit",
                               str(250000)])
    else:
        sys.stderr.write("Qdisc count can't be zero if loss is enabled!\n")
        sys.exit(2)
