from flask import Flask, render_template, request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           vote = list(popular_df['num_ratings'].values),
                           rating = list(popular_df['avg_ratings'].values),
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    if user_input not in books['Book-Title'].values:
        return render_template('recommend.html',
                               book_name=list(books['Book-Title'].values),
                               error="❌ This book is not in the Top 50 books.")


    index = np.where(pt.index == user_input)[0][0]
    distances = similarity_scores[index]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        # print(pt.index[i[0]])
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        # print(temp_df.drop_duplicates('Book-Title')['Image-URL-M'])
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    # print(data)
    return render_template('recommend.html', data = data)


if __name__ == '__main__':
    app.run(debug=True)