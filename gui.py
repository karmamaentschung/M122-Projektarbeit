import tkinter as tk
from tkinter import scrolledtext
import subprocess

class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple GUI with Output Display")

        # Create a Text widget for displaying output
        self.output_text = scrolledtext.ScrolledText(root, width=50, height=10)
        self.output_text.pack(pady=10)

        # Create a button to trigger the Python script
        self.run_button = tk.Button(root, text="Run Script", command=self.run_python_script)
        self.run_button.pack()

    def run_python_script(self):
        try:
            # Run your Python script and capture the output
            script_output = subprocess.check_output(["python", "test.py"], text=True, stderr=subprocess.STDOUT)

            # Display the output in the Text widget
            self.output_text.insert(tk.END, script_output)
            self.output_text.insert(tk.END, "\n")  # Add a newline for better readability

        except subprocess.CalledProcessError as e:
            # If there is an error, display it in the Text widget
            self.output_text.insert(tk.END, f"Error: {e.output}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()
