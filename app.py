from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

favourites = []  # each entry: { 'outfit': str, 'occasion': str }

# ---------------- SPLASH ----------------
@app.route('/')
def splash():
    return render_template('splash.html')


# ---------------- LOGIN ----------------
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', favs=favourites)


# ---------------- SELECT ----------------
@app.route('/select')
def select():
    return render_template('select.html')


@app.route('/decide', methods=['POST'])
def decide():

    a_top = request.form.get('a_top')
    a_bottom = request.form.get('a_bottom')
    a_shoes = request.form.get('a_shoes')
    b_top = request.form.get('b_top')
    b_bottom = request.form.get('b_bottom')
    b_shoes = request.form.get('b_shoes')
    occasion = request.form.get('occasion', '').lower()

    occasion_rules = {
        'office': {
            'winner': 'Outfit A',
            'reasons': [
                '👔 Outfit A has a more formal and professional look suitable for workplace.',
                '🎨 The color combination in Outfit A is subtle and office-appropriate.',
                '✅ Outfit A follows a smart-casual dress code expected in office environments.'
            ]
        },
        'casual': {
            'winner': 'Outfit B',
            'reasons': [
                '😎 Outfit B has a relaxed and comfortable style perfect for casual outings.',
                '🌈 The colors in Outfit B are vibrant and fun, great for everyday wear.',
                '👟 Outfit B pairs well with casual footwear making it an easy go-to look.'
            ]
        },
        'function': {
            'winner': 'Outfit A',
            'reasons': [
                '🎉 Outfit A has an elegant and put-together look ideal for functions and events.',
                '✨ The outfit stands out in a crowd while still looking classy and appropriate.',
                '👗 Outfit A strikes the right balance between festive and formal for functions.'
            ]
        },
        'traditional': {
            'winner': 'Outfit B',
            'reasons': [
                '🪔 Outfit B carries a traditional and cultural aesthetic that fits the occasion.',
                '🎨 The rich tones and style of Outfit B complement traditional settings beautifully.',
                '🙏 Outfit B respects the dress etiquette expected at traditional ceremonies.'
            ]
        },
        'party': {
            'winner': 'Outfit B',
            'reasons': [
                '🥂 Outfit B has a bold and stylish look that turns heads at parties.',
                '💃 The outfit has great energy and flair perfect for a party vibe.',
                '🌟 Outfit B is trendy and eye-catching, exactly what a party calls for.'
            ]
        }
    }

    rule = occasion_rules.get(occasion, {
        'winner': 'Outfit A',
        'reasons': [
            '✅ Outfit A has a more balanced and versatile look overall.',
            '🎨 The color and style combination works well for this occasion.',
            '👌 Outfit A is the safer and smarter choice for this event.'
        ]
    })

    return render_template('result.html',
                           winner=rule['winner'],
                           occasion=occasion.capitalize(),
                           reasons=rule['reasons'],
                           a_top=a_top, a_bottom=a_bottom, a_shoes=a_shoes,
                           b_top=b_top, b_bottom=b_bottom, b_shoes=b_shoes)


# ---------------- UPLOAD ----------------
@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/compare', methods=['POST'])
def compare():

    file1 = request.files['outfit1']
    file2 = request.files['outfit2']

    filename1 = secure_filename(file1.filename)
    filename2 = secure_filename(file2.filename)

    path1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
    path2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)

    file1.save(path1)
    file2.save(path2)

    occasion = request.form.get('occasion', '').lower()

    occasion_outfits = {
        'office': {
            'recommendation': 'Outfit 1',
            'reasons': [
                '👔 Outfit 1 has a clean and professional look perfect for the office.',
                '🎨 The tones are subtle and workplace-appropriate.',
                '✅ It follows a smart-casual dress code expected in professional settings.'
            ]
        },
        'casual': {
            'recommendation': 'Outfit 2',
            'reasons': [
                '😎 Outfit 2 is relaxed and comfortable, great for casual outings.',
                '🌈 The colors are fun and vibrant for everyday wear.',
                '👟 It pairs well with casual footwear for an easy everyday look.'
            ]
        },
        'function': {
            'recommendation': 'Outfit 1',
            'reasons': [
                '🎉 Outfit 1 looks elegant and put-together, ideal for functions and events.',
                '✨ It stands out in a crowd while remaining classy and appropriate.',
                '👗 It strikes the right balance between festive and formal for functions.'
            ]
        },
        'traditional': {
            'recommendation': 'Outfit 2',
            'reasons': [
                '🪔 Outfit 2 carries a traditional aesthetic that fits the occasion beautifully.',
                '🎨 The rich tones complement traditional settings perfectly.',
                '🙏 It respects the dress etiquette expected at traditional ceremonies.'
            ]
        },
        'party': {
            'recommendation': 'Outfit 2',
            'reasons': [
                '🥂 Outfit 2 is bold and stylish, perfect for turning heads at parties.',
                '💃 It has great energy and flair that matches the party vibe.',
                '🌟 It is trendy and eye-catching, exactly what a party calls for.'
            ]
        }
    }

    rule = occasion_outfits.get(occasion, {
        'recommendation': 'Outfit 1',
        'reasons': [
            '✅ Outfit 1 has a more balanced and versatile look overall.',
            '🎨 The color and style combination works well for this occasion.',
            '👌 It is the safer and smarter choice for this event.'
        ]
    })

    return render_template('result.html',
                           img1=filename1,
                           img2=filename2,
                           winner=rule['recommendation'],
                           occasion=occasion.capitalize(),
                           reasons=rule['reasons'])


@app.route('/add_fav', methods=['POST'])
def add_fav():
    outfit = request.form.get('outfit', 'Outfit')
    occasion = request.form.get('occasion', '')
    favourites.append({'outfit': outfit, 'occasion': occasion})
    return redirect(url_for('dashboard'))


# ---------------- RATE ----------------
@app.route('/rate')
def rate():
    return render_template('rate.html')


@app.route('/rate_result', methods=['POST'])
def rate_result():

    file = request.files['outfit']
    filename = secure_filename(file.filename)

    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    return render_template('result.html',
                           single=filename,
                           text="Nice outfit! Try contrast colors 👌")


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)