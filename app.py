from flask import Flask, request, render_template_string
import pickle
import numpy as np

app = Flask(__name__)

# Load data
pt = pickle.load(open('pt.pkl', 'rb'))
similarity_score = pickle.load(open('similarity.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))

# Recommendation function
def recommend(book_name):
    try:
        index = np.where(pt.index == book_name)[0][0]
        similar_items = sorted(
            list(enumerate(similarity_score[index])),
            key=lambda x: x[1],
            reverse=True
        )[1:6]

        data = []
        for i in similar_items:
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            title = temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0]
            author = temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0]
            image = temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values[0]
            data.append((title, author, image))

        return data
    except:
        return []

# HTML + CSS inside Python
template = """
<!DOCTYPE html>
<html>
<head>
    <title>Book Recommender</title>
    <style>
        body {
            font-family: Arial;
            text-align: center;
            background-color: #f5f5f5;
        }
        input {
            padding: 10px;
            width: 300px;
        }
        button {
            padding: 10px 20px;
            cursor: pointer;
        }
        .results {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
        }
        .card {
            margin: 15px;
            padding: 10px;
            background: white;
            width: 200px;
            border-radius: 10px;
        }
        img {
            width: 100%;
        }
    </style>
</head>
<body>

<h1>📚 Book Recommender System</h1>

<form method="post">
    <input type="text" name="book" placeholder="Enter book name" required>
    <button type="submit">Recommend</button>
</form>

<div class="results">
    {% for book in data %}
        <div class="card">
            <img src="{{ book[2] }}">
            <h3>{{ book[0] }}</h3>
            <p>{{ book[1] }}</p>
        </div>
    {% endfor %}
</div>

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    data = []
    if request.method == 'POST':
        book_name = request.form.get('book')
        data = recommend(book_name)
    return render_template_string(template, data=data)

if __name__ == '__main__':
    app.run(debug=True)