# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    color = db.Column(db.String(20), default='gradient-1')

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    memos = Memo.query.order_by(Memo.created_at.desc()).all()
    return render_template('index.html', memos=memos)

@app.route('/add_memo', methods=['POST'])
def add_memo():
    content = request.form.get('content')
    color = request.form.get('color', 'gradient-1')
    if content:
        memo = Memo(content=content, color=color)
        db.session.add(memo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_memo/<int:id>', methods=['POST'])
def delete_memo(id):
    memo = Memo.query.get_or_404(id)
    db.session.delete(memo)
    db.session.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True,port=5001)