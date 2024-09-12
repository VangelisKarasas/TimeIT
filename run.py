from FlaskTimeIT import app


import pyodbc
print(pyodbc.drivers())
if __name__ == '__main__':
    app.run(debug=True)
