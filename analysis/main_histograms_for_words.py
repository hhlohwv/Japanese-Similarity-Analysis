"""
Main script for plotting histograms for lemma frequencies, as well as parts of
speech for the lemmas present in a show.
"""

import matplotlib.pyplot as plt
import matplotlib as mpl  # for setting rcParams for addcopyfighandler package
import addcopyfighandler  #not called explicitly, adds ctrl+c feature to plots

from subtitleparsing import language_hist_occur, language_hist_pos
from domain_similarity_analysis import domain_extract