import matplotlib.pyplot as plt

def onclick(event):
    print(event.xdata, event.ydata)

fig,ax = plt.subplots()
ax.plot(range(10))
fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()