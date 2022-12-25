import sys

import numpy as np
import itertools as iter
from tkinter import *
import matplotlib.pyplot as plt
import networkx as nx


def leave():
    sys.exit(0)


def click_1():
    def enter_graph():
        def read_matrix():
            G = [[0] * n for l in range(n)]

            for k in range(n):
                for m in range(n):
                    G[k][m] = int(txts[k][m].get())

            frame3.destroy()
            find_autos(G, n)

        n = int(txt.get())
        frame2.destroy()
        frame3 = Frame(master=window)
        frame3.pack()
        lbl3 = Label(frame3, text="Введите граф: ", font=("Arial Bold", 12))
        lbl3.grid(column=0, row=0)
        txts = [[] * n for o in range(n)]
        btn3 = Button(frame3, text="Далее", command=read_matrix)
        btn3.grid(column=n + 1, row=0)

        for i in range(n):
            for j in range(n):
                txt2 = Entry(frame3, width=3)
                txt2.grid(column=j + 1, row=i)
                txts[i].append(txt2)

    frame.destroy()
    frame2 = Frame(master=window)
    frame2.pack()
    txt = Entry(frame2, width=5)
    txt.grid(column=1, row=0)
    lbl2 = Label(frame2, text="Введите колличество вершин: ", font=("Arial Bold", 12))
    lbl2.grid(column=0, row=0)
    btn3 = Button(frame2, text="Далее", command=enter_graph)
    btn3.grid(column=2, row=0)


def find_autos(G2, g_size):
    def try_perm(p):
        nonlocal G
        nonlocal lbls
        usedVertexes = ""
        p_size = len(p)
        P = [[0] * p_size for i in range(p_size)]
        k = 1

        for i in range(p_size):
            P[i][p[i] - 1] = 1

        for j in range(p_size):
            if (p[j] != k) and ((f"{p[j]},{k}" in usedVertexes) == False):
                usedVertexes += f"({k},{p[j]})"
            elif (p[j] == k) and ((f"{p[j]}" in usedVertexes) == False):
                usedVertexes += f"({p[j]})"
            k += 1

        PT = np.transpose(P)
        PTG = np.dot(PT, G)
        FIN = np.dot(PTG, P)

        if (FIN == G).all():
            lbl2 = Label(frame2, text=usedVertexes, font=("Arial Bold", 12))
            lbls.append(lbl2)
            print(usedVertexes)

    G = [[0] * g_size for i in range(g_size)]
    p = []
    lbls = []
    frame2 = Frame(master=window)

    for i in range(g_size):
        p.append(i + 1)
        G[i] = G2[i]

    perm_set = iter.permutations(p)

    for h in perm_set:
        try_perm(h)

    d = 0
    for h in lbls:
        h.grid(column=1, row=d)
        d += 1

    frame2.pack()


def click_2():
    def read_autos():
        def send_autos():
            groups = []

            for j in range(n):
                groups.append(txts[i].get())

            frame3.destroy()
            find_graph(n, groups)

        n = int(txt.get())
        frame3 = Frame(master=window)
        frame2.destroy()
        frame3.pack()
        lbl2 = Label(frame3, text="Введите автоморфизмы: ")
        lbl2.grid(column=0, row=0)
        btn1 = Button(frame3, text="Далее", command=send_autos)
        btn1.grid(column=2, row=0)
        txts = []

        for i in range(n):
            txt2 = Entry(frame3, width=15)
            txt2.grid(column=1, row=i)
            txts.append(txt2)

    frame2 = Frame(master=window)
    frame.destroy()
    frame2.pack()
    txt = Entry(frame2, width=5)
    txt.grid(column=1, row=0)
    lbl4 = Label(frame2, text="Введите количество автоморфизмов: ", font=("Arial Bold", 12))
    lbl4.grid(column=0, row=0)
    btn3 = Button(frame2, text="Далее", command=read_autos)
    btn3.grid(column=2, row=0)


