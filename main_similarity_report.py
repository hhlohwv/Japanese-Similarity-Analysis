"""
Script for reading in show subtitles, calculating TF-IDF scores for
each lemma in the shows, and calculating cosine similarities between the
shows to determine which are the most similar (based on lemmas present)

Using networkx package for visualizing the similarity connections between
shows
"""

import numpy as np
import networkx as nx  # for visualizing similarity results
import pandas as pd  # data file output as csv

import fugashi  # Mecab wrapper for tokenizer function

# Functions for creating and importing the core vocab list from subtitle shows
from subtitleparsing import generate_core_vocab_list, import_core_vocab_list, shows_lemma_is_in


def main():
    #%% Generating list of core vocabulary from all shows in sub folder
    subtitle_folder = 'subtitles'

    tagger = fugashi.Tagger() # creating tagger object for later use

    save_dir = 'script-output'

    # generate_core_vocab_list(subtitle_folder, tagger, save_dir)

    #%% Importing in already generated lists with lemmas that satisfy
    # all, 90%, or 80% show occurence
    shows_and_lemmas, shows_all, shows_90per, \
        shows_80per = import_core_vocab_list(save_dir)

    # These are essentially my 'core vocabulary lists' depending if I want my
    # occurence requirement to be all shows, 90% of shows, or 80% of shows
    print('')
    print(f'# of Lemmas in all shows: {len(shows_all)}')
    print(f'# of Lemmas in 90% of shows: {len(shows_90per)}')
    print(f'# of Lemmas in 80% of shows: {len(shows_80per)}\n')

    #%% Calculate TF-IDF for each lemma and generate a square
    # maxtrix with values between 0-1 to represent the similarity of the text

    lemmas_num_of_show_in = shows_lemma_is_in(shows_and_lemmas)  # dict of {lemmas : # of shows they appear in}
    num_of_shows = len(shows_and_lemmas)  # number of shows in the subtitle folder
    
    TF_IDF_for_all_shows = {}  # empty dict for storing {lemma : TF-IDF value} for every lemma in each show

    i = 0

    for show in shows_and_lemmas:  # for all lemmas
        total_words_in_show = sum(list(shows_and_lemmas[show].values()))     
        tf_idf = {}
        # calculate Term-freq * Inverse document frequency (TF-IDF)
    
        for lemma in lemmas_num_of_show_in:
            if lemma in shows_and_lemmas[show]:
                tf = shows_and_lemmas[show][lemma] / total_words_in_show
                idf = np.log(num_of_shows / lemmas_num_of_show_in[lemma])
                
                tf_idf[lemma] = tf * idf
            
            else:
                tf_idf[lemma] = 0

            # Note: TF-IDF = 0 if lemma is in all shows, or if it does not
            # appear in a show

        TF_IDF_for_all_shows[show] = tf_idf

        # Saving TF-IDF scores for lemmas in shows to CSV files
        data = [list(TF_IDF_for_all_shows[show].keys()),list(TF_IDF_for_all_shows[show].values())]
        df = pd.DataFrame(data=data).T
        df.columns = ['Lemma', 'TF-IDF']
        df.to_csv(f'{save_dir}/TF-IDF Scores/{show}-TF-IDF.csv', encoding='utf_8_sig')

        # Printing out a status line saying how many shows have been processed, overwriting on the same line
        i += 1
        print(f'TF-IDF values calculated for {i}/{num_of_shows} shows')

    
    #%% Calculate the cosine similarity between the shows
    cosine_sim_matrix = np.zeros((num_of_shows, num_of_shows))  # empty matrix for storing similarity scores
    show_list_order = list([x for x in TF_IDF_for_all_shows])  # list to know the order of the rows/columns in TF-IDF matrix

    print('-- Beginning Cosine Similarity Calculations --\n')

    for i,show1 in enumerate(TF_IDF_for_all_shows):
        print(f'Calculating similarities to {show1}')

        for j,show2 in enumerate(TF_IDF_for_all_shows):
            A_vec = list(TF_IDF_for_all_shows[show1].values())
            B_vec = list(TF_IDF_for_all_shows[show2].values())
            A_dot_B = np.dot(A_vec, B_vec)

            A_norm = np.linalg.norm(A_vec)
            B_norm = np.linalg.norm(B_vec)
            norm_product = A_norm * B_norm

            cos_sim = A_dot_B / norm_product

            cosine_sim_matrix[i,j] = cos_sim

    print('-- Cosine Similarity matrix calculation complete --\n')

    # Saving cosine similarity matrix as csv
    df = pd.DataFrame(data=cosine_sim_matrix, columns=show_list_order, index=show_list_order)
    df.to_csv(f'{save_dir}/Cosine Similarity matrix.csv')

    # For each show, print the next 3 shows that are closest in similarity
    show_similarity_output = f'{save_dir}/Show Similarity Analysis Results.txt'

    print('-- Beginning write of similarity analysis to file --')
    with open(show_similarity_output, 'w') as file:

        for i,show in enumerate(show_list_order):
            file.write(f'Top 3 similar shows to {show}:\n')

            similarity_values = cosine_sim_matrix[i]

            # sorts values from greatest -> least
            sorted_similarity_values = sorted(similarity_values, reverse=True)

            # ignores '1', which is similarity with itself
            top_4_similar_val = sorted_similarity_values[1:5]  

            for j,x in enumerate(top_4_similar_val):
                # pulling index where x is in the similarity array
                index = np.where(similarity_values == x)[0][0]  # [0][0] is for getting the integer
                file.write(f'{j+1} {show_list_order[index]}: {x*100:.2f}%\n')

            file.write('\n')

    print('-- Similarity analysis file writing complete --')

    #%% Visualizing Similarity results as a graph
    G = nx.Graph()  # general network object

    # Creation of nodes for all shows
    for show in show_list_order:
        G.add_node(f'{show}')

    
    # Creating edges with weights equal to the similarity score
    for i,show1 in enumerate(show_list_order):
        similarity_values = cosine_sim_matrix[i]

        for index,show2 in enumerate(show_list_order):
            if show1 == show2:
                continue

            G.add_edge(show1, show2)
            G[show1][show2]['weight'] = similarity_values[index]*100


    # generate gexf file for viewing in Gephi program
    nx.write_gexf(G, f'{save_dir}/Show Similarity Graph.gexf')  

    return


if __name__ == '__main__':
    main()