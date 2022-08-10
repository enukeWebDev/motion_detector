from motion_detector import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool

# df["Start_string"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
# df["End_string"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

# col_data_source = ColumnDataSource(df)

p = figure(x_axis_type = "datetime", height = 100, width = 500, title = "Motion Detector Graph")
p.yaxis.minor_tick_line_color = None
p.yaxis[0].ticker.desired_num_ticks = 1

hover_for_info = HoverTool(tooltips = [("Start", "@Start"), ("End", "@End")])
p.add_tools(hover_for_info)

q = p.quad(left = df["Start"], right = df["End"], bottom = 0, top = 1, color = "red")

output_file("Graph.html")

show(p)