def find_graph(groups_count, groups_strs):
    graph = []
    g = nx.Graph()
    graph_size = 0  # Просто максимальное число
    perms = []  # массив перестановок
    groups = []

    for i in range(groups_count):
        group = groups_strs[i]
        group = group.replace(')(', ' ')
        group = group.replace('(', '')
        group = group.replace(')', '  ')
        gan = list(group)
        # print(max(gan))
        automorphism = [0] * int(max(gan))

        for j in range(len(group) - 2):
            if group[j + 1] == ',':
                automorphism[int(group[j]) - 1] = int(group[j + 2])

                if f"{group[j + 2]}," in group:
                    continue
                else:
                    automorphism[int(group[j + 2]) - 1] = int(group[j])

            elif group[j + 1] == ' ' and group[j - 1] != ',':
                automorphism[int(group[j]) - 1] = int(group[j])

        groups.append(automorphism)
        print(groups[j])


    matrix_array = []
    is_graph_not_found = True
    group_size = max(group)
    graph_size = int(group_size)


    for i in range(groups_count):
        array = [[0] * graph_size for k in range(graph_size)]

        for k in range(graph_size):
            x = groups[i][k]
            array[x - 1][k] = 1

        matrix_array.append(array)

    mxn = np.arange(graph_size * graph_size).reshape(graph_size, graph_size)

    for i in range(2 ** (graph_size * graph_size)):
        if is_graph_not_found:
            arr = (i >> mxn) % 2
            degree = [0] * graph_size
            graph_is_ok = True
            fool = 0

            for j in range(graph_size):
                fool += sum(arr[j])

            if fool % 2 != 0:
                graph_is_ok = False

            if not graph_is_ok:
                continue

            for j in range(graph_size):
                countOne = 0
                countOne += sum(arr[j])

                if countOne < 1 or countOne > graph_size:
                    graph_is_ok = False

            if not graph_is_ok:
                continue

            for j in range(graph_size):
                for k in range(graph_size):
                    if arr[j][k] == 1:
                        if arr[k][j] != 1:
                            graph_is_ok = False

            if not graph_is_ok:
                continue

            for j in range(graph_size):
                if arr[j][j]:
                    graph_is_ok = False

            if not graph_is_ok:
                continue

            countDegree = 0

            for j in range(graph_size):
                degree[j] += sum(arr[j])

                if degree[j] % 2 != 0:
                    countDegree += 1

            if countDegree % 2 != 0:
                graph_is_ok = False

            if not graph_is_ok:
                continue

            if graph_is_ok:
                for j in range(graph_size):
                    degree[j] += sum(arr[j])

                for j in range(groups_count):
                    for k in range(graph_size):
                        if degree[groups[j][k] - 1] != degree[k]:
                            graph_is_ok = False

            if not graph_is_ok:
                continue

            if graph_is_ok:
                for j in range(graph_size):
                    degree[j] += sum(arr[j])

                if graph_is_ok:
                    degree1 = [0] * graph_size

                    for j in range(groups_count):
                        P = matrix_array[j]
                        PT = np.transpose(P)
                        PTG = np.dot(PT, arr)
                        FIN = np.dot(PTG, P)

                        if (FIN != arr).all():
                            graph_is_ok = False

            if graph_is_ok:
                graph = arr
                # for k in range(graph_size):
                #    print(arr[k])
                is_graph_not_found = False

    for i in range(graph_size):
        for j in range(graph_size):
            if graph[i][j] == 1:
                g.add_edge(i, j)
            print(str(graph[i][j]) + ' ')
        print('\n')

    nx.draw(g)
    plt.savefig("filename.png")
    frame4 = Frame(master=window)
    frame4.pack()
    img = PhotoImage(file='filename.png')
    panel = Label(frame4, image=img)
    panel.grid(column=0, row=0)
    btn3 = Button(frame4, text="ВЫХОД", command=leave)
    btn3.grid(column=0, row=1)

    window.mainloop()


window = Tk()
window.title("Альтернативный экзамен студентов из 1305")
window.geometry('600x400')
frame = Frame(master=window)
frame.pack()

lbl = Label(frame, text="Автоморфизмы", font=("Arial Bold", 12))
lbl.grid(column=1, row=2)
lbl2 = Label(frame, text=" графа", font=("Arial Bold", 12))
lbl2.grid(column=2, row=2)
btn = Button(frame, text="Построить граф", command=click_2)
btn.grid(column=2, row=3)
btn2 = Button(frame, text="Найти все автоморфизмы", command=click_1)
btn2.grid(column=1, row=3)

window.mainloop()
