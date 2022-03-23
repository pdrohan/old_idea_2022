from Website import create_app


app = create_app()


#only if we run this file, not if we import, are we going to execute this line
#This means you only run the webserver when this file is run

if __name__ == '__main__':
    app.run(debug=True)
