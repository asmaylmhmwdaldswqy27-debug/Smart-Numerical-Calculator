import tkinter as tk
from tkinter import ttk, messagebox
from methods import compute_nonlinear, compute_linear, compute_errors

def run_nonlinear():
    tree_nl.delete(*tree_nl.get_children())
    try:
        steps, res = compute_nonlinear(ent_eq.get(), ent_x0.get(), ent_tol.get(), cmb_nl.get())
        for row in steps: tree_nl.insert("", "end", values=row)
        lbl_res_nl.config(text=res)
    except Exception as e: messagebox.showerror("Error", str(e))

def run_linear():
    tree_lin.delete(*tree_lin.get_children())
    try:
        A = [[float(e[j].get()) for j in range(3)] for e in entries_A]
        b = [float(eb.get()) for eb in entries_b]
        steps, res = compute_linear(A, b, float(ent_lin_tol.get()), cmb_lin.get())
        for row in steps: tree_lin.insert("", "end", values=row)
        lbl_res_lin.config(text=res)
    except Exception as e: messagebox.showerror("Error", str(e))

def run_errors():
    try:
        lbl_res_err.config(text=compute_errors(float(ent_true.get()), float(ent_approx.get())))
    except Exception as e: messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Smart Numerical Calculator")
root.geometry("880x600")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# --- Tab 1: Nonlinear ---
tab1 = ttk.Frame(notebook, padding=10)
notebook.add(tab1, text=" 1. Nonlinear Equations ")

f1 = ttk.Frame(tab1); f1.pack(fill="x", pady=5)
cmb_nl = ttk.Combobox(f1, values=["Newton-Raphson Method", "Simple Iteration"], state="readonly", width=22); cmb_nl.current(0); cmb_nl.pack(side="left", padx=5)
ent_eq = ttk.Entry(f1, width=18); ent_eq.insert(0, "x**3 - 7*x + 1"); ent_eq.pack(side="left", padx=5)
ent_x0 = ttk.Entry(f1, width=8); ent_x0.insert(0, "-2.8"); ent_x0.pack(side="left", padx=5)
ent_tol = ttk.Entry(f1, width=8); ent_tol.insert(0, "0.0005"); ent_tol.pack(side="left", padx=5)
tk.Button(f1, text="Calculate", bg="#2563EB", fg="white", command=run_nonlinear).pack(side="left", padx=10)

lbl_res_nl = tk.Label(tab1, text="Result", bg="#DCFCE7", fg="#166534", font=("Segoe UI", 10, "bold"), pady=6)
lbl_res_nl.pack(fill="x", pady=5)

tree_nl = ttk.Treeview(tab1, columns=("n", "x_n", "fx", "x_next", "err"), show="headings")
for col, t in zip(tree_nl["columns"], ["n", "x_n", "f(x_n)", "x_{n+1}", "Error"]):
    tree_nl.heading(col, text=t); tree_nl.column(col, anchor="center", width=150)
tree_nl.pack(fill="both", expand=True)


tab2 = ttk.Frame(notebook, padding=10)
notebook.add(tab2, text=" 2. Linear Systems ")

f2 = ttk.Frame(tab2); f2.pack(fill="x", pady=5)
cmb_lin = ttk.Combobox(f2, values=["Jacobi Method", "Gauss-Seidel Method"], state="readonly", width=20); cmb_lin.current(0); cmb_lin.pack(side="left", padx=5)
ent_lin_tol = ttk.Entry(f2, width=10); ent_lin_tol.insert(0, "0.0005"); ent_lin_tol.pack(side="left", padx=5)
tk.Button(f2, text="Solve", bg="#2563EB", fg="white", command=run_linear).pack(side="left", padx=10)

m_frame = ttk.Frame(tab2); m_frame.pack(pady=5)
entries_A, entries_b = [], []
def_A, def_b = [[15, 3, -2], [2, 10, 1], [1, -2, 8]], [85, 51, 5]
for i in range(3):
    row_e = []
    for j in range(3):
        e = ttk.Entry(m_frame, width=6, justify="center"); e.insert(0, str(def_A[i][j])); e.grid(row=i, column=j*2, padx=2, pady=2)
        row_e.append(e)
        if j < 2: ttk.Label(m_frame, text="+").grid(row=i, column=j*2+1)
    entries_A.append(row_e)
    ttk.Label(m_frame, text="=").grid(row=i, column=6)
    eb = ttk.Entry(m_frame, width=6, justify="center"); eb.insert(0, str(def_b[i])); eb.grid(row=i, column=7, padx=2)
    entries_b.append(eb)

lbl_res_lin = tk.Label(tab2, text="Result", bg="#DCFCE7", fg="#166534", font=("Segoe UI", 10, "bold"), pady=6)
lbl_res_lin.pack(fill="x", pady=5)

tree_lin = ttk.Treeview(tab2, columns=("k", "x", "y", "z", "err"), show="headings")
for col, t in zip(tree_lin["columns"], ["k", "x", "y", "z", "Max Error"]):
    tree_lin.heading(col, text=t); tree_lin.column(col, anchor="center", width=150)
tree_lin.pack(fill="both", expand=True)


tab3 = ttk.Frame(notebook, padding=20)
notebook.add(tab3, text=" 3. Error Analysis ")

f3 = ttk.Frame(tab3); f3.pack(anchor="w", pady=5)
ttk.Label(f3, text="True Value:").grid(row=0, column=0, sticky="w", pady=5)
ent_true = ttk.Entry(f3, width=15); ent_true.insert(0, "10000"); ent_true.grid(row=0, column=1, padx=10)
ttk.Label(f3, text="Approx Value:").grid(row=1, column=0, sticky="w", pady=5)
ent_approx = ttk.Entry(f3, width=15); ent_approx.insert(0, "9999"); ent_approx.grid(row=1, column=1, padx=10)
tk.Button(f3, text="Calculate", bg="#2563EB", fg="white", command=run_errors).grid(row=2, column=0, columnspan=2, pady=10)

lbl_res_err = tk.Label(tab3, text="Result", bg="#DCFCE7", fg="#166534", font=("Segoe UI", 10, "bold"), pady=8, padx=10)
lbl_res_err.pack(fill="x", pady=10)

root.mainloop()
