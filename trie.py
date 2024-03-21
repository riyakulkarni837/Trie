class TrieNode:
    def __init__(self, label=""):
        self.children = {}
        self.is_end_word = False
        self.label = label

class Trie:
    def __init__(self, is_compressed):
        self.is_compressed = is_compressed
        self.root = TrieNode()
        self.is_trie = True

    def construct_trie_from_text(self, text):
        """Constructs a trie from the given list of words."""
        for key in text:
            node = self.root
            i = 0
            while i < len(key):
                char = key[i]
                node = node.children.setdefault(char, TrieNode(char))
                i += 1
            node.is_end_word = True

        if self.is_compressed:
            self.compress(self.root)

    def construct_suffix_tree_from_text(self, keys):
        """Constructs a suffix tree from the given list of words."""
        for key in keys:
            i = 0
            while i < len(key):
                node = self.root
                suffix = key[i:]
                j = 0
                while j < len(suffix):
                    char = suffix[j]
                    node = node.children.setdefault(char, TrieNode(char))
                    j += 1
                node.is_end_word = True
                i += 1
            
        if self.is_compressed:
            self.compress(self.root)

    def compress(self, node, parent=None, char=None):
        """Compresses the trie or suffix tree recursively."""
        while len(node.children) == 1 and not node.is_end_word:
            child_char, child_node = next(iter(node.children.items()))
            node.label += child_node.label
            node.children = child_node.children
            node.is_end_word = child_node.is_end_word
            if parent:
                parent.children[char] = node
            child_node = node
            node = child_node

        for char, child_node in node.children.items():
            self.compress(child_node, node, char)

    def insert_suffix_tree(self, suffix):
        """Inserts a suffix into the suffix tree."""
        node = self.root
        if self.is_compressed:
            common_prefix = ''
            i = 0
            while i < len(suffix):
                char = suffix[i]
                if char in node.children:
                    common_prefix += char
                    node = node.children[char]
                else:
                    break
                i += 1
            while i < len(suffix):
                char = suffix[i]
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
                i += 1
            node.is_end_word = True
        else:
            i = 0
            while i < len(suffix):
                char = suffix[i]
                if char not in node.children:
                    node.children[char] = TrieNode(char)
                node = node.children[char]
                i += 1
            node.is_end_word = True

    def search_and_get_depth(self, key):
        """Searches for a key in the trie or suffix tree and returns its depth."""
        node = self.root
        depth = 0
        i = 0
        while i < len(key):
            found = False
            for child_char, child_node in node.children.items():
                if key[i:].startswith(child_node.label):
                    found = True
                    depth += 1
                    node = child_node
                    i += len(child_node.label)
                    break
            if not found:
                return -1
        return depth if node.is_end_word else -1
