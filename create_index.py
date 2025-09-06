import csv
from string import Template
import sys

index = {}
post_template = Template("[$title](https://fetlife.com/$author/posts/$post")
post_template = Template(
    "- [$title](https://fetlife.com/users/$user_id/posts/$post_id)\n"
)
with open("./backup/posts.csv", "r", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["deleted_at"] or not row["category"]:
            continue

        body = row["body"]
        tags = []
        for i, line in enumerate(body.split("\n")[::-1]):
            if line.startswith("tags:"):
                tags = [
                    tag.strip()
                    for tag in line.strip("tags:").split(",")
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

        if not tags:
            category = row["category"]
            if category not in index:
                index[category] = []

            index[category].append(post)

with open("index.md", "w") as mdfile:
    for tag, posts in index.items():
        mdfile.write(f"## {tag}\n")
        for post in sorted(posts, key=lambda p: p["title"]):
            mdfile.write(post_template.substitute(
                title=post["title"],
                user_id=post["user_id"],
                post_id=post["id"]
            ))
