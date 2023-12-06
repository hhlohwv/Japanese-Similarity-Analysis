"""
Script for defining functions for isolating lines from the subtitle files and
extracting lemmas and parts of speech from the sentences.
Also functions for counting frequency and occurence
"""
import re  # for regular expression searching
import os  #for scanning files in the given directory
import json  # for writing and reading dictionary to file

# import matplotlib.pyplot as plt
# import matplotlib as mpl


def generate_core_vocab_list(subtitle_folder, tagger, save_dir):
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
    None, but writes the following to file:

    shows_and_lemmas: dict - dictionary with show names as keys, with values as
    another {key:value} set of {lemmas in the show:frequency of occurence}
    
    lemmas_all_shows: list - list of lemmas which appear at least once in every
    show in the subtitle folder
    
    lemmas_90per_shows: list - list of lemmas which appear in ~90% of the shows
    (rounded) in the subtitle folder

    lemmas_80per_shows: list - list of lemmas which appear in ~80% of the shows
    (rounded) in the subtitle folder
    """

    shows = os.listdir(subtitle_folder) # get show folder names in subtitles/

    shows_and_lemmas = {}  #initializing empty dictionaries for storage
    
    print('-- Beginning parse of shows in subtitle folder --\n')

    for series in shows:  # begin parsing all series in subtitle folder
        print(f'Show currently parsing: {series}')

        path = f'{subtitle_folder}/{series}'
        show_subs_files = os.listdir(path) # get names for each sub file

        cleaned_lines = []  #initialize list for storage of lines

        for file in show_subs_files:  # allows reading any number of sub files
            with open(f'{path}/{file}', 'r', encoding='UTF-8') as f:  
            # extracting the lines from the subititle file
                file_text = f.readlines()

            # unpack and add to total list of cleaned lines
            cleaned_lines = cleaned_lines + [*clean_lines(file_text)]

        # getting dict of lemmas present and how many times they occur
        lemma_counts = lemmas_counter(cleaned_lines, tagger)

        # linking the lemmas and counts to the show name in a dict format
        shows_and_lemmas[series] = lemma_counts

    lemma_show_occurence = shows_lemma_is_in(shows_and_lemmas)


    # extracting out the lemmas that occur in all, 90%, and 80% of the shows 
    # in the show list (i.e. value=# of shows and then percentages of that)
    num_shows = len(shows_and_lemmas)

    # Note: item() returns a list of the key,value pairs
    # using list comprehension to sort out lemmas with the value for all shows
    # courtesy of https://datagy.io/python-check-if-key-value-dictionary/
    lemmas_all_shows = [lemma for lemma, occurs in \
                        lemma_show_occurence.items() if occurs == num_shows]
    
    shows_90 = round(num_shows*0.9)  # rounds to the nearest integer
    lemmas_90per_shows = [lemma for lemma, occurs in 
                        lemma_show_occurence.items() if occurs >= shows_90]
    
    shows_80 = round(num_shows*0.8)
    lemmas_80per_shows = [lemma for lemma, occurs in \
                        lemma_show_occurence.items() if occurs >= shows_80]


    # Exporting/saving files to the provided save directory
    print('')
    print(f'Generating core vocab lists in {save_dir}/\n')

    # Check if save directory exists, create if doesn't
    if not os.path.exists(save_dir):
        print('Save folder not found, creating...\n')
        os.makedirs(save_dir)

    print('')
    print('Beginning write of shows-and-lemmas dictionary...')
    # Writing shows_and_lemmas dictionary to file
    with open(f'{save_dir}/shows-and-lemmas-dict.txt', 'w', encoding='UTF-8') as \
        save_file:
        save_file.write(json.dumps(shows_and_lemmas))

    print('File write complete\n')

    print('Beginning write of lemmas-all-shows list...')
    # writing lemmas lists to file
    with open(f'{save_dir}/lemmas-in-all-shows.txt', 'w', encoding='UTF-8') as \
        save_file:
        for i in lemmas_all_shows:
            save_file.write(i + '\n')
    
    print('File write complete\n')

    print('Beginning write of lemmas-90per-shows list...')
    with open(f'{save_dir}/lemmas-in-90per-shows.txt', 'w', encoding='UTF-8') as \
        save_file:
        for i in lemmas_90per_shows:
            save_file.write(i + '\n')
    
    print('File write complete\n')

    print('')
    print('Beginning write of lemmas-80per-shows list...')
    with open(f'{save_dir}/lemmas-in-80per-shows.txt', 'w', encoding='UTF-8') as \
        save_file:
        for i in lemmas_80per_shows:
            save_file.write(i + '\n')

    print('File write complete\n')

    return


def import_core_vocab_list(core_vocab_dir):
    """
    For importing dictionary and list files previously generated by the
    generate_core_vocab_list() function

    Parameters:
    ---
    core_vocab_list_dir: str - path to the folder containing the lemma and show
    dictionary and list outputs from 

   Returns:
    ---
    shows_and_lemmas: dict, dictionary with show names as keys, with values as
    another {key:value} set of {lemmas in the show:frequency of occurence}
    
    lemmas_all_shows: list, list of lemmas which appear at least once in every
    show in the subtitle folder
    
    lemmas_90per_shows: list, list of lemmas which appear in ~90% of the shows
    (rounded) in the subtitle folder

    lemmas_80per_shows: list, list of lemmas which appear in ~80% of the shows
    (rounded) in the subtitle folder

    """
    # Reading in files
    with open(f'{core_vocab_dir}/shows-and-lemmas-dict.txt', 'r', encoding='UTF-8') \
        as f:
        shows_and_lemmas = f.read()

    shows_and_lemmas = json.loads(shows_and_lemmas) # convert back to dict


    with open(f'{core_vocab_dir}/lemmas-in-all-shows.txt', 'r', encoding='UTF-8') \
        as f:
        lemmas_all_shows = f.read().splitlines() # gets rid of newlines

    with open(f'{core_vocab_dir}/lemmas-in-90per-shows.txt', 'r', encoding='UTF-8') \
        as f:
        lemmas_90per_shows = f.read().splitlines()

    with open(f'{core_vocab_dir}/lemmas-in-80per-shows.txt', 'r', encoding='UTF-8') \
        as f:
        lemmas_80per_shows = f.read().splitlines()


    return shows_and_lemmas, lemmas_all_shows, lemmas_90per_shows, \
        lemmas_80per_shows


def clean_lines(sub_file: list[str]) -> list[str]:
    """
    Take a subtitle file and strip away the subtitle numbers, text within 
    parentheses (so keeping only spoken dialogue), empty spaces, and time
    stamps.

    Only works for .srt subtitles at the moment.

    Parameters
    ---
    sub_file: list of strings, imported subtitle lines to clean

    Returns
    ---
    cleaned_lines: list of strings, subtitle file with only spoken lines.

    """
    cleaned_lines = []
    
    ignore_list = ['→','\ufeff','-->','♪～','～♪']  #list of symbols to scrub
    for line in sub_file:
        line = line.strip()  # removes beginning/end spaces and newlines

        #regex search/removal of text between parentheses
        line = re.sub(r'\（.*?\）', '', line)
        # replacing odd spaces
        line = re.sub(f'\u3000', ' ', line)

        if line.isdigit():  #checks if the line is a digit
            continue

        # if string is empty, move on
        if (not line):  # bool of empty line is false, not makes true
            continue

        if '\ufeff' in line:  #check for \ufeff string in line
            continue

        if '-->' in line:  # checking if arrow is in line, timestamps
            continue

        if line == '♪～' or line == '～♪':  # checking for music lines
            continue

        if line == ignore_list:
            continue

        cleaned_lines.append(line)  # appends line if passes above checks


    return cleaned_lines


def pos_counter(words: list, tagger) -> 'str':
    """
    Use Fugashi as the tokenizer and generate the part of speech (POS) for
    a given word

    Inputs are the words for analysis and tagger object generated via
    fugashi
    
    Output is a dict with parts of speech: occurence pairs
    """
    pos_counter = {}
    for lemma in words:
        # note: tagger(lemma) -> list of a single fugashi object
        # tagger(lemma)[0] ->  access that single list element
        # tagger(lemma)[0].feature.pos1 -> get POS of single fugashi object
        pos = tagger(lemma)[0].feature.pos1
        if pos not in pos_counter:
            pos_counter[pos] = 0

        pos_counter[pos] += 1

    return pos_counter


def lemmas_counter(cleaned_lines: list[str], tagger) -> dict:
    """
    Extract the individual words from the cleaned lines, generate and return a list
    that contains all the unique words and the number of times they occur in the
    cleaned lines.

    Parameters:
    ---
    cleaned lines: list[str] - a list where each element is the dialogue line

    tagger: fugashi tagger object - object created using fugashi.Tagger

    Returns:
    ---
    lemma_count: dict - dictionary object where the lemmas are the keys and values
    are the number of times they occur in the inputed cleaned lines
    """
    lemma_list = []

    for line in cleaned_lines:
        word_list = tagger(line)  # returns a list of the words in sentence
        for word in word_list:

            lemma = word.feature.lemma

            if lemma == None:  # need to filter None's before .isalpha()
                continue
            
            if not lemma.isalpha():  # removes non japanes character lemmas
                continue

            lemma_list.append(lemma)


    # calculate frequency of each lemma, utilizing a dictionary to 
    # help with counting
    lemma_counter = {}  # empty dictionary
    # 
    for word in lemma_list:
        if word not in lemma_counter:
            lemma_counter[word] = 0  # initializing the lemma if not present

        lemma_counter[word] += 1
    

    return lemma_counter


def pos_freq_eng_conv(pos_dict, tagger):
    """
    Purpose is to take a dictionary variable of parts of speech and their
    frequency and return an Eng translated list of the POS names and a list
    of their freq, sorted from most to least freq.
    """
    # Separating keys and values from dictionaries
    freq = list(pos_dict.values())
    bins = list(pos_dict.keys())

    # Resorting the order of the POS from most freq to least freq
    # copying from https://stackoverflow.com/questions/13668393/python-sorting-two-lists
    freq, bins = (list(x) for x in zip(*sorted(zip(freq, bins))))
    freq.reverse()
    bins.reverse()

    # Conversion of japanese grammar words into english
    conversion_key = {'連体詞': 'pre-noun adjectival',
                        '助詞': 'particle',
                        '動詞': 'verb',
                        '代名詞': 'pronoun',
                        '助動詞': 'bound auxiliary',
                        '名詞': 'noun',
                        '感動詞': 'interjection',
                        '形状詞': 'adjectival noun',
                        '接頭辞': 'prefix',
                        '形容詞': 'adjective',
                        '副詞': 'adverb',
                        '接尾辞': 'suffix',
                        '補助記号': 'supplementary symbol',
                        '接続詞': 'conjunction',
                        '記号': 'symbol' }

    bins_eng = []
    for i in bins:
        bins_eng.append(conversion_key[i])


    return bins_eng, freq


# def language_hist_occur(title: str, input_dict: dict, scale:str):
#     """
#     For plotting histograms of occurence freq for an inputed dictionary of
#     lemma:freq
#     """

