import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 1. Setup the figure and axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Left plot: The Locus (Coordinate Plane)
ax1.set_xlim(-1, 1)
ax1.set_ylim(-1, 1)
ax1.set_aspect('equal')
ax1.set_title("The Locus (Path of x and y)")
ax1.grid(True)
line, = ax1.plot([], [], 'g-', alpha=0.3)  # The trail
point, = ax1.plot([], [], 'ro')            # The current (x, y) point

# Right plot: The Chart (Data readout)
ax2.axis('off')
table_text = ax2.text(0.1, 0.5, '', fontsize=12, family='monospace')

# Data storage
x_data, y_data = [], []

def update(a):
    # The "Code" for x and y
    x = (3/4) * np.cos(3 * a)
    y = -(3/4) * np.sin(3 * a)
   
    x_data.append(x)
    y_data.append(y)
   
    # Update the animation
    line.set_data(x_data, y_data)
    point.set_data([x], [y])
   
    # Update the Real-Time Chart
    display_text = (
        f"Time (a): {a:.2f}\n\n"
        f"X-Position (Left/Right): {x: .4f}\n"
        f"Y-Position (Up/Down):    {y: .4f}\n\n"
        f"Rule: x² + y² = (3/4)²\n"
        f"Check: {x**2 + y**2:.4f} = 0.5625"
    )
    table_text.set_text(display_text)
   
    return line, point, table_text

# Animate over 'a' from 0 to 2*pi
ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 120),
                    interval=50, blit=True)

plt.tight_layout()
plt.show()
