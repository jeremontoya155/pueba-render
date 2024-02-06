from flask import Flask, render_template, request, send_file
import pandas as pd
import tabula

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No se ha seleccionado ningún archivo'
        
        file = request.files['file']
        
        if file.filename == '':
            return 'No se ha seleccionado ningún archivo'
        
        if file:
            try:
                if file.filename.endswith('.xlsx'):
                    df = pd.read_excel(file)
                elif file.filename.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.filename.endswith('.txt'):
                    df = pd.read_csv(file, sep='\t')
                elif file.filename.endswith('.pdf'):
                    tables = tabula.read_pdf(file)
                    df = pd.concat(tables)
                else:
                    return 'Formato de archivo no válido'
                
                table_html = df.to_html(classes='table table-striped')
                return render_template('index.html', table=table_html)
            except Exception as e:
                return f'Ocurrió un error al procesar el archivo: {e}'
    
    return render_template('index.html')

@app.route('/download')
def download():
    # Obtener los datos de la tabla
    table_data = request.args.get('table_data', '')
    
    # Crear un DataFrame de Pandas a partir de los datos de la tabla
    df = pd.read_html(table_data)[0]
    
    # Guardar el DataFrame como archivo Excel
    excel_file = 'table_data.xlsx'
    df.to_excel(excel_file, index=False)
    
    # Devolver el archivo Excel como una respuesta de descarga
    return send_file(excel_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
