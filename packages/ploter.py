from typing import List, Optional

import matplotlib.pyplot as plt


class PlotManager:
    def __init__(self, figsize: tuple = (10, 6)):
        """
        کلاس مدیریت نمودارها

        Args:
            figsize: اندازه نمودار (عرض, ارتفاع)
            style: استایل نمودار
        """
        self.figsize = figsize
        self.colors = [
            "#1f77b4",
            "#ff7f0e",
            "#2ca02c",
            "#d62728",
            "#9467bd",
            "#8c564b",
            "#e377c2",
            "#7f7f7f",
            "#bcbd22",
            "#17becf",
        ]

    def line_plot(
        self,
        x_data: List,
        y_data: List,
        title: str = "Line Plot",
        xlabel: str = "X Axis",
        ylabel: str = "Y Axis",
        label: Optional[str] = None,
        color: Optional[str] = None,
        grid: bool = True,
    ) -> None:
        """
        ایجاد نمودار خطی

        Args:
            x_data: x
            y_data: y
            title: عنوان نمودار
            xlabel: برچسب محور x
            ylabel: برچسب محور y
            label: برچسب برای legend
            color = color[0]/blue, color[3]/red, color[2]/green
            grid: True or False
        """
        if color is None:
            color = self.colors[0]

        plt.figure(figsize=self.figsize)
        plt.plot(x_data, y_data, label=label, color=color, linewidth=2)
        plt.title(title, fontsize=14, fontweight="bold")
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)

        if grid:
            plt.grid(True, alpha=0.3)

        if label:
            plt.legend()

        plt.tight_layout()
        plt.show()

    def bar_plot(
        self,
        categories: List[str],
        values: List[float],
        title: str = "Bar Plot",
        xlabel: str = "Categories",
        ylabel: str = "Values",
        color: Optional[str] = None,
    ) -> None:
        """
        ایجاد نمودار میله‌ای
        """
        plt.figure(figsize=self.figsize)

        if color is None:
            color = self.colors[0]

        bars = plt.bar(categories, values, color=color, alpha=0.7)
        plt.title(title, fontsize=14, fontweight="bold")
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)

        # اضافه کردن مقادیر روی میله‌ها
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{height:.1f}",
                ha="center",
                va="bottom",
            )

        plt.tight_layout()
        plt.show()

    def scatter_plot(
        self,
        x_data: List,
        y_data: List,
        title: str = "Scatter Plot",
        xlabel: str = "X Axis",
        ylabel: str = "Y Axis",
        color: Optional[str] = None,
        size: int = 50,
    ) -> None:
        """
        ایجاد نمودار پراکندگی
        """
        plt.figure(figsize=self.figsize)

        if color is None:
            color = self.colors[0]

        plt.scatter(x_data, y_data, color=color, s=size, alpha=0.6)
        plt.title(title, fontsize=14, fontweight="bold")
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def histogram(
        self,
        data: List[float],
        title: str = "Histogram",
        xlabel: str = "Values",
        ylabel: str = "Frequency",
        bins: int = 10,
        color: Optional[str] = None,
    ) -> None:
        """
        ایجاد هیستوگرام
        """
        plt.figure(figsize=self.figsize)

        if color is None:
            color = self.colors[0]

        plt.hist(data, bins=bins, color=color, alpha=0.7, edgecolor="black")
        plt.title(title, fontsize=14, fontweight="bold")
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def pie_chart(
        self,
        labels: List[str],
        sizes: List[float],
        title: str = "Pie Chart",
        autopct: str = "%1.1f%%",
    ) -> None:
        """
        ایجاد نمودار دایره‌ای
        """
        plt.figure(figsize=self.figsize)

        plt.pie(
            sizes,
            labels=labels,
            autopct=autopct,
            colors=self.colors[: len(labels)],
            startangle=90,
        )
        plt.title(title, fontsize=14, fontweight="bold")
        plt.axis("equal")  # برای دایره‌ای بودن نمودار
        plt.tight_layout()
        plt.show()

    def multiple_lines(
        self,
        x_data: List,
        y_data_list: List[List],
        labels: List[str],
        title: str = "Multiple Lines",
        xlabel: str = "X Axis",
        ylabel: str = "Y Axis",
    ) -> None:
        """
        ایجاد نمودار با چندین خط
        """
        plt.figure(figsize=self.figsize)

        for i, y_data in enumerate(y_data_list):
            color = self.colors[i % len(self.colors)]
            plt.plot(x_data, y_data, label=labels[i], color=color, linewidth=2)

        plt.title(title, fontsize=14, fontweight="bold")
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def save_plot(self, filename: str, dpi: int = 300) -> None:
        """
        ذخیره نمودار فعلی
        """
        plt.savefig(filename, dpi=dpi, bbox_inches="tight")
        print(f"Plot {filename} saved!")
