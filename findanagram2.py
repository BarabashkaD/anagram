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
class QWord:
    def __init__(self):
        self.ihash = int(0)
        self.word = None
        self.sword= None
        self.dahash=None
        self.line = 0 
        self.widx = 0

    # compares the second value
    def __lt__(self, other):
        return self.ihash < other.ihash
    def bits_hash(self):
        self.ihash = int(0)
        for idx, ch in enumerate(self.word):
            self.ihash |= powersof2[letter2index[ch]]
    def denis_hash_array(self):
        if self.dahash is None:
            self.dahash = array.array('b',zero_list)
            for idx, ch in enumerate(self.word):
                self.dahash[letter2index[ch]] += 1
        return self.dahash  
    def anagram_hash(self,alg = 0)  :
        if alg == 0:
            return self.denis_hash_array()
        if self.sword is None:
            self.sword = sorted(self.word)
        return self.sword
        

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
                item = QWord()
                item.word = word2
                item.line = lidx
                item.widx = widx
                text_words.append(item)
        #if len(words) != 0:_
        #    print (f"Line {lidx: 5} contain {widx+1: 3} words")
    print (f"Total lines {lidx:5} with {len(text_words): 6} words")
    return text_words


def preprocessing2heap(words):
    processed_heap = []
    for widx, word in enumerate(words):
        word.bits_hash()
        heapq.heappush(processed_heap, word)
    return processed_heap #words 

def find_anagrams_heap(words):
    anagrams = []
    words2 = sorted(words)
    
    while words2:
        ref_item = words2.pop(0)
        ref_item.anagram_hash()

        for cur_item in words2:
            if cur_item.ihash == ref_item.ihash:
                if ref_item.word != cur_item.word:
                    cur_item.anagram_hash()
                    if cur_item.dahash == ref_item.dahash:
                        anagrams.append({"word1":cur_item,"word2":ref_item})
                        words2.remove(cur_item)
            else:
                break
    return anagrams    

def print_anagrams(anagrams):
    for idx,anagama in enumerate(anagrams):
        print (anagama["word1"].word,anagama["word2"].word)
    print (f"Total Anagrams {idx+1: 5}")

def main():
    words = load_text("example.txt")   
    tic = time.perf_counter()
    words4 = preprocessing2heap(words)
    tmc = time.perf_counter()
    anagrams = find_anagrams_heap(words4)
    toc = time.perf_counter()
    print(f" find_anagrams with Heap {tmc - tic:0.4f} + {toc - tmc:0.4f} => {toc - tic:0.4f} seconds")
    print_anagrams(anagrams)     


if __name__ == '__main__':
    main()    