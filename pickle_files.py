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
           "FAST_RISE_IE": ["CNTRACSID", "SessionDate", "SessionTime", "Trial",
                            "LeftStim", "RightStim", "StimuliACC",
                            "StimuliCRESP", "StimuliOnsetTime", "StimuliRESP",
                            "StimuliRT", "Stimulus"],
           "FAST_RISE_IR": ["CNTRACSID", "SessionDate", "SessionTime",
                            "Stimulus", "StimType", "StimuliAACC",
                            "StimuliACRESP", "StimuliAOnsetTime",
                            "StimuliARESP", "StimuliART", "StimuliBACC",
                            "StimuliBCRESP", "StimuliBOnsetTime",
                            "StimuliBRESP", "StimuliBRT"],
           "FAST_RISE_AR": ["CNTRACSID", "SessionDate", "SessionTime", "Trial",
                            "LeftStim", "RightStim", "StimuliACC",
                            "StimuliCRESP", "StimuliOnsetTime", "StimuliRESP",
                            "StimuliRT", "Stimulus", "TrialType"],
           }

merge_cols = {"FAST_RISE_IE": [],
              "FAST_RISE_IR": [["ItemsA", "ItemsB"]],
              "FAST_RISE_AR": [],
              "EP2_AX": [],
              "EP2_ICET": [],
              "EP_AX": [],
              "PACT_AX": [],
              }

merge_col_names = {"FAST_RISE_IE": [],
                   "FAST_RISE_IR": ["Trial"],
                   "FAST_RISE_AR": [],
                   "EP2_AX": [],
                   "EP2_ICET": [],
                   "EP_AX": [],
                   "PACT_AX": [],
                   }

null_cols = {"FAST_RISE_IE": ["LeftStim"],
             "FAST_RISE_IR": ["StimType"],
             "FAST_RISE_AR": ["TrialType"],
             "EP2_AX": ["Probe.ACC"],
             }

# Could probably benefit from task specific replacements, considering how many
# RISE requires.
replace_dict = {"FAST_RISE_IE": {".edat2": {"Trial": "BadTrial",
                                            "EncodingList.Sample": "Trial",
                                            "Stimuli.RESP": "StimuliRESP",
                                            "Stimuli.RT": "StimuliRT",
                                            "Stimuli.ACC": "StimuliACC",
                                            "Stimuli.CRESP": "StimuliCRESP",
                                            "Stimuli.OnsetTime": "StimuliOnsetTime",
                                            },
                                 },
                "FAST_RISE_IR": {".edat2": {"StimuliA.RT": "StimuliART",
                                            "StimuliB.RT": "StimuliBRT",
                                            "StimuliA.RESP": "StimuliARESP",
                                            "StimuliB.RESP": "StimuliBRESP",
                                            "StimuliA.CRESP": "StimuliACRESP",
                                            "StimuliB.CRESP": "StimuliBCRESP",
                                            "StimuliA.ACC": "StimuliAACC",
                                            "StimuliB.ACC": "StimuliBACC",
                                            "StimuliA.OnsetTime": "StimuliAOnsetTime",
                                            "StimuliB.OnsetTime": "StimuliBOnsetTime",
                                            },
                                 },
                "FAST_RISE_AR": {".edat2": {"EncodingList": "Trial",
                                            "Stimuli.RESP": "StimuliRESP",
                                            "Stimuli.RT": "StimuliRT",
                                            "Stimuli.ACC": "StimuliACC",
                                            "Stimuli.CRESP": "StimuliCRESP",
                                            "Stimuli.OnsetTime": "StimuliOnsetTime",
                                            },
                                 },
                "EP2_AX": {".edat": {"Experiment": "ExperimentName",
                                     "BlockList.Cycle": "Block",
                                     },
                           ".edat2": {"Experiment": "ExperimentName",
                                      "CueStim": "CueStim[Block]",
                                      "ProbeStim": "ProbeStim[Block]",
                                      },
                           },
                }

# Could this just be headers with the word "Block"?
fill_block = ["BlockList", "EndBlock"]

with open(code_dir + "/headers.pickle", "w") as file_:
    pickle.dump([headers, replace_dict, fill_block, merge_cols,
                 merge_col_names, null_cols], file_)
