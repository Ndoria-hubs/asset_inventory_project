from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def features():
    return render_template('features.html')

if __name__ == '__main__':
    app.run(debug=True)
