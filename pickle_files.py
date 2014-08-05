# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 12:40:07 2014

@author: tsalo
"""

import pickle
import inspect
import os

code_dir = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))

headers = {"EP_AX": ["Subject", "Group", "ExperimentName", "Session", "Age",
                     "Handedness", "Sex", "Block", "Cue.RT", "Cue.ACC",
                     "Probe.RT", "Probe.ACC", "TrialType", "Cue.OnsetTime",
                     "Probe.OnsetTime", "Cue", "SessionDate"],
           "EP2_AX": ["Subject", "Group", "Session", "Age", "ExperimentName",
                      "Handedness", "Sex", "BlockNum", "Cue.RT", "Cue.ACC",
                      "Probe.RT", "Probe.ACC", "TrialType", "Cue.OnsetTime",
                      "Probe.OnsetTime", "CueStim[Block]", "SessionDate"],
           "PACT_AX": ["Subject", "Group", "ExperimentName", "Session", "Age",
                       "Handedness", "Sex", "BlockList", "Cue.RT", "Cue.ACC",
                       "Probe.RT", "Probe.ACC", "TrialType", "Cue.OnsetTime",
                       "Probe.OnsetTime", "Cue", "SessionDate"],
           "EP2_ICET": ["Subject", "BlockNum", "ExperimentName", "TrialNum",
                        "Probe.ACC", "IsSame", "CueStim[Block]",
                        "TrialType", "Cue.OnsetTime", "Probe.OnsetTime",
                        "Probe.RT", "Feedback", "Feedback.OnsetTime"],
           }

replace_dict = {".edat": {"Experiment": "ExperimentName",
                          "BlockList.Cycle": "Block",
                          },
                ".edat2": {"Experiment": "ExperimentName",
                           "CueStim": "CueStim[Block]",
                           "ProbeStim": "ProbeStim[Block]",
                           }
                }

# Could this just be headers with the word "Block"?
fill_block = ["BlockList", "EndBlock"]

with open(code_dir + "/headers.pickle", "w") as file_:
    pickle.dump([headers, replace_dict, fill_block], file_)
