#Labelling Function
def autolabel(rects,ax):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.02*height,
                '%d' % int(height),
                ha='center', va='bottom')

def balls_faced(x):
    return len(x)

def dot_balls(x):
    return (x==0).sum()