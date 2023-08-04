from tkinter import * 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

jaw = 0
pitch = 0
roll = 0
x = 0
y = 0
z = 0

points_base = np.array([
                        [-1, -0.2, 0],  #a1
                        [-1, 0.2, 0],  #a2

                        [0.8, 1, 0],  #a3
                        [1.2, 1, 0],  #a4

                        [1.2, -1, 0],  #a5
                        [0.8, -1, 0]   #a6
                        ])    

points_platform = np.array([    
                            [-1, -0.2, 3],  #b1
                            [-1, 0.2, 3],  #b2

                            [0.8, 1, 3],  #b3
                            [1.2, 1, 3],  #b4

                            [1.2, -1, 3],  #b5
                            [0.8, -1, 3]   #b6
                            ])    

def plot_points(ax, points, color):
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], color=color)

def plot_connecting_lines(ax, points, color):
    for i in range(len(points)):
        ax.plot([points[i, 0], points[i-1, 0]], [points[i, 1], points[i-1, 1]], [points[i, 2], points[i-1, 2]], color=color)

def plot_base(ax, points):
    plot_points(ax, points, 'red')
    plot_connecting_lines(ax, points, 'red')

def plot_platform(ax, points):
    plot_points(ax, points, 'blue')
    plot_connecting_lines(ax, points, 'blue')

def find_center(points):
    return np.mean(points, axis=0)

def apply_rotations_centered(points, jaw, pitch, roll):
    center = find_center(points)

    points[:, 0] -= center[0]
    points[:, 1] -= center[1]
    points[:, 2] -= center[2]

    points = apply_rotations(points, jaw, pitch, roll)

    points[:, 0] += center[0]
    points[:, 1] += center[1]
    points[:, 2] += center[2]

    return points

def apply_rotations(points, jaw, pitch, roll):
    # jaw
    rot_matrix = np.array([
                            [np.cos(np.deg2rad(jaw)), -np.sin(np.deg2rad(jaw)), 0],
                            [np.sin(np.deg2rad(jaw)), np.cos(np.deg2rad(jaw)), 0],
                            [0, 0, 1]
                            ])
    points = np.matmul(points, rot_matrix)

    # pitch
    rot_matrix = np.array([
                            [np.cos(np.deg2rad(pitch)), 0, np.sin(np.deg2rad(pitch))],
                            [0, 1, 0],
                            [-np.sin(np.deg2rad(pitch)), 0, np.cos(np.deg2rad(pitch))]
                            ])
    points = np.matmul(points, rot_matrix)

    # roll
    rot_matrix = np.array([
                            [1, 0, 0],
                            [0, np.cos(np.deg2rad(roll)), -np.sin(np.deg2rad(roll))],
                            [0, np.sin(np.deg2rad(roll)), np.cos(np.deg2rad(roll))]
                            ])
    points = np.matmul(points, rot_matrix)

    return points

def apply_translations(points, x, y, z):
    points[:, 0] += x
    points[:, 1] += y
    points[:, 2] += z

    return points

def plot_3d():
    global ax

    points_platform_rot = apply_rotations_centered(points_platform, jaw, pitch, roll)
    points_platform_rot_trans = apply_translations(points_platform_rot, x, y, z)

    ax.clear()

    ax.set_xlim3d(-1, 2)
    ax.set_ylim3d(-1, 2)
    ax.set_zlim3d(-1, 2)

    plot_base(ax, points_base)
    plot_platform(ax, points_platform_rot_trans)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

def redraw_all():
    global ax
    global canvas
    global toolbar

    plot_3d()
    canvas.draw()
    toolbar.update()

def init_window():
    global root
    global ax
    global canvas
    global toolbar

    fig = Figure(figsize=(5, 5), dpi=100)
    ax = fig.add_subplot(111, projection='3d')

    plot_3d()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack()

    frame = Frame(root, name="points_base_frame_root")
    tk_draw_textboxes_points_base(frame)
    frame.pack(side=LEFT)

    frame = Frame(root, name="points_platform_frame_root")
    tk_draw_textboxes_points_platform(frame)
    frame.pack(side=LEFT)

    frame = Frame(root, name="rot_frame_root")
    tk_draw_sliders_rot(frame)
    frame.pack(side=LEFT)

    frame = Frame(root, name="trams_frame_root")
    tk_draw_sliders_trams(frame)
    frame.pack(side=LEFT)


