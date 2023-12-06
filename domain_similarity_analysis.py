"""
Functions for determining domain language of each show and quantifying
the similarity between two shows
"""

def domain_extract(show_lemmas_freq, core_vocab_list, min_occur_limit):
    """
    Extract the 'Domain Vocab' for the inputed show and return as a list

    Simply filtering out the 'core vocab list' and only counting words which
    occur 'min occur limit' or greater
    """
    # filtering out the lemmas in the core_vocab_list from the total lemmas 
    # in the show
    show_no_core = {}

    for lemma in show_lemmas_freq:
        if lemma in core_vocab_list:
            continue

        if show_lemmas_freq[lemma] < min_occur_limit:
            continue

        show_no_core[lemma] = show_lemmas_freq[lemma]

    return show_no_core