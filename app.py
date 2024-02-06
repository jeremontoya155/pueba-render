from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'excelFile' not in request.files:
            return 'No se ha seleccionado ningún archivo'
        
        file = request.files['excelFile']
        
        if file.filename == '':
            return 'No se ha seleccionado ningún archivo'
        
        if file:
            try:
                df = pd.read_excel(file)
                table_html = df.to_html(classes='table table-striped')
                return render_template('index.html', table=table_html)
            except Exception as e:
                return f'Ocurrió un error al procesar el archivo: {e}'
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
