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

    # shows = os.listdir(subtitle_folder) # get show folder names in subtitles/

    # shows_and_lemmas = {}  #initializing empty dictionaries for storage

    # for series in shows:  # begin parsing all series in subtitle folder
    #     print(f'Show currently parsing: {series}')

    #     path = f'{subtitle_folder}/{series}'
    #     show_subs_files = os.listdir(path) # get names for each sub file

    #     cleaned_lines = []  #initialize list for storage of lines

    #     for file in show_subs_files:  # allows reading any number of sub files
    #         with open(f'{path}/{file}', 'r', encoding='UTF-8') as f:  
    #         # extracting the lines from the subititle file
    #             file_text = f.readlines()

    #         # unpack and add to total list of cleaned lines
    #         cleaned_lines = cleaned_lines + [*clean_lines(file_text)]

    #     # getting dict of lemmas present and how many times they occur
    #     lemma_counts = lemmas_counter(cleaned_lines, tagger)

    #     # linking the lemmas and counts to the show name in a dict format
    #     shows_and_lemmas[series] = lemma_counts

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
    # shows_90 = round(num_shows*0.9)  # rounds to the nearest integer
    # lemmas_90per_shows = [lemma for lemma, occurs in 
    #                     lemma_show_occurence.items() if occurs >= shows_90]
    
    # shows_80 = round(num_shows*0.8)
    # lemmas_80per_shows = [lemma for lemma, occurs in \
    #                     lemma_show_occurence.items() if occurs >= shows_80]


    # # Exporting/saving files to the provided save directory
    # print('')
    # print(f'Generating core vocab lists in {save_dir}/\n')

    # # Check if save directory exists, create if doesn't
    # if not os.path.exists(save_dir):
    #     print('Save folder not found, creating...\n')
    #     os.makedirs(save_dir)

    # print('')
    # print('Beginning write of shows-and-lemmas dictionary...')
    # # Writing shows_and_lemmas dictionary to file
    # with open(f'{save_dir}/shows-and-lemmas-dict.txt', 'w', encoding='UTF-8') as \
    #     save_file:
    #     save_file.write(json.dumps(shows_and_lemmas))

    # print('File write complete\n')

    # print('Beginning write of lemmas-all-shows list...')
    # # writing lemmas lists to file
    # with open(f'{save_dir}/lemmas-in-all-shows.txt', 'w', encoding='UTF-8') as \
    #     save_file:
    #     for i in lemmas_all_shows:
    #         save_file.write(i + '\n')
    
    # print('File write complete\n')

    # print('Beginning write of lemmas-90per-shows list...')
    # with open(f'{save_dir}/lemmas-in-90per-shows.txt', 'w', encoding='UTF-8') as \
    #     save_file:
    #     for i in lemmas_90per_shows:
    #         save_file.write(i + '\n')
    
    # print('File write complete\n')

    # print('')
    # print('Beginning write of lemmas-80per-shows list...')
    # with open(f'{save_dir}/lemmas-in-80per-shows.txt', 'w', encoding='UTF-8') as \
    #     save_file:
    #     for i in lemmas_80per_shows:
    #         save_file.write(i + '\n')

    # print('File write complete\n')

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