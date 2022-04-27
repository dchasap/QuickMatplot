#!/usr/bin/python3 

import argparse
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
#import logging

parser = argparse.ArgumentParser()
#figure type options
parser.add_argument("--barplot", dest="barplot", action="store_false", help="Draw a bar plot (enabled by defaul)")
parser.add_argument("--scatterplot", dest="scatterplot", action="store_true", help="Draw a scatter plot")
parser.add_argument("--lineplot", dest="lineplot", action="store_true", help="Draw a line plot")
parser.add_argument("--stacked", dest="stacked", action="store_true", help="Stack multiple bars (clustered by default)")
#data options
parser.add_argument("-i", "--input-files", dest="input_files", nargs='*', required=True, help="Input data file to be plotted")
parser.add_argument("-o", "--output-file", dest="output_file", default="out.pdf", help="Output figure")
parser.add_argument("-y", "--ydata", dest="ydata", nargs='*', required=True, help="Data to plot on y axis")
parser.add_argument("-x", "--xdata", dest="xdata", default='NA', help="Data to plot on x axis")
parser.add_argument("--ylabel", dest="ylabel", default='y', help="Label for y axis")
parser.add_argument("--xlabel", dest="xlabel", default='x', help="Labe:/l for x axis")
parser.add_argument("--labels", dest="labels", nargs="*", help="Labels for the corresponding input files")
parser.add_argument("--auto-labels", dest="auto_labels", action="store_true", help="Automatically try to get labels from input data")
parser.add_argument("--title", dest="title", default='', help="Plot title")
#legend options
parser.add_argument("--remove-legend", dest="legend_enabled", action="store_false", help="Remove legend from figure")
parser.add_argument("--legend-position", dest="legend_position", default="best", help="Define legend position")
parser.add_argument("--legend-columns", dest="legend_cols", default=2, help="Number of columns for the legend")
parser.add_argument("--legend-font-size", dest="legend_fontsize", default=14, help="Define legend position")
#grid and axis options
parser.add_argument("--enable-major-gridlines", dest="enable_major_gridlines", action="store_true", help="Show major gridlines")
parser.add_argument("--xaxis-percentages", dest="xaxis_percentages", action="store_true", help="Set x axis tick labels to percentages")
parser.add_argument("--disable-xticks", dest="disable_xticks", action="store_true", help="Do not show xticks")
parser.add_argument("--xticks-rotate-by", dest="xticks_rotate_by", default=0, help="Rotate xtick labels by N degrees")
parser.add_argument("--xticks-labels", dest="xticks_labels", nargs="*", default=None, help="Set custom labels for xticks")
parser.add_argument("--xticks-step", dest="xticks_step", default=1, help="Set custom step for xticks")
parser.add_argument("--xticks-labelsize", dest="xticks_labelsize", default=16, help="Set plot's xticks label font size")
parser.add_argument("--yrange", dest="yrange", nargs=2, default=None, help="Set range for y axis")
parser.add_argument("--xrange", dest="xrange", nargs=2, default=None, help="Set range for x axis")
#general aesthetics
parser.add_argument("--plot-size-inches", dest="plot_size_inches", nargs="*", help="Set plot size (inches)")
parser.add_argument("--font-size", dest="font_size", default="18", help="Set plot's font size")
parser.add_argument("--bar-width", dest="bar_width", default=0.8, help="Bar width")
parser.add_argument("--line-width", dest="line_width", default=1, help="Line width") 
parser.add_argument("--point-size", dest="point_size", default=5, help="Point size")
parser.add_argument("--custom-markers", dest="markers", default=None, help="Custom markers")
parser.add_argument("--marker-step", dest="marker_step", default=1, help="Set marker step, in case plot has too many data points")
parser.add_argument("--add-marker-points", dest="add_markers", action="store_true", help="Adds marker points to lineplot")
parser.add_argument("--custom-linestyles", dest="linestyles", default=None, help="Custom linetypes")

parser.add_argument("--custom-color-palette", dest="custom_color_palette", nargs="*", required=False, help="Define a custom color palette (expects hex values seperated by spaces)")
parser.add_argument("--choose-color-palette", dest="color_palette", default="default", help="Choose a predefined color palette (default, greyscale, metro_ui, program)")
parser.add_argument("--style-xkcd", dest="style_xkcd_enabled", action="store_true", help="Create an xkcd style plot")
parser.add_argument("--normalize-x-by", dest="norm_x_by", default=None, help="Normalize x axis data by n")
parser.add_argument("--normalize-y-by", dest="norm_y_by", default=None, help="Normalize y axis data by n")
parser.add_argument("--xaxis-log-scale", dest="xaxis_log_scale", action="store_true", help="Use log scale for x axis")
parser.add_argument("--yaxis-log-scale", dest="yaxis_log_scale", action="store_true", help="Use log scale for y axis")

