import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog

def plot_result(frame, distances, losses, title):
    for widget in frame.winfo_children():
        widget.destroy()

    fig = plt.Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(distances, losses, label="Path Loss (dB)", color='blue')
    ax.set_xlabel("Distance")
    ax.set_ylabel("Path Loss (dB)")
    ax.set_title(title)
    ax.grid(True)
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # Attach save button
    def save_plot():
        file = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png")])
        if file:
            fig.savefig(file)

    return save_plot
