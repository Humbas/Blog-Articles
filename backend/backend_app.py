from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

today =  datetime.today().strftime('%Y-%m-%d')

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

posts = [
    {"id": 1, "title": "First post", "content": "This is the first post.", "author": "Humberto", "date": today},
    {"id": 2, "title": "Second post", "content": "This is the second post.", "author": "Humberto", "date": today},
    {"id": 3, "title": "Aragon post", "content": "This is the aragon post.", "author": "Humberto", "date": today},
    {"id": 4, "title": "Zebra post", "content": "This is the zebra post.", "author": "Humberto", "date": today},
]


def find_post_by_id(post_id):
    """returns a post dict correspondent to the id argument"""
    for post in posts:
        if post_id == post['id']:
            return post


def provide_id():
    """provides next if when a post is inserted"""
    max = 0
    next_id = 0
    for post in posts:
        id = post['id']
        if max < id:
            max = id
            next_id = max + 1
    return next_id


def sort_asc_title(posts):
    """display list by asc title"""
    asc_title_posts = sorted(posts, key=lambda d: d['title'])
    return asc_title_posts


def sort_desc_title(posts):
    """display list by desc title"""
    desc_title_posts = sorted(posts, key=lambda d: d['title'], reverse=True)
    return desc_title_posts


def sort_asc_content(posts):
    """display list by asc content"""
    asc_content_posts = sorted(posts, key=lambda d: d['content'])
    return asc_content_posts

def sort_asc_author(posts):
    """display list by asc author"""
    asc_author_posts = sorted(posts, key=lambda d: d['author'])
    return asc_author_posts

def sort_desc_author(posts):
    """display list by desc author"""
    desc_author_posts = sorted(posts, key=lambda d: d['author'], reverse=True)
    return desc_author_posts



def sort_desc_content(posts):
    """display list by desc content"""
    desc_content_posts = sorted(posts, key=lambda d: d['content'], reverse=True)
    return desc_content_posts


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    """exposes post lists and allows sort list disposition by GET, allows post insertion by POST"""
    if request.method == 'GET':
        sort = request.args.get('sort')
        direction = request.args.get('direction')
        if direction and sort:
            if direction == 'asc':
                if sort == 'title':
                    return jsonify(sort_asc_title(posts))
                elif sort == 'content':
                    return jsonify(sort_asc_content(posts))
                elif sort == 'author':
                    return jsonify(sort_asc_author(posts))
                else:
                    return jsonify(posts)

            elif direction == 'desc':
                if sort == 'title':
                    return jsonify(sort_desc_title(posts))
                elif sort == 'content':
                    return jsonify(sort_desc_content(posts))
                elif sort == 'author':
                    return jsonify(sort_asc_content(posts))
                else:
                    return jsonify(posts)
            else:
                return jsonify(posts)
        return jsonify(posts)

    if request.method == 'POST':
        new_post = request.get_json()
        if new_post:
            if new_post['title'] == '':
                return jsonify({"Error": "No title was added"}), 400
            if new_post['content'] == '':
                return jsonify({"Error": "No content was added"}), 400
            if new_post['author'] == '':
                return jsonify({"Error": "No author was added"}), 400
            new_post['id'] = provide_id()
            new_post['date'] = today
            posts.append(new_post)
            return jsonify(
                {"message": f"Post successfully added"}, 200
            )
        else:
            return "No post was added"


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = find_post_by_id(post_id)

    if post is None:
        return 'Post not found', 404
    else:
        if request.method == 'DELETE':
            posts.remove(post)
            return jsonify(
                {"message": f"Post with the id {post_id} deleted successfully"}, 200
            )


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """allows post update by PUT request"""
    post = find_post_by_id(post_id)

    if post is None:
        return 'Post not found', 404
    else:
        if request.method == 'PUT':
            changed_post = request.json
            if changed_post['title'] != post['title']:
                post['title'] = changed_post['title']
            if changed_post['content'] != post['content']:
                post['content'] = changed_post['content']
            return jsonify(
                {"message": f"Post with the id {post_id} altered successfully"}, 200
            )


@app.route('/api/posts/search', methods=['GET'])
def handle_search():
    """provides title or content search by get method"""
    title = request.args.get('title')
    content = request.args.get('content')

    if title or content:
        filtered_posts = [post for post in posts if post.get('title') == title or post.get('content') == content]
        return jsonify(filtered_posts)
    else:
        return jsonify({"message": f"Nothing found regarding your search"}, 404)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