#TODO: scale axes

args = parser.parse_args()

#logging.basicConfig(level=logging.DEBUG, format='%(message)s')

matplotlib.rcParams.update({'font.size': args.font_size})

#def format_fn(tick_val, tick_pos):
#    if int(tick_val) in xs:
#        return args.xticks_labels[int(tick_val)]
#    else:
#        return ''


#init figure
if args.style_xkcd_enabled:
    plt.xkcd()

plt.style.use('default')
#plt.style.use('classic')
#plt.style.use('seaborn-whitegrid')
#plt.style.use('ggplot')


fig = plt.figure(figsize = (8, 4))
ax = fig.add_subplot(1, 1, 1)
#ax.spines['right'].set_color('none')
#ax.spines['top'].set_color('none')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
ax.ticklabel_format(useOffset=False) 
ax.set_axisbelow(True)

plt.margins(x=0.01)

if args.yaxis_log_scale:
    ax.set_yscale('symlog')
if args.xaxis_log_scale:
    ax.set_xscale('symlog')

if args.enable_major_gridlines:
    ax.grid(b=True, color='grey', alpha=0.5, which='major', linestyle='--', linewidth=.5)
    #grid(color='r', linestyle='-', linewidth=2)
#plt.xticks([], [])
#plt.yticks([])
#plt.xticks(rotation=args.xticks_rotate_by, verticalalignment='bottom')
plt.xlabel(args.xlabel)
plt.ylabel(args.ylabel)
plt.title(args.title)
#plt.yticks(np.arange(0, 14000, 2000), ('0', '2', '4', '6', '8', '10', '12'))
#plt.locator_params(axis='x', nbins=10)

#choose built-in color palette
color_palettes = {  "default" : ["b", "r", "g", "m", "y"],
                                        "greyscale" : ["#000000", "#7b7d7b", "#969696", "#bfbfbf", "#ebebeb"],
                                        "metro_ui" : ["#00aedb", "#d11141", "#00b159", "#ffc425", "#f37735", "#ff0097", "#9f00a7", "#00aba9", "#eff4ff", "#99b433"],
                                        "program"   : ["#00a0b0", "#cc2a36", "#4f372d", "#edc951", "#eb6841"],
}

markers=["o", "s", "^", "v", "<", ">", "d", 'P', 'X']
markers=["X", "P"]
if args.markers != None:
    markers=args.markers

#linestyles=["-", "--", "-.", "-", "-"]
linestyles=["-", "--", ":", "-.", "-"]
if args.linestyles !=  None:
   linestyles=args.linestyles

if args.custom_color_palette != None:
    colors=args.custom_color_palette
else:
    colors=color_palettes[args.color_palette]

line_no = 0
file_no = 0
for input_file in args.input_files:

    df = pd.read_csv(input_file)

    # apply data transformation, normalization, etc
    if args.norm_y_by != None:
        df[args.ydata] = df[args.ydata] * float(args.norm_y_by)
    if args.norm_x_by != None:
        df[args.xdata] = df[args.xdata] * float(args.norm_x_by)

    for y in args.ydata:

        ydata = df[y]
        if args.xdata != "NA":
            xdata = df[args.xdata]
            if not args.lineplot:
                plt.xticks(range(len(xdata)), xdata)
        else:
            xdata = range(0, len(ydata)) 
            plt.xticks([])

        if args.labels is not None:
            label = args.labels.pop(0)
        elif args.auto_labels:
            label = y
        else:
            label = "line " + str(line_no)

        color = colors[line_no % len(colors)]

        if args.scatterplot:
            marker = markers[line_no % len(markers)]
            size=float(args.point_size)
        else:
            if args.add_markers:
                marker = markers[line_no % len(markers)]
            else:
                marker = ","
            linestyle = linestyles[line_no % len(linestyles)]
            size=float(args.line_width)
            point_size=float(args.point_size)

