import os
import matplotlib.pyplot as plt
from plot import init_plot, generate_ax_func, plot_window_elements
from interface import construct_data, Data

def main(data: Data, post_process = None):
    fig = init_plot()
    funcs, params, gs = generate_ax_func(fig, data.pressure, data.variables, data.show_digit)
    
    for func, param in zip(funcs, params):
        func(param, gs)
    
    plot_window_elements(fig, data.info)
    if post_process is not None:
        post_process()

if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 3):
        print("Usage: python main.py <data_json> <filename>")
        sys.exit(1)
    if isinstance(sys.argv[1], Data):
        main(sys.argv[1], sys.argv[2])
    else:
        main(construct_data(sys.argv[1]), sys.argv[2])