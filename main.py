from v2.matrix import Matrix

# ----------------------------------------------------------------
# Corps
# ----------------------------------------------------------------

m1 = Matrix(size=(3, 3))
m2 = Matrix(size=(3, 3))
m1.set_line(0, [1, 0, 1])
m1.set_line(1, [0, 1, 0])
m1.set_line(2, [1, 0, 1])
m2.set_line(0, [2, 0, 0])
m2.set_line(1, [2, 2, 1])
m2.set_line(2, [0, 0, 2])

print(m1)
print(m2)

m3 = m1*m2
print(m3)

m3 = m1+m2
print(m3)
print(m3.get([1, 2]))

# fenetre = Tk()
#
# network = nn.NeuralNetwork([2, 4, 1], 2)
# displayer = NetworkDisplayer(network, fenetre)
#
# Button(fenetre, text="Changer les poids", fg="black", bg="grey",
#        command=lambda: display(network, fenetre)).grid(column=4, row=15, padx=15, pady=15)
#
# fenetre.mainloop()
