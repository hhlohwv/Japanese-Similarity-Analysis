"""
Main function to test calling and running of the other auxilary functions
and module scripts in this folder.
"""
import matplotlib.pyplot as plt
import matplotlib as mpl  # for setting rcParams for addcopyfighandler package
import addcopyfighandler  #not called explicitly, adds ctrl+c feature to plots

import numpy as np

import fugashi  # Mecab wrapper for tokenizer function

# Functions for creating and importing the core vocab list from subtitle shows
from subtitleparsing import generate_core_vocab_list, import_core_vocab_list, shows_lemma_is_in
from subtitleparsing import language_hist_occur, language_hist_pos

from domain_similarity_analysis import domain_extract


def main():

    # Generating list of core vocabulary from all shows in sub folder
    subtitle_folder = 'subtitles'

    tagger = fugashi.Tagger() # creating tagger object for later use

    save_dir = 'script-output'

    generate_core_vocab_list(subtitle_folder, tagger, save_dir)

    # Importing in already generated lists with lemmas that satisfy
    # all, 90%, or 80% show occurence
    shows_and_lemmas, shows_all, shows_90per, \
        shows_80per = import_core_vocab_list(save_dir)

    # These are essentially my 'core vocabulary lists' depending if I want my
    # occurence requirement to be all shows, 90% of shows, or 80% of shows
    print('')
    print(f'# of Lemmas in all shows: {len(shows_all)}')
    print(f'# of Lemmas in 90% of shows: {len(shows_90per)}')
    print(f'# of Lemmas in 80% of shows: {len(shows_80per)}\n')

    # Calculate TF-IDF for each lemma and generate a square
    # maxtrix with values between 0-1 to represent the similarity of the text

    total_lemma_occurence = shows_lemma_is_in(shows_and_lemmas)  # dict of {lemmas : # of shows they appear in}
    total_shows = len(shows_and_lemmas)  # number of shows in the subtitle folder
    
    all_shows_TF_IDF = {}  # empty dict for storing {lemma : TF-IDF value} for every lemma in each show

    for show in shows_and_lemmas:
        total_words_in_show = sum(list(shows_and_lemmas[show].values()))     
        TF_IDF = {}
        # calculate Term-freq * Inverse document frequency (TF-IDF)
    
        for lemma in total_lemma_occurence:
            if lemma in shows_and_lemmas[show]:
                TF = shows_and_lemmas[show][lemma] / total_words_in_show
                IDF = np.log(total_shows / total_lemma_occurence[lemma])
                
                TF_IDF[lemma] = TF * IDF
            
            else:
                TF_IDF[lemma] = 0

            # Note: TF-IDF = 0 if lemma is in all shows, or if it does not
            # appear in a show

        all_shows_TF_IDF[show] = TF_IDF

    
    # Calculate the cosine similarity between the shows
    TF_IDF_matrix = np.zeros((total_shows, total_shows))  # empty matrix for storing similarity scores
    show_list_order = list([x for x in all_shows_TF_IDF])  # list to know the order of the rows/columns in TF-IDF matrix

    print('-- Beginning Cosine Similarity Calculations --\n')

    for i,show1 in enumerate(all_shows_TF_IDF):
        print(f'Calculating similarities to {show1}')

        for j,show2 in enumerate(all_shows_TF_IDF):
            A_vec = list(all_shows_TF_IDF[show1].values())
            B_vec = list(all_shows_TF_IDF[show2].values())
            A_dot_B = np.dot(A_vec, B_vec)

            A_norm = np.linalg.norm(A_vec)
            B_norm = np.linalg.norm(B_vec)
            norm_product = A_norm * B_norm

            cos_sim = A_dot_B / norm_product

            TF_IDF_matrix[i,j] = cos_sim

    print('-- TF-IDF matrix calculation complete --\n')

    # For each show, print the next 3 shows that are closest in similarity
    show_similarity_output = f'{save_dir}/Show Similarity Analysis Results.txt'

    print('-- Beginning write of similarity analysis to file --')
    with open(show_similarity_output, 'w') as file:

        for i,show in enumerate(show_list_order):
            file.write(f'Top 3 similar shows to {show}:\n')

            similarity_values = TF_IDF_matrix[i]

            # sorts values from greatest -> least
            sorted_similarity_values = sorted(similarity_values, reverse=True)

            # ignores '1', which is similarity with itself
            top_3_similar_val = sorted_similarity_values[1:4]  

            for j,x in enumerate(top_3_similar_val):
                # pulling index where x is in the similarity array
                index = np.where(similarity_values == x)[0][0]  # [0][0] is for getting the integer
                file.write(f'{j+1} {show_list_order[index]}: {x*100:.2f}%\n')

            file.write('\n')

    print('-- Similarity analysis file writing complete --')
    return


if __name__ == '__main__':
    main()