# app.py

import sys
from tkinter import Tk
from frontend.main_ui import DynamicMemoryVisualizerApp
from flask_app import app

def run_tkinter():
    root = Tk()
    app = DynamicMemoryVisualizerApp(root)
    root.mainloop()

def run_flask():
    app.run(debug=True)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--web":
        run_flask()
    else:
        run_tkinter()