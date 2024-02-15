## Autocomplete in python from a text file:

#### The goal was to mimic a google search, in that a partial query being typed prompted the system to return autocomplete suggestions.

There is no elastic aspect or scoring aspect, so typoes are not resolved in the code at all.
For example, searching `howt o train your d` will not return `[how to train your dog', 'how to train your delts', 'how to train your dragon']`, but might instead return `[]` if `howt` does not appear in any queries.

Aside from that aspect, I am happy with this code.

At first I built a standard trie, but the resulting response time was poor, as the suggestion process included traversing through every query that shared the current prefix. As building the trie is a one-time process here, I decided to front-load the process of collecting the matching queries into that step as well. 

I modified the standard trie by giving each node a sorted array of size k (default is 4, as mentioned in the assignment sheet), and populating these arrays recusively with the highest frequency query strings in any child nodes. As a result, the suggestion part of the logic is very fast, at the cost of a more memory-intensive trie. 


I had some difficulties along the way: I failed to notice that although the queries have associated frequencies, they are not unique. As a result, I was getting responses that didn't match the data. However, upon finding this, it all clicked together nicely. In addition, the longest query (or at least the one that caused the problem) was over 1000 characters long. I used `sys.setrecursionlimit(1500)` to get around this problem.

### Timing: 
- Processing the 573596 queries into a trie: `26.6s`
- Adding the 4 most frequent suffixes to each trie node: `20.1s`
- Getting suggestions for:
    - 'how to': `0.0004s`
    - 'how to train your d: `0.00016s`
