from flask import Flask, render_template, redirect, request




app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def main():
	if request.method == 'POST':
		print (request.form)
		return render_template('index.html')
	else:
		return render_template('index.html')



if __name__ == "__main__":
	app.run()

