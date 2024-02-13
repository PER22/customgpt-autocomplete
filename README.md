## Autocomplete in python from a text file:

#### The goal was to mimic a google search, in that a partial query being typed prompted the system to return autocomplete suggestions.

There is no elastic aspect or scoring aspect, so typoes are not resolved in the code at all.
For example, searching `howt o train your d` will not return `[how to train your dog', 'how to train your delts', 'how to train your dragon']`, but might instead return `[]` if `howt` does not appear in any queries.

Aside from that aspect, I am happy with this code.

At first I built a standard trie, but the resulting response time was poor, as the suggestion process included traversing through every query that shared the current prefix. As building the trie is a one-time process here, I decided to front-load the process of collecting the matching queries into that step as well. 

I modified the standard trie by giving each node a sorted array of size k (default is 4, as mentioned in the assignment sheet), and populating these arrays recusively with the highest frequency query strings in any child nodes. As a result, the suggestion part of the logic is very fast, at the cost of a more memory-intensive trie. 

I will have to learn how to time functions in python, and then I will add that to the code, and put some examples of queries, responses, and times, as well as measuring the building time for the trie.

I had some difficulties along the way: I failed to notice that although the queries have associated frequencies, they are not unique. As a result, I was getting responses that didn't match the data. However, upon finding this, it all clicked together nicely.