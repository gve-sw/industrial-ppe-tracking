from flask import Flask, render_template
from flask_wtf import Form
from wtforms import RadioField, SelectField

SECRET_KEY = 'development'

app = Flask(__name__)
app.config.from_object(__name__)
class SimpleForm(Form):
    #example = RadioField('Label', choices=[('fart','description'),('traffo','whatever')])
    zone = SelectField(u'Zone', choices=[('c02', 'Carbon Dioxide Storage Room'), ('weld', 'Welding Area'), ('TNT', 'TNT Manufacturing Zone')])
    user1 = SelectField(u'User1', choices=[('John', 'John'), ('Adam', 'Adam'), ('Sarah', 'Sarah')])
    ppe1 = SelectField(u'Ppe1', choices=[('Helmet', 'Helmet'), ('Vest', 'Vest'), ('Goggles', 'Goggles')])
    user2 = SelectField(u'User2', choices=[('John', 'John'), ('Adam', 'Adam'), ('Sarah', 'Sarah')])
    ppe2 = SelectField(u'Ppe2', choices=[('Helmet', 'Helmet'), ('Vest', 'Vest'), ('Goggles', 'Goggles')])


@app.route('/',methods=['post','get'])
def hello_world():
    form = SimpleForm()
    if form.validate_on_submit():
        print (form.zone.data)
        print (form.user1.data)
    else:
        print (form.errors)
    return render_template('example.html',form=form)

if __name__ == '__main__':
    app.run(debug=True)