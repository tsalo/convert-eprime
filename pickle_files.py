# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 12:40:07 2014
Writes out pickle file with a number of dictionaries used by convert_eprime.py.
All of your task-specific information goes here.
@author: tsalo
"""

import pickle
import inspect
import os

code_dir = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))

# Specific columns to pull. Outputted rcsvs (reduced csv files) will only
# contain these columns.
headers = {
    "EP_AX": ["Subject", "Group", "ExperimentName", "Session", "Age",
              "Handedness", "Sex", "Block", "Cue.RT", "Cue.ACC",
              "Probe.RT", "Probe.ACC", "TrialType", "Cue.OnsetTime",
              "Probe.OnsetTime", "Cue", "SessionDate"],
    "EP_Stroop": ["Subject", "Session", "Group", "Block", "Trial",
                  "CellLabel", "StroopStimulus.ACC", "StroopStimulus.OnsetTime",
                  "StroopStimulus.RT"],
    "bEP_AX": ["Subject", "Group", "ExperimentName", "Session", "SessionDate",
               "Age", "Handedness", "Block", "Trial", "CueStim[Block]",
               "AllCue.ACC", "AllCue.OnsetTime", "AllCue.RT", "AllProbe",
               "AllProbe.ACC", "Cue.OnsetTime", "Probe.OnsetTime",
               "AllProbe.RT", "TrialType", "Running[Block]"],
    "EP2_AX": ["Subject", "Group", "Session", "Age", "ExperimentName",
               "Handedness", "Sex", "BlockNum", "Cue.RT", "Cue.ACC",
               "Probe.RT", "Probe.ACC", "TrialType", "Cue.OnsetTime",
               "Probe.OnsetTime", "CueStim[Block]", "SessionDate"],
    "bEP2_AX": ["CNTRACSID", "EP2ID", "EPCID", "EPPID", "UHRID", "Subject",
                "Group", "ExperimentName", "Session", "Age", "Handedness",
                "Sex", "Test", "Cue.RT", "Cue.ACC", "Probe.RT", "Probe.ACC",
                "TrialType", "Cue.OnsetTime", "Probe.OnsetTime",
                "SessionDate"],
    "PACT_AX": ["Subject", "Group", "ExperimentName", "Session", "Age",
                "Handedness", "Sex", "BlockList", "Cue.RT", "Cue.ACC",
                "Probe.RT", "Probe.ACC", "TrialType", "Cue.OnsetTime",
                "Probe.OnsetTime", "Cue", "SessionDate"],
    "EP2_ICET": ["Subject", "Group", "BlockNum", "ExperimentName", "TrialNum",
                 "Probe.ACC", "IsSame", "CueStim[Block]",
                 "TrialType", "Cue.OnsetTime", "Probe.OnsetTime",
                 "Probe.RT", "Feedback", "Feedback.OnsetTime", "SessionDate",
                 "DeadlineNeu", "DeadlineRew", "DeadlinePun", "ISIshort",
                 "Money", "Proce.ACC"],
    "AGG_ES": ["Subject", "Group", "BlockNum", "MiniBlockNum",
               "DisplayStim.RT", "DisplayStim.OnsetTime", "DisplayStim.ACC",
               "StartScan.OffsetTime", "TrialNum", "TrialType", "Emotion"],
    "AGG_CS": ["Subject", "Group", "CSD", "BlockNum", "Procedure[Trial]",
               "Procedure[SubTrial]", "Go.RT", "Go.OnsetTime", "Go.ACC",
               "TrialType", "DisplayRating.RESP", "Rateing[SubTrial]"],
    "AGG_Ek60": ["Subject", "Group", "Procedure[Trial]",
                 "StimSelect.RT[SubTrial]", "StimSelect.ACC[SubTrial]",
                 "StimResp[SubTrial]", "StimSelect.CRESP[SubTrial]"],
    "AGG_Reapp": ["Subject", "Group", "TrialNum", "Rating.RESP", "Rating.RT",
                  "Rating.OnsetTime", "StimulusImage.OnsetTime",
                  "Cue.OnsetTime", "PicValence", "BlockCue",
                  "TrialOrder.Sample"],
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
    "NICNAC_CUE": ["Crave.CRESP", "Crave.RESP", "Crave.RT",
                   "Crave.RTTime", "FixDur", "Procedure[Block]", "Duration",
                   "PicNeut1.OnsetTime", "PicSmok1.OnsetTime"],
    }

# Whether or not to remove NULL rows (rows where there are empty cells that
# have been filled with NULL).
remnulls = {
    "EP_AX": True,
    "EP_Stroop": True,
    "bEP_AX": True,
    "EP2_AX": True,
    "bEP2_AX": True,
    "PACT_AX": True,
    "EP2_ICET": True,
    "AGG_ES": False,
    "AGG_CS": False,
    "AGG_Ek60": True,
    "AGG_Reapp": True,
    "NICNAC_CUE": False,
    }

# Headers of columns to merge if they occur.
merge_cols = {"FAST_RISE_IE": [],
              "FAST_RISE_IR": [["ItemsA", "ItemsB"]],
              "FAST_RISE_AR": [],
              "EP2_AX": [],
              "EP2_ICET": [],
              "EP_AX": [],
              "PACT_AX": [],
              }

# Names of merged columns. Pairs up with merge_cols.
merge_col_names = {"FAST_RISE_IE": [],
                   "FAST_RISE_IR": ["Trial"],
                   "FAST_RISE_AR": [],
                   "EP2_AX": [],
                   "EP2_ICET": [],
                   "EP_AX": [],
                   "PACT_AX": [],
                   }

# Columns from which to define null rows (e.g. if the column has rows with NULL
# values, remove those rows from the matrix).
null_cols = {"FAST_RISE_IE": ["LeftStim"],
             "FAST_RISE_IR": ["StimType"],
             "FAST_RISE_AR": ["TrialType"],
             "EP2_AX": ["Probe.ACC"],
             }

# Column headers to replace (in order to match edat naming convention).
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

with open(os.path.join(code_dir, "headers.pickle"), "w") as fo:
    pickle.dump([headers, remnulls, replace_dict, fill_block, merge_cols,
                 merge_col_names, null_cols], fo)
