import tkinter as tk




def show_about(root):
    about_window = tk.Toplevel(root)  # Create a new top-level window
    about_window.title("About This Program")
    about_window.geometry("500x300")  # Set size of the About window
    
    # Add some text inside the About window
    label = tk.Label(about_window, text="1st Project in Advanced Topics in Antennas\n\nCreated by: Toutoudakis Emmanouil\n\nMTP330", font=("Arial", 12))
    label.pack(pady=20)
    # Styled Close Button
    close_button = tk.Button(
        about_window,
        text="Close",
        font=("Arial", 12, "bold"),
        fg="white",
        bg="blue",
        padx=10,
        pady=5,
        borderwidth=3,
        relief="raised",
        command=about_window.destroy  # Closes the About window
        
    )
    close_button.pack(pady=10)