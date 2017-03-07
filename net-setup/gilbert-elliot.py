#!/usr/bin/env python3

import sys
import helper
from helper import State
import time


config = helper.read_arguments(sys.argv)
helper.init_seed(config["seed"])

switch_state_dl = False
switch_state_ul = False
state_dl = State.GAP
state_ul = State.GAP

# Main loop of application
while True:

    if switch_state_dl:
        if state_dl == State.GAP:
            helper.set_loss_rate("veth2",
                                 config["qdisc_nr_dl"],
                                 config["loss_rate_dl"])
            state_dl = State.BURST

        elif state_dl == State.BURST:
            helper.set_loss_rate("veth2",
                                 config["qdisc_nr_dl"],
                                 0.0)
            state_dl = State.GAP

    if switch_state_ul:
        if state_ul == State.GAP:
            helper.set_loss_rate("veth3",
                                 config["qdisc_nr_ul"],
                                 config["loss_rate_ul"])
            state_ul = State.BURST

        elif state_ul == State.BURST:
            helper.set_loss_rate("veth3",
                                 config["qdisc_nr_ul"],
                                 0.0)
            state_ul = State.GAP

    time.sleep(1)
    switch_state_dl = \
        helper.switch_state(config["move_to_burst_dl"]) \
        if state_dl == State.GAP \
        else helper.switch_state(config["move_to_gap_dl"])
    switch_state_ul = \
        helper.switch_state(config["move_to_burst_ul"]) \
        if state_ul == State.GAP \
        else helper.switch_state(config["move_to_gap_ul"])
