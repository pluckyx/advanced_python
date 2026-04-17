'''
O(n^2)
Class Definition:

NodeTree: A class to represent a node in a Huffman tree. Each node can have a left and a right child.
Function huffman_code_tree:

This recursive function generates the Huffman codes for each character. It takes a node and the current binary string (initially empty) as input.
If the node is a string (a character), it returns a dictionary with the character and its corresponding binary code.
If the node is not a string, it calls itself recursively for the left and right children, updating the binary string with '0' for left and '1' for right.
It accumulates and returns the Huffman codes in a dictionary.
Calculating Frequency of Each Character in the String:

The code iterates over the string, counting the frequency of each character and storing it in the frequency dictionary.
Sorting the Frequencies:

The frequencies are sorted in descending order and stored in nodes.
Building the Huffman Tree:

The while loop continues until there is only one node left in nodes.
In each iteration, the two nodes with the lowest frequency are taken, a new NodeTree is created with these two nodes as children, and this new node is added back to nodes.
The nodes list is then re-sorted by frequency.
Generating Huffman Codes:

The huffman_code_tree function is called with the root node of the Huffman tree to generate the Huffman codes.
Printing the Characters with Their Huffman Codes:

The code iterates over the frequency list and prints each character with its corresponding Huffman code.

'''
string = 'BCAADDDCCACACAC'

class NodeTree(object):

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def get_children(self):
        return (self.left, self.right)

    def __repr__(self):
        return f'Node({self.left}, {self.right})'


# Main function implementing huffman coding
def huffman_code_tree(node, left=True, bin_string=''):
    if isinstance(node, str):
        return {node: bin_string}
    l, r = node.get_children()
    codes = dict()
    codes.update(huffman_code_tree(l, True, bin_string + '0'))
    codes.update(huffman_code_tree(r, False, bin_string + '1'))
    return codes


# Calculating frequency
frequency = {}
for char in string:
    frequency[char] = frequency.get(char, 0) + 1

frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=True)

nodes = frequency

while len(nodes) > 1:
    (key1, count1) = nodes[-1]
    (key2, count2) = nodes[-2]
    nodes = nodes[:-2]
    new_node = NodeTree(key1, key2)
    nodes.append((new_node, count1 + count2))

    nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

huffman_code = huffman_code_tree(nodes[0][0])


for (char, freq) in frequency:
    print(f' {char!r:4} | {huffman_code[char]:12}')

