from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('table',attrs={'class':'history-rates-data'})
row2=table.find_all('a',attrs={'class':'w'})
row_length = len(row2)

temp = [] #initiating a list 

for i in range(1, row_length):

    #get tanggal
    tanggal=table.find_all('a',attrs={'class':'w'})[i].text

    #get inflation mom
    kurs=table.find_all('span',attrs={'class':'w'})[i].text

    temp.append((tanggal,kurs))


temp = temp[::-1]

#change into dataframe
data = pd.DataFrame(temp,columns=('tanggal','kurs'))

#insert data wrangling here
#Mengubah data atribut kurs
data['kurs']=data['kurs'].astype('string')
data['kurs']=data['kurs'].str.replace("1 USD = "," ")
data['kurs']=data['kurs'].str.replace(" IDR"," ")
data['kurs']=data['kurs'].str.replace(",","")
data['kurs']=data['kurs'].astype('int')
data['tanggal']=data['tanggal'].astype('datetime64[ns]')
data=data.set_index('tanggal')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{data["kurs"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = data.plot(figsize = (10,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]
     
	

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)



if __name__ == "__main__": 
    app.run(debug=True)