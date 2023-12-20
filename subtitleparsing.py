"""
Script for defining functions for isolating lines from the subtitle files and
extracting lemmas and parts of speech from the sentences.
Also functions for counting frequency and occurence
"""
import re  # for regular expression searching
import os  #for scanning files in the given directory


def create_lemma_database(subtitle_folder, tagger):
    """
    Create a dictionary containing the name of the show as the key and the set of lemmas
    present as the value.

    Parameters:
    ---
    subtitle_folder: str - name of folder containing shows and their subtitles
    for parsing/analyzing

    tagger: fugashi tagger object - object generated via fugashi.Tagger() or from fugashi import Tagger


    Returns:
    ---
    shows_and_lemmas: dict - dictionary with show names as keys, with values as the set of lemmas present
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

        # Convert the list of lines to list of lemmas
        lemma_list = []
        for sentence in cleaned_lines:
            lemmas = lemma_extract(sentence, tagger)
            for lemma in lemmas:
                lemma_list.append(lemma)

        # reduce down to unique set
        lemma_set = set(lemma_list)

        # Add lemma set and show name to output dict
        shows_and_lemmas[series] = lemma_set


    return shows_and_lemmas


def lemma_extract(text, tagger):
    """
    Short function for returning a list of words and a list of the lemmas
    """
    words = tagger(text)

    lemma_list = []
    for word in words:
        lemma_list.append(word.feature.lemma)

    return lemma_list


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
