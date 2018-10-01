from flask import Flask, request, render_template, flash, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, DateField, IntegerField, BooleanField, ValidationError # see some new ones... + ValidationError
from wtforms.validators import Required, Length

import requests
import json


API_KEY= '5e7727f2cde00a408a3fd1e9a7d5a88a'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string' 
app.debug=True

class WeatherForm(FlaskForm):
    Zipcode = IntegerField("Enter Zipcode:", validators=[Required()])
    submit= SubmitField('Submit')

    def validate_passcode(self, field):
        for ch in field.data:
            if len(str(ch)) != 5:
                raise ValidationError("Your passcode was not valid because it had less than 5 characters.")

@app.route('/zipcode', methods= ['POST'])
def zipcode():
	form= WeatherForm()
	if form.validate_on_submit():
		zipcode= str(form.zipcode.data)
		params = {}
		params['zip'] = zipcode + ',us'
		params['appid'] = '5e7727f2cde00a408a3fd1e9a7d5a88a'
		baseurl= 'http://api.openweathermap.org/data/2.5/weather?'
		response = requests.get(baseurl, params = params)
		response_dict= json.loads(response.text)
		print(response_dict)

		description = response_dict['weather'][0]['description']
		city = response_dict['name']
		temperature_kelvin = response_dict['main']['temp']

		return render_template('results.html', city= city, description= description, temperature= temperature)



	flash(form.errors)
	return render_template('weather_form.html', form = form)


if __name__ == '__main__':
	app.run(use_reloader= True, debug=True)




