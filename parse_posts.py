import re
import os

filename = os.path.join(os.path.expanduser("~"), "Desktop\\DS\\blogs\\data", "data", "1005545.male.25.Engineering.Sagittarius.xml")
all_posts = []

# parse text from filename
with open(filename) as inf:
    post_start = False
    post = []
    # post starts with <post> tag and finishes with </post>
    for line in inf:
        line = line.strip()
        if line == "<post>":
            post_start = True
        elif line == "</post>":
            post_start = False
            all_posts.append("\n".join(post))
            post = []
        elif post_start:
            post.append(line)

print(all_posts[0])