from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df=pickle.load(open('popular.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
similarity_score=pickle.load(open('similarity_score.pkl','rb'))

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           book_author=list(popular_df['Book-Author'].values),
                           book_image=list(popular_df['Image-URL-L'].values),
                           book_votes=list(popular_df['num_ratings'].values),
                           book_rating=list(popular_df['avg_rating'].values))

@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

@app.route('/recommended_books',methods=['post'])
def recommended_books():
    user_input=request.form.get('user_input')

    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        # print(pt.index[i[0]])
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))

        data.append(item)

    print(data)
    # return data
    return render_template('/recommend.html',data=data)

if __name__=='__main__':
    app.run(debug=True)