def tk_draw_textboxes_points_base(frame):
    global points_base

    label = Label(frame, text="Points of the base")
    label.pack()

    for i in range(len(points_base)):
        sub_frame = Frame(frame, name=f"points_base_frame{i}")
        sub_frame.pack()

        label = Label(sub_frame, text=f"a{i}: ")
        label.pack(side=LEFT)

        for j in range(3):
            inp = Entry(sub_frame, width=10, name=f"inp{i}{j}")
            inp.pack(side=LEFT)  # Pack the text fields horizontally inside the frame
            inp.insert(END, points_base[i, j])

    btn = Button(frame, text="Update", command=tk_update_points)
    btn.pack()

def tk_draw_textboxes_points_platform(frame):
    #global points_platform

    label = Label(frame, text="Points of the platform")
    label.pack()

    for i in range(len(points_platform)):
        sub_frame = Frame(frame, name=f"points_platform_frame{i}")
        sub_frame.pack()

        label = Label(sub_frame, text=f"b{i}: ")
        label.pack(side=LEFT)

        for j in range(3):
            inp = Entry(sub_frame, width=10, name=f"inp{i}{j}")
            inp.pack(side=LEFT)  # Pack the text fields horizontally inside the frame
            inp.insert(END, points_platform[i, j])

    btn = Button(frame, text="Update", command=tk_update_points)
    btn.pack()

def tk_draw_sliders_rot(frame):
    global jaw
    global pitch
    global roll

    label = Label(frame, text="Jaw")
    label.pack()
    slider = Scale(frame, from_=-90, to=90, orient=HORIZONTAL, command=tk_update_jaw)
    slider.pack()

    label = Label(frame, text="Pitch")
    label.pack()
    slider = Scale(frame, from_=-90, to=90, orient=HORIZONTAL, command=tk_update_pitch)
    slider.pack()

    label = Label(frame, text="Roll")
    label.pack()
    slider = Scale(frame, from_=-90, to=90, orient=HORIZONTAL, command=tk_update_roll)
    slider.pack()

def tk_draw_sliders_trams(frame):
    global x
    global y
    global z

    label = Label(frame, text="X")
    label.pack()
    slider = Scale(frame, from_=-5, to=5, orient=HORIZONTAL, command=tk_update_x)
    slider.pack()

    label = Label(frame, text="Y")
    label.pack()
    slider = Scale(frame, from_=-5, to=5, orient=HORIZONTAL, command=tk_update_y)
    slider.pack()

    label = Label(frame, text="Z")
    label.pack()
    slider = Scale(frame, from_=-5, to=5, orient=HORIZONTAL, command=tk_update_z)
    slider.pack()

def tk_update_jaw(val):
    global jaw
    jaw = float(val)
    redraw_all()

def tk_update_pitch(val):
    global pitch
    pitch = float(val)
    redraw_all()

def tk_update_roll(val):
    global roll
    roll = float(val)
    redraw_all()

def tk_update_x(val):
    global x
    x = float(val)
    redraw_all()

def tk_update_y(val):
    global y
    y = float(val)
    redraw_all()

def tk_update_z(val):
    global z
    z = float(val)
    redraw_all()

def tk_update_points():
    global points_base
    global points_platform
    global root

    root_frame = root.children["points_base_frame_root"]

    for i in range(len(points_base)):
        frame = root_frame.children[f"points_base_frame{i}"]
        for j in range(3):
            points_base[i, j] = float(frame.children[f"inp{i}{j}"].get())

    root_frame = root.children["points_platform_frame_root"]

    for i in range(len(points_platform)):
        frame = root_frame.children[f"points_platform_frame{i}"]
        for j in range(3):
            points_platform[i, j] = float(frame.children[f"inp{i}{j}"].get())

    redraw_all()

if __name__ == "__main__":
    root = Tk()
    root.title("6DOF Motion Simulator")
    root.geometry("1000x1000")
    init_window()
    root.mainloop()