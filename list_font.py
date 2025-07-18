from matplotlib import pyplot as plt
import matplotlib
a=sorted([f.name for f in matplotlib.font_manager.fontManager.ttflist])

with open('fonts.txt', 'w', encoding='utf-8') as f:
    for i in a:
        f.write(i + '\n')