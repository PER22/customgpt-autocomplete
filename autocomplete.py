import sys
from flask import Flask, request
import time  

app = Flask(__name__)

sys.setrecursionlimit(1500)

class SortedFixedSizeArray:
    def __init__(self, max_size=4):
        self.arr = []
        self.max_size = max_size
    def __insert__(self, tuple):
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
        node.frequency += frequency
    
    def prioritize(self):
        self._prioritize(self.root, '')
    
    def _prioritize(self, node, prefix):
        if node.is_end_of_word:
            node.most_frequent_suffixes.__insert__((prefix, node.frequency))
        
        for char, child in node.children.items():
            self._prioritize(child, prefix + char)
            for suffix_tuple in child.most_frequent_suffixes.arr:
                node.most_frequent_suffixes.__insert__(suffix_tuple)
        
    def suggest(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return [suggestion for suggestion in node.most_frequent_suffixes.arr]

trie = Trie()

print('loading data...')
start_time = time.time()  

with open('medical-questions', 'r') as file:
  for line in file:
    query, frequency = (lambda parts: (parts[0], int(parts[1])))(line.strip().split('\t'))
    trie.insert(query=query, frequency=frequency)

end_time = time.time()  
print(f"Data loaded and inserted in {end_time - start_time} seconds")

print("Now prioritizing")
start_time = time.time()  
trie.prioritize()
end_time = time.time() 
print(f"Trie is prioritized in {end_time - start_time} seconds")

print('Trie is prioritized, ready for queries')

@app.route('/s')
def autocomplete():
    start_time = time.time() 
    query = request.args.get('q', '')
    suggestions = trie.suggest(query)
    end_time = time.time()  
    print(f"Suggestion generated in {end_time - start_time} seconds")
    return {'suggestions': suggestions}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
