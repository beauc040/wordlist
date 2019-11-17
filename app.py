from flask import Flask, request, Response, render_template, jsonify
import json
import requests
import itertools
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Regexp
import re

class WordForm(FlaskForm):
    avail_letters = StringField("Letters", validators= [
        Regexp(r'^[a-z]*$', message="must contain letters only")
    ])
    wlength = StringField("Word Length", validators= [
        Regexp(r'^([3-9]|10)$|^$', message="must be a number from 3 to 10, or nothing at all")
    ])
    pattern = StringField("Pattern", validators= [
        Regexp(r'^([a-z]|\.)*$', message="must contain letters or . only")
    ])
    submit = SubmitField("Go")

    def validate(self):
        if not super().validate():
            return False
        if not self.avail_letters.data and not self.pattern.data:
            err_msg = 'Either Letters, Pattern, or both must be specified'
            self.avail_letters.errors.append(err_msg)
            self.pattern.errors.append(err_msg)
            return False
        if self.pattern.data and self.wlength.data \
                and len(self.pattern.data) != int(self.wlength.data):
            err_msg = 'Word Length must be the same as Pattern length'
            self.pattern.errors.append(err_msg)
            self.wlength.errors.append(err_msg)
            return False
        return True

csrf = CSRFProtect()
app = Flask(__name__)
app.config["DICT_KEY"] = "86a0b2c1-6207-4d4e-9fa1-25115d00b3e1"
app.config["SECRET_KEY"] = "aelrkbjp9a8ehhjaa)(*J$(*GH"
app.config["TEMPLATES_AUTO_RELOAD"] = True
csrf.init_app(app)

def clean_def(d):
    if not d:
        return d
    d = re.sub('{[a-z]*}', '', d)
    d = re.sub('{/[a-z]*}', '', d)
    d = re.split('{[a-z]*\|', d)
    d = ''.join(d)
    d = re.sub('(\||[0-9])*}', '', d)
    if '|' in d or '{' in d or '}' in d:
        print(d)
        return None
    return d

def get_definitions(word):
    """ Returns the definitions of word (formatted in html) """
    url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/%s?key=%s" % \
        (word, app.config["DICT_KEY"])
    r = requests.get(url = url)
    data = r.json()
    def_list = []
    for defs in data:
        if type(defs) == str:
            continue
        defs = defs.get('def')
        if not defs:
            continue
        for d in defs or []:
            for s in d.get('sseq') or []:
                if s[0][0] == 'pseq':
                    s = s[0][1][0][1]
                    dt = s.get('dt')
                    if dt:
                        cdt = clean_def(dt[0][1])
                        if cdt:
                            def_list.append(cdt)
                    continue
                dt = s[0][1].get('dt')
                if dt:
                    cdt = clean_def(dt[0][1])
                    if cdt:
                        def_list.append(cdt)

    if not def_list:
        return ["No definitions found"]
    return def_list

@app.route('/')
def def_page():
    return index()

@app.route('/index')
def index():
    form = WordForm()
    return render_template("index.html", form=form, name='Ethan Beauclaire')


@app.route('/words', methods=['POST','GET'])
def letters_2_words():
    form = WordForm()
    if form.validate_on_submit():
        letters = form.avail_letters.data
        wlength = form.wlength.data
        pattern = form.pattern.data
    else:
        return render_template("index.html", form=form)

    with open('sowpods.txt') as f:
        if not pattern:
            good_words = set(x.strip().lower() for x in f.readlines())
        else:
            p = re.compile('^' + pattern + '$')
            good_words = set(x.strip().lower() for x in f.readlines() if p.match(x.strip().lower()))

    word_set = set()
    if letters:
        if wlength=="":
            for l in range(3,len(letters)+1):
                for word in itertools.permutations(letters,l):
                    w = "".join(word)
                    if w in good_words:
                        word_set.add(w)
        else:
            for word in itertools.permutations(letters,int(wlength)):
                w = "".join(word)
                if w in good_words:
                    word_set.add(w)
    else:
        for w in good_words:
            word_set.add(w)  # Already matched the pattern, length is satisfied from validation

    return render_template('wordlist.html',
        wordlist=sorted(word_set, key=lambda x:(len(x),x)),
        name="CS4131")




@app.route('/proxy')
def proxy():
    print("in proxy")
    word = request.args['word']
    defs = get_definitions(word)
    return jsonify(defs)
