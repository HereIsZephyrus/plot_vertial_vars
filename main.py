from plot import init_plot, generate_ax_func, plot_window_elements
from interface import construct_data, Data
import matplotlib.pyplot as plt

def main(data: Data):
    fig = init_plot()
    funcs, params = generate_ax_func(fig, data.pressure, data.variables)
    
    for func, param in zip(funcs, params):
        func(param)
    
    plot_window_elements(fig, data.info)
    plt.savefig('sounding_plot.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("图像已保存到 sounding_plot.png")

if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 2):
        print("Usage: python main.py <data_json>")
        sys.exit(1)
    if isinstance(sys.argv[1], Data):
        main(sys.argv[1])
    else:
        main(construct_data(sys.argv[1]))