#        if line_no == 0:
#            if args.scatterplot:
#                ax.plot(range(len(ydata)), ydata, marker, markersize=size, label=label, color=color)
#            elif args.lineplot:
#                ax.plot(xdata[1::10], ydata[1::10], linestyle=linestyle, linewidth=size, marker=marker, markersize=point_size, markevery=int(args.marker_step), label=label, color=color)
 #           else:
 #               ax.bar(range(len(ydata)), ydata, width=float(args.bar_width), align='center', label=label, color=color)

        if args.stacked:
            if args.scatterplot:
                ax.plot(range(len(ydata)), ydata, marker, markersize=size, label=label, color=color, markeredgewidth=0.5, markeredgecolor='black')
            elif args.lineplot: 
                ax.plot(xdata[1::10], ydata[1::10], linestyle, linewidth=size, marker=marker, markersize=point_size, markevery=int(args.marker_step), label=label, color=color)
            else:
                ax.bar(range(len(ydata)), ydata, width=float(args.bar_width), align='center', label=label, color=color, bottom=stacked_ydata, edgecolor='black', linewidth=0.01)
            stacked_ydata += ydata
        else:
            if args.scatterplot:
                ax.plot(range(len(ydata)), ydata, marker, markersize=size, label=label, color=color, markeredgewidth=0.5, markeredgecolor='black')
            elif args.lineplot: 
                ax.plot(xdata[1::10], ydata[1::10], linestyle, linewidth=size, marker=marker, markersize=point_size, markevery=int(args.marker_step), label=label, color=color)
            else:
                gap = 0.1
                width = (1 - gap) / len(args.ydata)
                pos = [j - (1 - gap) / 2 + line_no * width - 1 for j in range(1, len(ydata) + 1)]
                ax.bar(pos, ydata, width, label=label, color=color, edgecolor='black', linewidth=0.01)
                #ax.bar([line_no*width + x for x in range(len(ydata))], ydata, width, label=label, color=color)
        line_no += 1
    file_no += 1

if args.disable_xticks:
    plt.xticks([], [])
elif args.xticks_labels != None:
    #ax.set_xticks(args.xticks_labels)
    #ax.set_xticks(ax.get_xticks()[::len(ax.get_xticks()) // 10000]) # set new tick positions
    ax.set_xticklabels(ax.get_xticklabels(), rotation = int(args.xticks_rotate_by), ha="right")
    #ax.set_xticks( np.geomspace(0, 20000 ,15).round() )
else:
    ax.set_xticks(ax.get_xticks()[::int(args.xticks_step)])
    plt.setp(ax.get_xticklabels(), ha="right", rotation = int(args.xticks_rotate_by))

# DISABLE scientific notation in y axis
# ax.ticklabel_format(style='plain', axis='y')

plt.tick_params(labelsize=args.xticks_labelsize)

if args.legend_enabled and line_no > 1:

    if args.legend_position == "above":
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + 0.1, box.width, box.height * 0.65])
        lgnd = ax.legend(loc='center', bbox_to_anchor=(0.5, 1.3), prop={'size':args.legend_fontsize}, ncol=int(args.legend_cols))
    elif args.legend_position == "below":
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + .3, box.width, box.height * 0.65])
        lgnd = ax.legend(loc='center', bbox_to_anchor=(0.5, -0.5), prop={'size':args.legend_fontsize}, ncol=int(args.legend_cols))
    elif args.legend_position == "outside":
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
        lgnd = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size':args.legend_fontsize})
    else:
        lgnd = ax.legend(loc=args.legend_position, bbox_to_anchor=(1, 0.5), prop={'size':args.legend_fontsize})

if args.xaxis_percentages:
    vals = ax.get_yticks()
    ax.set_yticklabels(['{:3.0f}%'.format(x) for x in vals])

if args.yrange != None:
    x = args.yrange.pop(0)
    y = args.yrange.pop(0)
    ax.set_ylim(float(x), float(y))

if args.xrange != None:
    x = args.xrange.pop(0)
    y = args.xrange.pop(0)
    ax.set_xlim(float(x), float(y))
#plt.semilogx()
#plt.semilogy()
#plt.xlim()
if args.plot_size_inches != None:
    x = args.plot_size_inches.pop(0)
    y = args.plot_size_inches.pop(0)
    fig.set_size_inches(float(x), float(y))

#plt.tight_layout()

if args.legend_enabled and line_no > 1:
    fig.savefig(args.output_file, bbox_extra_artists=(lgnd,), bbox_inches='tight')
else:   
    fig.savefig(args.output_file, bbox_inches='tight')


