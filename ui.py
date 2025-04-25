import tkinter as tk
from tkinter import ttk, messagebox
import models
import about_window
import utils
from graph_utils import plot_result  # Ensure you are using the correct function for plotting

MODEL_PARAMS = {
    "Outdoor": {
        "Free Space": ["Frequency (MHz)"],
        "Hata": ["Frequency (MHz)", "Base Station Height (m)", "Mobile Height (m)"],
        "Cost-231 Hata": ["Frequency (MHz)", "Base Station Height (m)", "Mobile Height (m)", "City Size (0 or 3)"],
        "Okumura": ["Frequency (MHz)", "Base Station Height (m)", "Mobile Height (m)", "Max Distance (km)", "Area Gain (dB)"],
    },
    "Indoor": {
        "ITU": ["Frequency (MHz)", "Floor Penetration Factor"],
        "Log-Distance": ["Reference Distance (m)", "Distance (m)", "Path Loss at Ref (dB)", "Path Loss Exponent"]
    }
}

def build_ui(root):
    selected_env = tk.StringVar(value="Outdoor")
    selected_model = tk.StringVar()
    entries = {}

    dark_mode = tk.BooleanVar(value=False)  # <-- Add this line

    def apply_theme():
        bg = "#1e1e1e" if dark_mode.get() else "SystemButtonFace"
        fg = "white" if dark_mode.get() else "black"
        entry_bg = "#2e2e2e" if dark_mode.get() else "white"

        # Apply theme to the main layout parts
        canvas.config(bg=bg)
        scroll_frame.config(bg=bg)
        center_frame.config(bg=bg)
        input_frame.config(bg=bg)
        plot_frame.config(bg=bg)
        root.config(bg=bg)

        for widget in center_frame.winfo_children() + input_frame.winfo_children() + plot_frame.winfo_children():
            try:
                widget.config(bg=bg, fg=fg)
            except:
                pass
            if isinstance(widget, tk.Entry):
                widget.config(bg=entry_bg, fg=fg, insertbackground=fg)

    def toggle_dark_mode():
        dark_mode.set(not dark_mode.get())
        apply_theme()


    def validate_input(P):
        """Validate if the entered text is a valid float number or empty string."""
        if P == "" or P.replace('.', '', 1).isdigit():
            return True
        else:
            return False

    def update_model_options(*_):
        model_menu['menu'].delete(0, 'end')
        selected_model.set("")
        for m in MODEL_PARAMS[selected_env.get()]:
            model_menu['menu'].add_command(label=m, command=tk._setit(selected_model, m, update_fields))

    def update_fields(*_):
        for widget in input_frame.winfo_children():
            widget.destroy()
        entries.clear()
        model = selected_model.get()
        if model:
            for param in MODEL_PARAMS[selected_env.get()][model]:
                label = tk.Label(input_frame, text=param)
                vcmd = root.register(validate_input)
                entry = tk.Entry(input_frame, validate="key", validatecommand=(vcmd, "%P"))
                label.pack()
                entry.pack()
                entries[param] = entry

    def calculate():
        try:
            user_inputs = {k: float(e.get()) for k, e in entries.items() if e.get() != ""}
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values in all fields.")
            return

        model = selected_model.get()
        env = selected_env.get()

        try:
            if env == "Outdoor":
                if model == "Free Space":
                    d, l = models.free_space(user_inputs["Frequency (MHz)"])
                elif model == "Hata":
                    d, l = models.hata(user_inputs["Frequency (MHz)"], user_inputs["Base Station Height (m)"], user_inputs["Mobile Height (m)"])
                elif model == "Cost-231 Hata":
                    d, l = models.cost231_hata(user_inputs["Frequency (MHz)"], user_inputs["Base Station Height (m)"],
                                               user_inputs["Mobile Height (m)"], user_inputs["City Size (0 or 3)"])
                elif model == "Okumura":
                    d, l = models.okumura(
                        user_inputs["Frequency (MHz)"],
                        user_inputs["Base Station Height (m)"],
                        user_inputs["Mobile Height (m)"],
                        user_inputs["Max Distance (km)"],
                        user_inputs["Area Gain (dB)"]
                    )
            elif env == "Indoor":
                if model == "ITU":
                    d, l = models.itu_indoor(user_inputs["Frequency (MHz)"], user_inputs["Floor Penetration Factor"])
                elif model == "Log-Distance":
                    d, l = models.log_distance(user_inputs["Reference Distance (m)"], user_inputs["Distance (m)"],
                                               user_inputs["Path Loss at Ref (dB)"], user_inputs["Path Loss Exponent"])

            save_fn = plot_result(plot_frame, d, l, f"{model} - {env}")
            save_btn.config(command=save_fn, state="normal")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_inputs():
        for entry in entries.values():
            entry.delete(0, tk.END)

    def reset_selection():
        selected_env.set("Outdoor")
        update_model_options()
        selected_model.set("")
        update_fields()

    def toggle_plot():
        if plot_frame.winfo_viewable():
            plot_frame.pack_forget()
        else:
            plot_frame.pack(fill="both", expand=True, padx=50, pady=10)

    # ----- MENU BAR -----
    menu_bar = tk.Menu(root)

    # File Menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open PDF Report", command=lambda: utils.open_pdf("report.pdf"))
    file_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Edit Menu
    edit_menu = tk.Menu(menu_bar, tearoff=0)
    edit_menu.add_command(label="Clear Inputs", command=clear_inputs)
    edit_menu.add_command(label="Reset Selections", command=reset_selection)
    menu_bar.add_cascade(label="Edit", menu=edit_menu)

    # View Menu
    view_menu = tk.Menu(menu_bar, tearoff=0)
    view_menu.add_command(label="Show/Hide Plot", command=toggle_plot)
    view_menu.add_checkbutton(label="Toggle Dark Mode", onvalue=True, offvalue=False, variable=dark_mode, command=toggle_dark_mode)
    menu_bar.add_cascade(label="View", menu=view_menu)

    # About Menu
    menu_bar.add_command(label="About", command=lambda: about_window.show_about(root))

    root.config(menu=menu_bar)

    # --- SCROLLABLE WRAPPER SETUP ---
    canvas = tk.Canvas(root, borderwidth=0, height=720)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    scroll_frame = tk.Frame(canvas)
    scroll_window = canvas.create_window((0, 0), window=scroll_frame, anchor="n")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas_width = event.width
        canvas.itemconfig(scroll_window, width=canvas_width)

    scroll_frame.bind("<Configure>", on_configure)
    canvas.bind("<Configure>", on_configure)
    canvas.configure(yscrollcommand=scrollbar.set)

    center_frame = tk.Frame(scroll_frame, width=800)
    center_frame.pack(pady=20)

    # UI Setup
    tk.Label(center_frame, text="Select Environment:").pack(anchor="w", padx=10, pady=(10, 0))
    ttk.OptionMenu(center_frame, selected_env, selected_env.get(), *MODEL_PARAMS.keys(), command=update_model_options).pack(padx=10, fill="x")

    tk.Button(root, text="Help (Open PDF)", bg="gray", fg="white", font=("Arial", 10, "bold"),
              command=lambda: utils.open_pdf("report.pdf")).pack(pady=5)

    tk.Label(center_frame, text="Select Propagation Model:").pack(anchor="w", padx=10, pady=(10, 0))
    model_menu = ttk.OptionMenu(center_frame, selected_model, "")
    model_menu.pack(padx=10, fill="x")

    input_frame = tk.Frame(center_frame)
    input_frame.pack(pady=10, fill="x", padx=10)

    tk.Button(center_frame, text="Calculate", bg="blue", fg="white", font=("Arial", 12, "bold"), command=calculate).pack(pady=10)

    global plot_frame
    plot_frame = tk.Frame(center_frame, width=800, height=500)
    plot_frame.pack(fill="both", expand=True, padx=50, pady=10)
    plot_frame.pack_propagate(False)

    global save_btn
    save_btn = tk.Button(center_frame, text="Save Graph", state="disabled", bg="green", fg="white")
    save_btn.pack(pady=10)

    update_model_options()
