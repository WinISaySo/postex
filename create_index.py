import csv
from string import Template

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

        if row["category"] not in index:
              index[row["category"]] = []

        index[row["category"]].append({
            "id": row["id"],
            "user_id": row["user_id"],
            "title": row["title"],
            "created_at": row["created_at"],
            "last_updated": row["updated_at"],
            "body": row["body"] 
        })

with open("index.md", "w") as mdfile:
    for category, posts in index.items():
        mdfile.write(f"## {category}\n")
        for post in sorted(posts, key=lambda p: p["title"]):
            mdfile.write(post_template.substitute(
                title=post["title"],
                user_id=post["user_id"],
                post_id=post["id"]
            ))
