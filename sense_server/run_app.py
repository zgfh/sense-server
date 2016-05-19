from sense_server.app import app
import sense_server.core.route

if __name__ == '__main__':
    app.debug = True
    app.run("0.0.0.0", 3000)
