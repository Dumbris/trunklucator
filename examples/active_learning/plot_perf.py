import matplotlib as mpl
import matplotlib.pyplot as plt
from io import BytesIO
import base64
mpl.use('Agg')

def plot_performance(performance_history):
    fig, ax = plt.subplots(figsize=(8.5, 6), dpi=130)

    ax.plot(performance_history)
    ax.scatter(range(len(performance_history)), performance_history, s=13)

    ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(nbins=5, integer=True))
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(nbins=10))
    ax.yaxis.set_major_formatter(mpl.ticker.PercentFormatter(xmax=1))

    ax.set_ylim(bottom=0, top=1)
    ax.grid(True)

    ax.set_title('Incremental classification accuracy')
    ax.set_xlabel('Query iteration')
    ax.set_ylabel('Classification Accuracy')

    image = BytesIO()
    plt.plot()
    plt.savefig(image, format='png')
    plt.cla()
    plt.close(fig)
    return ''' <img src="data:image/png;base64,{}" border="0" /> '''.format(base64.encodebytes(image.getvalue()).decode())

