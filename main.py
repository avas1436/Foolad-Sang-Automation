from packages.ploter import PlotManager
from packages.safe_round import NumberRounder

# rounder = NumberRounder()
# print(rounder.round(1.23))

# print(rounder(3.1411615))
# print(rounder.round_list([1.25153, 2.355158, 0, None], zero_return=False))


x_list = [1, 2, 3, 4, 5]
y_list = [1, 5, 14, 25, 40]

plot = PlotManager()

plot.line_plot(
    x_data=x_list,
    y_data=y_list,
    title="avAs",
    xlabel="amir",
    ylabel="zade",
    label="abaszade",
    grid=False,
)
