import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from compiler import Function

def plot_graph():
    try:
        if not f.set_function(entry_f.get()):
            raise ValueError("Некоректний графік.")

        a = float(entry_a.get())
        b = float(entry_b.get())
        h = float(entry_h.get())
        
        if a >= b:
            raise ValueError("Ліва межа повинна бути меншою за праву.")
        if h <= 0:
            raise ValueError("Крок має бути більшим за 0.")
        
        global x, y
        x, y = [], []
        i = a
        while i <= b:
            x.append(i)
            y.append(f(i))
            i += h
        
        cur_func.clear()
        cur_func.set_xlim(a, b)
        cur_func.axhline(0, color="black")
        cur_func.axvline(0, color="black")
        cur_func.grid(linestyle="--")
        cur_func.set_title(f"Графік функції {f.function[1:-1]}")
        cur_func.set_xlabel("x")
        cur_func.set_ylabel("y")

        cur_func.plot(x, y)
        canvas.draw()

        button_save.config(state=tk.ACTIVE)
        
    except Exception as e:
        tk.messagebox.showerror("Помилка", f"Не вдалося побудувати графік: {e}")
        button_save.config(state=tk.DISABLED)

def save():
    path = tk.filedialog.asksaveasfilename(defaultextension=".dat", filetypes=[("DAT Files", "*.dat")])
    if path:
        with open(path, 'w', encoding='utf-8') as file:
            file.write('№\tx\ty\n')
            for i in range(len(x)):
                file.write(f'{i + 1}\t{x[i]}\t{y[i]}\n')
            tk.messagebox.showinfo("Save Successful", f"Results saved to {path}")

x, y = [], []

f = Function()

main_window = tk.Tk()
main_window.title("?????")

controls = ttk.Frame(main_window)
controls.pack(padx=5, pady=5)

ttk.Label(controls, text="Функція y = f(x):").grid(row=0, column=0, padx=5, pady=5)
entry_f = ttk.Entry(controls)
entry_f.insert(0, "sin(x)")
entry_f.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(controls, text="Ліва межа:").grid(row=1, column=0, padx=5, pady=5)
entry_a = ttk.Entry(controls)
entry_a.insert(0, "-10")
entry_a.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(controls, text="Права межа:").grid(row=2, column=0, padx=5, pady=5)
entry_b = ttk.Entry(controls)
entry_b.insert(0, "10")
entry_b.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(controls, text="Крок (h):").grid(row=3, column=0, padx=5, pady=5)
entry_h = ttk.Entry(controls)
entry_h.insert(0, "0.1")
entry_h.grid(row=3, column=1, padx=5, pady=5)

ttk.Button(controls, text="Побудувати графік", command=plot_graph).grid(row=4, column=0, pady=10)

button_save = ttk.Button(controls, text="Зберегти табуляцію", command=save, state=tk.DISABLED)
button_save.grid(row=4, column=1, pady=10)

plot = tk.Frame(main_window)
plot.pack()

fig = Figure()
cur_func = fig.add_subplot()

canvas = FigureCanvasTkAgg(fig, master=plot)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

main_window.mainloop()