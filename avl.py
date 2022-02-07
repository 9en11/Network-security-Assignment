# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 22:08:34 2022

@author: Naveen Mall
"""

import string
import random
import statistics
import matplotlib.pyplot as plt

import des
import random
des_obj = des.des()

def calculate_hamming_distance(s1, s2):
    
    s1_array = des.string_to_bit_array(s1)
    s2_array = des.string_to_bit_array(s2)
    d = 0
    for i in range(len(s1_array)):
        if s1_array[i] != s2_array[i]:
            d += 1
    return d


plain_text = "naveenkm"
secret_key = "priyansh"

plain_text_list = []
plain_text_list.append(plain_text)

secret_key_list = []
secret_key_list.append(secret_key)

plain_text_list_2 = []
plain_text_list_2.append(plain_text)


def change_string_by_m_bits(str, m):
    ignore_index_list = [7, 15, 23, 31, 39, 47, 55, 63]

    index_list = []
    for i in range(0, 64):
        if i not in ignore_index_list:
            index_list.append(i)
    
    positions = random.sample(index_list, m)
    
    for i in positions:
        str_list = des.string_to_bit_array(str)
        str_list[i] = str_list[i] ^ 1
    
    return des.bit_array_to_string(str_list)

def generate_random_plain_texts():
    initial_text = plain_text
    for i in range(0, 5):
        str = change_string_by_m_bits(initial_text, 1)
        while(str in plain_text_list):
            str = change_string_by_m_bits(initial_text, 1)
        plain_text_list.append(str)

def generate_random_secret_keys():
    initial_key = secret_key
    for i in range(0, 5):
        str = change_string_by_m_bits(initial_key, 1)
        while(str in secret_key_list):
            str = change_string_by_m_bits(initial_key, 1)
        secret_key_list.append(str)

def generate_five_hamming_dist_list():
    initial_text = plain_text
    for i in range(0, 5):
        str = change_string_by_m_bits(initial_text, i + 1)
        plain_text_list_2.append(str)
        initial_text = str


generate_random_plain_texts()
generate_random_secret_keys()
generate_five_hamming_dist_list()


def generate_plot(HD,title,initial_distances):

    HD_RoundWise = [initial_distances,] + list(zip(*HD))
    fig = plt.figure(figsize=(10, 8))                           
    plt.boxplot(HD_RoundWise, positions = [l for l in range(0,17)])
    medians = [ statistics.median(HD_current) for HD_current in HD_RoundWise ]
    plt.plot(medians, 'r')
    fig.suptitle("Plot for " + title, fontsize=18, fontweight = 'bold')
    plt.xlabel('Round Number', fontsize = 14, fontweight = 'bold')
    plt.ylabel('Hamming distance', fontsize = 14, fontweight = 'bold')
    fig.savefig(f'{title}.png')
    plt.show()

# function to perform the experiments with desired configuration changes in parts
def perform_experiment(change_plain_text,change_key,change_hamming_distance,experiment_name):

    HD=[]
    initial_distances = []

    cipher_text_dict = des_obj.run(secret_key, plain_text)
    org_ciper_text = cipher_text_dict["ciphers"]
    org_intermediates = cipher_text_dict["intermediate_res"]

    for i in range(1,6):

        if change_plain_text:
            cipher_text_dict = des_obj.run(secret_key_list[0], plain_text_list[i])
            cipher_text = cipher_text_dict["ciphers"]
            intermediates = cipher_text_dict["intermediate_res"]
            hd = [calculate_hamming_distance(txt1, txt2) for txt1, txt2 in zip(intermediates, org_intermediates)]
            HD.append(hd)
            initial_distances.append(calculate_hamming_distance(plain_text_list[i], plain_text))
        
        elif change_key:
            cipher_text_dict = des_obj.run(secret_key_list[i], plain_text)
            cipher_text = cipher_text_dict["ciphers"]
            intermediates = cipher_text_dict["intermediate_res"]
            hd = [calculate_hamming_distance(txt1, txt2) for txt1, txt2 in zip(intermediates, org_intermediates)]
            HD.append(hd)
            initial_distances.append(calculate_hamming_distance(plain_text_list[i], plain_text))
        
        elif change_hamming_distance:
            cipher_text_dict = des_obj.run(secret_key, plain_text_list_2[i])
            cipher_text = cipher_text_dict["ciphers"]
            intermediates = cipher_text_dict["intermediate_res"]
            hd = [calculate_hamming_distance(txt1, txt2) for txt1, txt2 in zip(intermediates, org_intermediates)]
            HD.append(hd)
            initial_distances.append(calculate_hamming_distance(plain_text_list_2[i], plain_text))

    generate_plot(HD,experiment_name,initial_distances)


perform_experiment(change_plain_text = 1, change_key = 0, change_hamming_distance = 0, experiment_name = "Five Different Plain Texts")

perform_experiment(change_plain_text = 0, change_key = 0, change_hamming_distance = 1, experiment_name = "Five Different Hamming Distances")

perform_experiment(change_plain_text = 0, change_key = 1, change_hamming_distance = 0, experiment_name = "Five Different Secret Keys")
