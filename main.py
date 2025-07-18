from plot import init_plot, generate_ax_func, plot_window_elements
from interface import construct_data, Data
import matplotlib.pyplot as plt
import os

def main(data: Data, filename: str):
    fig = init_plot()
    funcs, params, gs = generate_ax_func(fig, data.pressure, data.variables)
    
    for func, param in zip(funcs, params):
        func(param, gs)
    
    plot_window_elements(fig, data.info)
    plt.savefig(os.path.join("figures", filename), dpi=300, bbox_inches='tight')
    plt.close()
    print(f"图像已保存到 {filename}")

if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 3):
        print("Usage: python main.py <data_json> <filename>")
        sys.exit(1)
    if isinstance(sys.argv[1], Data):
        main(sys.argv[1], sys.argv[2])
    else:
        main(construct_data(sys.argv[1]), sys.argv[2])