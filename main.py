#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/16 2:27 PM
# @File    : main.py
# @Software: PyCharm

from flask import Flask, render_template, request, url_for, redirect
from utils import top10_newest, top10_rated

app = Flask(__name__)


@app.route('/')
def hello():
    if request.method == 'GET':
        return render_template('index.html',
                               newest=top10_newest(),
                               rated=top10_rated())


@app.route('/<question>')
def question_detail(question):
    import pyquery
    d = pyquery.PyQuery(url='https://stackoverflow.com/questions/' + question)
    d('div.js-comment-actions.comment-actions').remove()
    question_desc = d('#question > div > div.postcell.post-layout--right > div.post-text')
    question_thread = d('#question > div > div:nth-child(3)')  # d('#comments-2025282 > ul')
    best_answer = d('.answer:first > div > div.answercell.post-layout--right > div.post-text')
    return render_template('question.html',
                           question=question_desc,
                           question_thread=question_thread,
                           best_answer=best_answer
                           )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000')
