from flask import Flask, jsonify
from flask_cors import CORS
import request

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

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


@app.route('/api/posts', methods=['GET'])                          # noch benötigt?
def get_posts():
    return jsonify(POSTS)


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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
