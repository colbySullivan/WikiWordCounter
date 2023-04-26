"""
   author = Colby Sullivan, Last modified 4/25/2023
"""

import wikipediaapi as wapi
import matplotlib.pyplot as plt
import numpy as np
import sys
import time # May need this to introduce delays for API. Sleep for 1 second with time.sleep(1)

def get_text(page):
    """
    Gets all the text on a given wiki page and
    adds them to a set.

    Args:
        page (WikipediaPage): Wiki page

    Returns:
        set: text from the wiki page
    """
    wiki_set_of_text = list()
    page_text = page.text
    text_no_links = page_text.split()
    wiki_links = page.links
    text_links = list()
    for title in sorted(wiki_links.keys()):
            split_title = title.split()
            for split in split_title:
                if split.isalnum():
                    text_links.append(split)
    wiki_set_of_text = text_no_links + text_links
    return wiki_set_of_text

def count_words(wiki_set_of_text):
    dict_of_words = {}
    for word in wiki_set_of_text:
        if word in dict_of_words:
            value_buffer = dict_of_words[word]
            dict_of_words[word] = value_buffer+1
        else:
            dict_of_words[word] = 0
    return dict_of_words

def create_graph(completed_dict, graph_num):
    """
    Creates a graph using the matplotlib import. 
    Takes in a dictionary and splits it into two lists
    of the size taken from the command parameter.
    When graph is finished then this will print the top programming 
    languages and and their values to the console.
    
    https://matplotlib.org/stable/gallery/lines_bars_and_markers/barh.html

    Args:
        completed_dict (dictionary): Completed dictionary to be split
        graph_num (int): Number of languages on the y axis
    """
    plt.rcdefaults()
    fig, ax = plt.subplots() # Need fig or ax throws tuple error
    number = list_from_dict(list(completed_dict.values()), graph_num)
    language = list_from_dict(list(completed_dict.keys()), graph_num)
    y_pos = np.arange(graph_num)
    ax.barh(y_pos, number)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(language)
    ax.set_xlabel('Word occurrences')
    ax.set_title('Top words on a wiki page')
    plt.savefig("words.jpg")
    print("Top", graph_num, " word in the wiki page")
    list_length = len(number) #Extraneous variable suppresses enumerate warning
    for index in range(list_length):
        print (language[index], "-", number[index])

def list_from_dict(complete_dict_list, graph_num):
    """
    complete_dict_list is a list of either keys or values that are sent
    as a parameter. A new list is create with the size of graph_num
    that is taken from the num_to_show value.

    Args:
        complete_dict_list (dictionary): List of either key or values from dictionary
        graph_num (int): Number of languages to show on graph

    Returns:
        list: List of keys or values with the size of num_to_show
    """
    new_set = []
    index = 0
    for dict_term in complete_dict_list:
        if index < graph_num:
            new_set.append(dict_term)
            index+=1
    return new_set

##########################################################################

def main():
    """ 
        Parameters:
        num_to_show -- Number of top languages to show in ranking
    """
    title_of_page = "Danny DeVito"
    top_words = 10
    print("Accessing Wikipedia API")
    wiki_wiki = wapi.Wikipedia('en')
    page = wiki_wiki.page(title_of_page)
    print("Getting text")
    wall_of_text = get_text(page)
    #print(wall_of_text)
    print("Counting words")
    completed_dict = count_words(wall_of_text)
    sorted_dict = dict(sorted(completed_dict.items(), key=lambda item:item[1], reverse=True)) # Sort puts smallest value first
    create_graph(sorted_dict, top_words)

if __name__ == "__main__":
    # execute only if run as a script
    main()
