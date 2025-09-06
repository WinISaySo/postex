import csv
from string import Template
import os

POST_TEMPLATE = Template(
    "- [$title](https://fetlife.com/users/$user_id/posts/$post_id)\n"
)

def create_index(posts, mdfile):
    for post in sorted(posts, key=lambda p: p["title"]):
        mdfile.write(POST_TEMPLATE.substitute(
            title=post["title"],
            user_id=post["user_id"],
            post_id=post["id"]
        ))

def main():
    index = {}
    with open("./backup/posts.csv", "r", newline="") as csvfile:
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

            category = "#" + row["category"].lower().replace(" ", "-")
            if category not in index:
                index[category] = []

            index[category].append(post)

    for tag, posts in index.items():
        with open(f"output/{tag.lstrip('#')}.md", "w") as mdfile:
            create_index(posts, mdfile)

    with open(f"output/index.md", "w") as mdfile:
        mdfile.write("## By Tag\n\n")
        for tag in sorted(index.keys()):
            mdfile.write(POST_TEMPLATE.substitute(
                title=tag,
                user_id=post["user_id"],
                post_id="REPLACE_ME"
            ))

        mdfile.write("\n## Alphabetical\n")
        all_posts = [post for posts in index.values() for post in posts]

        create_index(sorted(all_posts, key=lambda p: p["title"]), mdfile)


if __name__ == "__main__":
    main()
