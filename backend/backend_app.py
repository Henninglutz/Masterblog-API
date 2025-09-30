from flask import Flask, jsonify
from flask_cors import CORS
from flask import request

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


#creating a new, unique "id"
def next_id():
    max_id = 0
    for p in POSTS:
        post_id = p.get("id", 0)
        if post_id > max_id:
            max_id = post_id
    return max_id + 1

#ID is the place to be - search function
def find_index(pid: int):
    for i, p in enumerate(POSTS):
        if p["id"] == pid:
            return i
    return None


#list of all posts
@app.get('/api/posts')
def list_posts():
    return jsonify(POSTS), 200


#parameters for every post: ID,TITLE, CONTENT
#201 return
#400 Error if somthing missing
@app.post('/api/posts')
def add_post():
    data = request.get_json(silent=True) or {}
    required = ("title", "content")
    missing = []
    for field in required:
        value = data.get(field)
        if not value or not str(value).strip():
            missing.append(field)


#using the ID to update the post (Content or Title)
@app.put("/api/posts/<int:pid>")
def update_post(pid: int):
    idx = find_index(pid)
    if idx is None:
        return jsonify({"error": f"Post with id {pid} not found."}), 404

    data = request.get_json(silent=True) or {}

    if "title" in data and isinstance(data["title"], str):
        new_title = data["title"].strip()
        if new_title:
            POSTS[idx]["title"] = new_title

    if "content" in data and isinstance(data["content"], str):
        new_content = data["content"].strip()
        if new_content:
            POSTS[idx]["content"] = new_content

    return jsonify(POSTS[idx]), 200


#delete function via ID
@app.delete('/api/posts/<int:pid>')
def delete_post(post_id:int):
    idx = find_index(post_id)
    if idx is None:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404
    POSTS.pop(idx)
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200


#calling the new ID here within post
    if missing:
        return jsonify({"error": "Missing required field(s): " + ", ".join(missing)}), 400
    post = {
        "id": next_id(),
        "title": data["title"].strip(),
        "content": data["content"].strip(),
    }
    POSTS.append(post)
    return jsonify(post), 201

#search function
@app.get("/api/posts/search")
def search_posts():
    q_title = (request.args.get("title") or "").lower()
    q_content = (request.args.get("content") or "").lower()

    def matches(p):
        title_ok = (q_title in p["title"].lower()) if q_title else True
        content_ok = (q_content in p["content"].lower()) if q_content else True
        return title_ok and content_ok

    results = [p for p in POSTS if matches(p)]
    return jsonify(results), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
