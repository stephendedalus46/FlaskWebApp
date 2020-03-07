from flaskblog import create_app  # intead of importing app

app = create_app()  # can pass in configuration as an argument, but it uses config_class as it's default(from init file)

if __name__ == '__main__':
    app.run(debug=True)
