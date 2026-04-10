"""
Functions for analyzing the contents of the lemma database
"""

def percentage_vocab_list(lemma_database, percentage):
    """
    Generate the list of core vocabulary by parsing through all the shows
    present in the inputed subtitle folder and write to file

    Parameters:
    ---
    subtitle_folder: str - name of folder containing shows and their subtitles
    for parsing/analyzing

    tagger: fugashi tagger object - object generated via fugashi.Tagger()

    save_dir: str - path to the folder where the generated core vocab lemma
    files are to be saved


    Returns:
    ---
    lemmas_XXper_shows: list - list of lemmas which appear in ~XX% of the shows
    (rounded) in the subtitle folder
    """
    lemma_show_occurence = shows_lemma_is_in(lemma_database)

    # extracting out the lemmas that occur in all, 90%, and 80% of the shows 
    # in the show list (i.e. value=# of shows and then percentages of that)
    num_shows = len(lemma_database.keys())

    # Note: item() returns a list of the key,value pairs
    # using list comprehension to sort out lemmas with the value for all shows
    # courtesy of https://datagy.io/python-check-if-key-value-dictionary/
    shows_per = round(num_shows * (percentage/100))
    lemmas_per_shows = [lemma for lemma, occurs in \
                        lemma_show_occurence.items() if (occurs >= shows_per and not None)]
    
    if None in lemmas_per_shows:  # strip out None if present in lists
        lemmas_per_shows.remove(None)

    return lemmas_per_shows


def shows_lemma_is_in(shows_and_lemmas):
    # Making a dict that has lemmas as keys and values as # of shows that it
    # appears in
    lemma_show_occurence = {}

    for series in shows_and_lemmas:
        for lemma in shows_and_lemmas[series]:
            if lemma == 'None':
                pass
            if lemma not in lemma_show_occurence:
                lemma_show_occurence[lemma] = 0  #adding if not present

            if lemma in shows_and_lemmas[series]:
                lemma_show_occurence[lemma] += 1 # increasing count if appears

    return lemma_show_occurence