#     lemma_counts = list(input_dict.values())

#     fig = plt.figure(figsize=(8,6))
#     plt.hist(lemma_counts, bins=100)
#     plt.title(f'Lemma Freq Occurence: {title}')
#     plt.xlabel('Occurence Frequency')
#     plt.ylabel('# of Lemmas with given frequency')
#     plt.yscale(scale)

#     # for copy-paste function
#     mpl.rcParams['savefig.format'] = 'svg' # sets copied file to .svg
#     mpl.rcParams['savefig.bbox'] = 'tight' # reduces white space around fig

#     fig.show()

#     return


# def language_hist_pos(title: str, input: dict, tagger, scale:str):
#     """
#     For plotting histograms of occurence for parts of speech of a word list
#     """
#     input_list = list(input.keys())

#     pos_dict = pos_counter(input_list, tagger)

#     pos_bins_eng, pos_freq = pos_freq_eng_conv(pos_dict, tagger)

#     fig = plt.figure(figsize=(8,7))
#     plt.bar(pos_bins_eng, pos_freq)
#     plt.title(f'POS Histogram for Lemmas: {title}')
#     plt.xlabel('Part of Speech')
#     plt.ylabel('Frequency')
#     plt.yscale(scale)

#     # Adjusting the rotation of the x labels and the whitespace around them
#     ax = plt.gca()  # access the figure axis
#     ax.set_xticklabels(labels=pos_bins_eng, rotation=80)
#     fig.subplots_adjust(bottom=0.3)

#     mpl.rcParams['savefig.format'] = 'svg' # sets copied file to .svg
#     mpl.rcParams['savefig.bbox'] = 'tight' # reduces white space around fig

#     fig.show()

#     return


def shows_lemma_is_in(shows_and_lemmas):
    # Making a dict that has lemmas as keys and values as # of shows that it
    # appears in
    lemma_show_occurence = {}

    for series in shows_and_lemmas:
        for lemma in shows_and_lemmas[series]:
            if lemma not in lemma_show_occurence:
                lemma_show_occurence[lemma] = 0  #adding if not present

            if lemma in shows_and_lemmas[series]:
                lemma_show_occurence[lemma] += 1 # increasing count if appears

    return lemma_show_occurence