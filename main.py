"""Модуль для переключения между страницами"""
from flask import Flask, render_template, redirect, request, abort, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
# db = MyDataBase()


@app.route('/')
def main():
    return "EducofRa"



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
