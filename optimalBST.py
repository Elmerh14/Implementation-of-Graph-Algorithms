import requests
import pprint
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# === Step 1: Query News API and Generate WordCloud ===
url = 'https://newsapi.org/v2/everything'
secret = '27f1f4908a0a43d18fd550e879571600' 

parameters = {
    'q': 'Palestine',
    'pageSize': 100,
    'apiKey': secret
}

response = requests.get(url, params=parameters)
data = response.json()
pprint.pprint(data)

# Extract titles and generate text string
textCombined = ' '.join(article['title'] for article in data['articles'])

# Generate word cloud
wordcloud = WordCloud(max_font_size=40).generate(textCombined)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

# === Step 2: Get Top-N Words and Probabilities (Normalized) ===
freq_dict = wordcloud.words_
top_words = dict(sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)[:50])
keys = sorted(top_words.keys())  # Sorted for OBST
raw_freqs = [top_words[k] for k in keys]
total = sum(raw_freqs)

# Normalize probabilities for OBST
p = [f / total for f in raw_freqs]
dummy_total = 1.0 - sum(p)
if dummy_total < 0:
    dummy_total = 0  # Prevent negative dummy weight due to float error
q = [dummy_total / (len(keys) + 1)] * (len(keys) + 1)
n = len(keys)

# === Step 3: Build Random BST and Cost Calculation ===
class Node:
    def __init__(self, key):
        self.key = key
        self.left = self.right = None

def insert_bst(root, key):
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert_bst(root.left, key)
    else:
        root.right = insert_bst(root.right, key)
    return root

def build_bst(keys):
    root = None
    for key in keys:
        root = insert_bst(root, key)
    return root

def cost_bst(root, key_probs, depth=1):
    if not root:
        return 0
    cost = depth * key_probs.get(root.key, 0)
    cost += cost_bst(root.left, key_probs, depth + 1)
    cost += cost_bst(root.right, key_probs, depth + 1)
    return cost

shuffled_keys = keys[:]
random.shuffle(shuffled_keys)
bst_root = build_bst(shuffled_keys)
regular_cost = cost_bst(bst_root, dict(zip(keys, p)))

# === Step 4: Optimal Binary Search Tree (OBST) ===
def optimal_bst(p, q, n):
    e = [[0] * (n + 2) for _ in range(n + 2)]
    w = [[0] * (n + 2) for _ in range(n + 2)]
    root = [[0] * (n + 1) for _ in range(n + 1)]

    for i in range(1, n + 2):
        e[i][i - 1] = q[i - 1]
        w[i][i - 1] = q[i - 1]

    for l in range(1, n + 1):
        for i in range(1, n - l + 2):
            j = i + l - 1
            e[i][j] = float('inf')
            w[i][j] = w[i][j - 1] + p[j - 1] + q[j]
            for r in range(i, j + 1):
                t = e[i][r - 1] + e[r + 1][j] + w[i][j]
                if t < e[i][j]:
                    e[i][j] = t
                    root[i - 1][j - 1] = r - 1
    return e[1][n], root

optimal_cost, root_table = optimal_bst(p, q, n)

# === Step 5: Output Comparison ===
print(f"\nNormalized Probabilities Sum Check:")
print(f"  Sum of p: {sum(p):.4f}")
print(f"  Sum of q: {sum(q):.4f}")
print(f"  Total:    {sum(p) + sum(q):.4f}")

print(f"\nRegular BST Weighted Cost: {regular_cost:.4f}")
print(f"Optimal BST Weighted Cost: {optimal_cost:.4f}")
