#import numpy as np 
import time
import array
from copy import deepcopy
from string import ascii_lowercase
import heapq

alefbet_len = len(ascii_lowercase)

letter2index = {s:idx for idx,s in enumerate(ascii_lowercase)}
zero_list  = [0 for i in range(alefbet_len)]
zero_array = array.array('b',range(alefbet_len))
for i in range(alefbet_len):
    zero_array[i] = 0

powersof2 = array.array('I',[pow(2,i) for i in range(32) ])


#----------------------------------------------------------------------------------------------
#
#
def load_text(name):
    fh = open (name)

    text_words = []
    l = ['pool', 'loco', 'cool','ploo', 'stain', 'satin', 'pretty', 'nice', 'loop']
    for lidx,line in enumerate(fh):#l): #
        words = line.lower().split()
        for widx,word in enumerate(words):
            word2 = ''.join([ch for ch in word if ch in ascii_lowercase])#remove not alefbet letters
            if len(word2) > 0:
                text_words.append( {"word":word2,"line":lidx,"nw":widx})
        #if len(words) != 0:_
        #    print (f"Line {lidx: 5} contain {widx+1: 3} words")
    print (f"Total lines {lidx:5} with {len(text_words): 6} words")
    return text_words


def denis_hash(word):
    hash = {}
    for idx, ch in enumerate(word):
        if ch not in hash:
            hash[ch] = 1
        else:
            hash[ch] += 1
    return hash

def denis_hash_array(word):
    hash = array.array('b',zero_list)
    for idx, ch in enumerate(word):
        hash[letter2index[ch]] += 1
    return hash    

def bits_hash(word):
    bithash = int(0)
    for idx, ch in enumerate(word):
        bithash |= powersof2[letter2index[ch]]
    return bithash

def sort_hash(word):
    return sorted(word)

def preprocessing(words, hash_function):
    processed_words = []
    for widx, word in enumerate(words):
        #word["hash"] = hash_function(word['word'])
        tmp = deepcopy(word)
        tmp["hash"] = hash_function(word['word'])
        processed_words.append(tmp)
    return processed_words #words

#----------------------------------------------------------------------------------------------
class PQNode:

    def __init__(self, key, value):
        self.key = key
        self.value = value

    # compares the second value
    def __lt__(self, other):
        return self.key < other.key


def preprocessing2heap(words):
    processed_heap = []
    for widx, word in enumerate(words):
        tmp = deepcopy(word)
        hash = bits_hash(word['word'])
        heapq.heappush(processed_heap, PQNode(hash,tmp))
    return processed_heap #words    

def find_anagrams_heap(words):
    anagrams = []
    words2 = sorted(words)
    
    while words2:
        ref_item = words2.pop(0)
        ref_item_hash = ref_item.key
        ref_item_word = ref_item.value
        ref_hash_denis = denis_hash_array(ref_item_word['word'])

        for cur_item in words2:
            cur_item_hash = cur_item.key
            cur_item_word = cur_item.value
            if cur_item_hash == ref_item_hash:
                if ref_item_word['word'] != cur_item_word['word']:
                    cur_hash_denis = denis_hash_array(cur_item_word['word'])
                    if cur_hash_denis == ref_hash_denis:
                        anagrams.append({"word1":ref_item_word,"word2":cur_item_word})
                        words2.remove(cur_item)
            else:
                break
    return anagrams

#----------------------------------------------------------------------------------------------        
def is_anagrama(word1, word2):
    for ch in word1["hash"]:
        if ch not in word1["hash"]:
            return False
    return True


def find_anagrams_denis(words):
    anagrams = []
    for widx, word in enumerate(words):
        if word is not None:
            ref_hash_denis = denis_hash_array(word['word'])
            for j in range(widx + 2,len(words)):
                if words[j] is not None:
                    cur_hash_denis = denis_hash_array(words[j]['word'])
                    if ref_hash_denis == cur_hash_denis:
                        if word["word"] != words[j]["word"]:
                            anagrams.append({"word1":word,"word2":words[j]})
                        words[j] = None
    return anagrams



def find_anagrams(words):
    anagrams = []
    for widx, word in enumerate(words):
        if word is not None:
            for j in range(widx + 1,len(words)):
                if words[j] is not None:
                    if word["hash"] == words[j]["hash"]:
                        if word["word"] != words[j]["word"]:
                            anagrams.append({"word1":word,"word2":words[j]})
                        words[j] = None
    return anagrams

def find_anagrams_dima(words):
    anagrams = []
    for widx, word in enumerate(words):
        if word is not None:
            ref_hash_denis = denis_hash_array(word['word'])
            for j in range(widx + 1,len(words)):
                if words[j] is not None:
                    if word["hash"] == words[j]["hash"]:
                        if word["word"] != words[j]["word"]:
                            cur_hash_denis = denis_hash_array(words[j]['word'])
                            if ref_hash_denis == cur_hash_denis:
                                anagrams.append({"word1":word,"word2":words[j]})
                        words[j] = None
    return anagrams

def print_anagrams(anagrams):
    for idx,anagama in enumerate(anagrams):
        print (anagama["word1"]["word"],anagama["word2"]["word"])
    print (f"Total Anagrams {idx+1: 5}")

def main():
    words = load_text("example.txt")

    tic = time.perf_counter()
    words1 = preprocessing(words,denis_hash)
    tmc = time.perf_counter()
    anagrams = find_anagrams(words1)
    toc = time.perf_counter()
    print(f" find_anagrams List for Hash {tmc - tic:0.4f} + {toc - tmc:0.4f} => {toc - tic:0.4f} seconds")
   # print_anagrams(anagrams)


    tic = time.perf_counter()
    words2 = preprocessing(words,denis_hash_array)
    tmc = time.perf_counter()
    anagrams = find_anagrams(words2)
    toc = time.perf_counter()
    print(f" find_anagrams Array for Hash {tmc - tic:0.4f} + {toc - tmc:0.4f} => {toc - tic:0.4f} seconds")
   # print_anagrams(anagrams)

    tic = time.perf_counter()
    words3 = preprocessing(words,bits_hash)
    tmc = time.perf_counter()
    anagrams = find_anagrams_dima(words3)
    toc = time.perf_counter()
    print(f" find_anagrams Bits for Hash {tmc - tic:0.4f} + {toc - tmc:0.4f} => {toc - tic:0.4f} seconds")
   # print_anagrams(anagrams)
    
    tic = time.perf_counter()
    words4 = preprocessing2heap(words)
    tmc = time.perf_counter()
    anagrams = find_anagrams_heap(words4)
    toc = time.perf_counter()
    print(f" find_anagrams with Heap {tmc - tic:0.4f} + {toc - tmc:0.4f} => {toc - tic:0.4f} seconds")
#    print_anagrams(anagrams)




    tic = time.perf_counter()
    anagrams = find_anagrams_denis(words)
    toc = time.perf_counter()
    print(f" find_anagrams List for Hash by Denis {toc - tic:0.4f} seconds")
    print_anagrams(anagrams)

    #words = preprocessing(words,sort_hash)

if __name__ == '__main__':
    main()
