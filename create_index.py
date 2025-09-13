from string import Template
import csv
import os
import re
import sys


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


POST_TEMPLATE = Template(
    "- [$title](https://fetlife.com/users/$user_id/posts/$post_id)\n"
)

def create_index(posts, mdfile):
    for post in sorted(posts, key=lambda p: natural_keys(p["title"])):
        mdfile.write(POST_TEMPLATE.substitute(
            title=post["title"],
            user_id=post["user_id"],
            post_id=post["id"]
        ))
        mdfile.write("\n")

def main(posts_file):

    index = {}
    with open(posts_file, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if any([
                row["deleted_at"],
                not row["category"],
                row["title"].startswith("#"),
                "index" in row["title"].lower()
            ]):
                continue

            body = row["body"]
            tags = []
            for i, line in enumerate(body.split("\n")[::-1]):
                if line.startswith("tags:"):
                    tags = [
                        tag.strip()
                        for tag in line.lstrip("tags:").split(",")
                        if tag.strip().startswith("#")
                    ]
                    break

            post = {
                "id": row["id"],
                "user_id": row["user_id"],
                "title": row["title"],
                "created_at": row["created_at"],
                "last_updated": row["updated_at"],
                "body": row["body"] 
            }

            for tag in tags:
                if tag not in index:
                    index[tag] = []

                index[tag].append(post)

            category = "#" + row["category"].lower().replace(" ", "-")
            if category not in index:
                index[category] = []

            index[category].append(post)

    with open("index.md", "w") as mdfile:
        for tag in sorted(index.keys(), key=natural_keys):
            mdfile.write(f"# {tag}\n")
            create_index(index[tag], mdfile)


if __name__ == "__main__":
    posts_file = sys.argv[1]
    main(posts_file)
