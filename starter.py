from pkg import app

if __name__ == '__main__':
    app.config.from_pyfile("config.py")
    app.run(debug=True, port=3000)