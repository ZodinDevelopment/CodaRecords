import tkinter as tk


root = tk.Tk()

v = tk.IntVar()

v.set(1)

waves = [
        ('sine', 1),
        ('triangle', 2),
        ('sawtooth', 3),
        ('square', 4)
]

def showChoice():
    print(v.get())


tk.Label(root, text="Make a choice", justify=tk.LEFT, padx=20).pack()

for val, wave in enumerate(waves):
    tk.Radiobutton(root,
                   text=wave,
                   padx=20,
                   variable=v,
                   command=showChoice,
                   value=val).pack(anchor=tk.W)

root.mainloop()
