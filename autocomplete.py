from flask import Flask, request

app = Flask(__name__)
import sys
sys.setrecursionlimit(1500)


#Will store the most common results for the trie node that contains it
class SortedFixedSizeArray:
    def __init__(self, max_size=4):
        self.arr = []
        self.max_size = max_size
    def insert(self, tuple):    
        self.arr.append(tuple)
        self.arr.sort(key=lambda x: -x[1])
        self.arr = self.arr[:self.max_size]

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0
        self.most_frequent_suffixes = SortedFixedSizeArray()


class Trie:
    def __init__(self):
        self.root = TrieNode()
   
    def insert(self, query, frequency):
        node = self.root
        for char in query:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.frequency = frequency
    
    def prioritize(self):
        self._prioritize(self.root, '')
    
    def _prioritize(self, node, prefix): 
        for char, child in node.children.items():
            self._prioritize(child, prefix + char) 

        
        if node.is_end_of_word:
            node.most_frequent_suffixes.insert((prefix, node.frequency))

        aggregated_suffixes = {}
        for child in node.children.values():
            for suffix, freq in child.most_frequent_suffixes.arr:
                if suffix not in aggregated_suffixes or aggregated_suffixes[suffix] < freq:
                    aggregated_suffixes[suffix] = freq

        # Insert aggregated suffixes ensuring the top N are kept
        for suffix, freq in aggregated_suffixes.items():
            node.most_frequent_suffixes.insert((suffix, freq))


    def suggest(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return [suggestion for suggestion in node.most_frequent_suffixes.arr]

trie = Trie()

print('loading data...')

with open('medical-questions', 'r') as file:
  for line in file:
    query, frequency = (lambda parts: (parts[0], int(parts[1])))(line.strip().split('\t'))
    trie.insert(query=query, frequency=frequency)

    
print("Data loaded successfully, now prioritizing")

trie.prioritize()

print('Trie is prioritized, ready for queries')




@app.route('/s')
def autocomplete():
    query = request.args.get('q', '')
    return trie.suggest(query)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)