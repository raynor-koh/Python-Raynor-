"""
Simulation of controlling the inverted pendulum on a cart with state controller.

Equations:
	th'' = (g * sin(th) - u * cos(th)) / L,
	u = Kp_th * th + Kd_th * th' + Kp_x * (x - x0) + Kd_x * x'

System:
	th' = Y,
	Y' = (g * sin(th) - u * cos(th)) / L,
	x' = Z,
	Z' = u = Kp_th * th + Kd_th * Y + Kp_x * (x - x0) + Kd_x * Z,

State:
	[th, Y, x, Z]
"""

"""
To display root locus plot, type in root locus. For position root locus, type in x; for angle root locus, type in th.
To display pendulum simulation, type in pendulum.
"""

import numpy as np

import matplotlib
matplotlib.use('TKAgg')

# For Pendulum Simulation
import matplotlib.pyplot as pp
import scipy.integrate as integrate
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from math import pi, trunc
from numpy import sin, cos

# For Root Locus Plot
import control

# TODO: Choose constants Section
# Physical Constants
g = 9.8
L = 1.5
m = 0.5

# Controller Constants
Kp_th = 50
Kd_th = 10
Kp_x = 0
Kd_x = 2

# initial conditions
Y = .0 		# pendulum angular velocity
th = 0.1	# pendulum angle    TODO: Change depending on choice
x = .0		# cart position
x0 = 0		# desired cart position
Z = .0		# cart velocity

# Don't need touch constants
# simulation time
dt = 0.01
Tmax = 7    # CHANGE IF TAKE TOO LONG
t = np.arange(0.0, Tmax, dt)

ax = 10    # Axis Limits
precision = 0.006
k = 1000.0	# Kalman filter coefficient


# Define Functions
def trim(x, step):
    d = trunc(x / step)
    return step * d

def step(t):
	if t < 5:
		return .0
	elif t >= 5 and t < 10:
		return 1.
	elif t >= 10 and t < 15:
		return -0.5
	else:
		return .0

def derivatives(state, t):
	ds = np.zeros_like(state)
	_th = state[0]
	_Y = state[1]
	_x = state[2]
	_Z = state[3]

	# x0 = step(t)

	u = Kp_th * _th + Kd_th * _Y + Kp_x * (_x - x0) + Kd_x * _Z

	ds[0] = state[1]
	ds[1] = (g * sin(_th) - u * cos(_th)) / L
	ds[2] = state[3]
	ds[3] = u

	return ds

def init():
    line.set_data([], [])
    time_text.set_text('')
    patch.set_xy((-cart_width/2, -cart_height/2))
    patch.set_width(cart_width)
    patch.set_height(cart_height)
    return line, time_text, patch


def animate(i):
    thisx = [xs[i], pxs[i]]
    thisy = [0, pys[i]]

    line.set_data(thisx, thisy)
    time_text.set_text(time_template % (i*dt))
    patch.set_x(xs[i] - cart_width/2)
    return line, time_text, patch


start = True
print("Initialising...")
state = np.array([th, Y, x, Z, trim(th, precision), .0])
while start:
    choice = input("Root Locus or Pendulum: ").lower()

    if choice == "root locus":
        x_or_th = input("Angle (th) or positon (x): ")
        if x_or_th == 'x':
            A = [1, Kd_th / L, (Kp_th - g) / L, 0, 0]
            B = [-1, 0, g / L, 0]

            G = control.TransferFunction(B, A)
            print("Transfer Function derived. =)")
            # lists of evenly spaced gains
            Kd_x = np.linspace(1000.0, 0, num=10000)

            # compute and plot root-locus
            r_list, k_list = control.root_locus(G, kvect=Kd_x, xlim=(-ax, ax), ylim=(-ax, ax))
            print("Displaying Root Locus Plot for Position")
            pp.show()

        elif x_or_th == 'th':
            A = [1, Kd_th / L, (Kp_th - g) / L, 0, 0]
            B = [-1, 0, g / L, 0]

            G = control.TransferFunction(B, A)
            print("Transfer Function derived. =)")
            # lists of evenly spaced gains
            Kd_x = np.linspace(1000, 0, num=10000)

            # compute and plot root-locus
            r_list, k_list = control.root_locus(G, kvect=Kd_x, xlim=(-ax, ax), ylim=(-ax, ax))
            print("Displaying Root Locus Plot for Angle")
            pp.show()

    elif choice == 'pendulum':
        print("Integrating...")
        # integrate your ODE using scipy.integrate.
        solution = integrate.odeint(derivatives, state, t)

        ths = solution[:, 0]
        xs = solution[:, 2]

        pxs = L * sin(ths) + xs
        pys = L * cos(ths)

        fig = pp.figure()
        ax = fig.add_subplot(111, autoscale_on=False, xlim=(-0.5, 2.0), ylim=(-0.5, 2))
        ax.set_aspect('equal')
        ax.grid()

        patch = ax.add_patch(Rectangle((0, 0), 0, 0, linewidth=1, edgecolor='k', facecolor='g'))

        line, = ax.plot([], [], 'o-', lw=2)
        time_template = 'time = %.1fs'
        time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

        cart_width = 0.3
        cart_height = 0.2

        ani = animation.FuncAnimation(fig, animate, np.arange(1, len(solution)),
                                      interval=25, blit=True, init_func=init)

        pp.show()

    elif choice == 'end':
        print("Script has finished running.")
        start = False

    else:
        print("Sorry wrong input. Enter again.")
