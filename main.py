import eel

if __name__ == '__main__':
    eel.init('static_web_folder', allowed_extensions=['.js', '.html'],)
    eel.start(
        'templates/main.html',
        jinja_templates='templates',
        mode='chrome',
        size=(720, 480),
        position=(0,0)
    )