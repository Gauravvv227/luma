from flask import Flask, render_template, request, redirect, url_for
from database import init_db, add_entry,get_all_entries,get_taste_profile,get_notes_sample
from recommender import get_recommendations

app = Flask(__name__)

init_db()

@app.route('/')
def home():
    type_filter=request.args.get('type')
    entries=get_all_entries(type_filter)
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    type_ = request.form['type']
    genre = request.form['genre']
    rating = request.form['rating']
    notes = request.form['notes']

    add_entry(title, type_, genre, rating, notes)
    return redirect(url_for('home'))
@app.route('/taste')
def taste():
    profile=get_taste_profile
    return render_template('taste.html',profile=profile)
@app.route('/recommend')
def recommend():
    profile = get_taste_profile()
    notes_sample = get_notes_sample()
    recommendations = get_recommendations(profile, notes_sample)
    return render_template('recommend.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True) 




