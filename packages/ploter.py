from typing import List, Optional

import matplotlib.pyplot as plt


class PlotManager:
    def __init__(self, figsize: tuple = (10, 6)):
        """
        کلاس مدیریت نمودارها

        Args:
            figsize: اندازه نمودار (عرض, ارتفاع)
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
        x_data: List[float],
        y_data: List[float],
        title: str = "Line Plot",
        xlabel: str = "X Axis",
        ylabel: str = "Y Axis",
        label: Optional[str] = None,
        color: Optional[str] = None,
        grid: bool = True,
    ):
        if color is None:
            color = self.colors[0]

        fig, ax = plt.subplots(figsize=self.figsize)
        ax.plot(x_data, y_data, label=label, color=color, linewidth=2)
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)

        if grid:
            ax.grid(True, alpha=0.3)
        if label:
            ax.legend()

        fig.tight_layout()
        return fig, ax

    def bar_plot(
        self,
        categories: List[str],
        values: List[float],
        title: str = "Bar Plot",
        xlabel: str = "Categories",
        ylabel: str = "Values",
        color: Optional[str] = None,
    ):
        if color is None:
            color = self.colors[0]

        fig, ax = plt.subplots(figsize=self.figsize)
        bars = ax.bar(categories, values, color=color, alpha=0.7)
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)

        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{height:.1f}",
                ha="center",
                va="bottom",
            )

        fig.tight_layout()
        return fig, ax

    def scatter_plot(
        self,
        x_data: List[float],
        y_data: List[float],
        title: str = "Scatter Plot",
        xlabel: str = "X Axis",
        ylabel: str = "Y Axis",
        color: Optional[str] = None,
        size: int = 50,
    ):
        if color is None:
            color = self.colors[0]

        fig, ax = plt.subplots(figsize=self.figsize)
        ax.scatter(x_data, y_data, color=color, s=size, alpha=0.6)
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.grid(True, alpha=0.3)

        fig.tight_layout()
        return fig, ax

    def histogram(
        self,
        data: List[float],
        title: str = "Histogram",
        xlabel: str = "Values",
        ylabel: str = "Frequency",
        bins: int = 10,
        color: Optional[str] = None,
    ):
        if color is None:
            color = self.colors[0]

        fig, ax = plt.subplots(figsize=self.figsize)
        ax.hist(data, bins=bins, color=color, alpha=0.7, edgecolor="black")
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.grid(True, alpha=0.3)

        fig.tight_layout()
        return fig, ax

    def pie_chart(
        self,
        labels: List[str],
        sizes: List[float],
        title: str = "Pie Chart",
        autopct: str = "%1.1f%%",
    ):
        fig, ax = plt.subplots(figsize=self.figsize)
        ax.pie(
            sizes,
            labels=labels,
            autopct=autopct,
            colors=self.colors[: len(labels)],
            startangle=90,
        )
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.axis("equal")

        fig.tight_layout()
        return fig, ax

    def multiple_lines(
        self,
        x_data: List[float],
        y_data_list: List[List[float]],
        labels: List[str],
        title: str = "Multiple Lines",
        xlabel: str = "X Axis",
        ylabel: str = "Y Axis",
    ):
        fig, ax = plt.subplots(figsize=self.figsize)
        for i, y_data in enumerate(y_data_list):
            color = self.colors[i % len(self.colors)]
            ax.plot(x_data, y_data, label=labels[i], color=color, linewidth=2)

        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend()

        fig.tight_layout()
        return fig, ax

    def save_plot(self, fig, filename: str, dpi: int = 300) -> None:
        fig.tight_layout()
        fig.savefig(filename, dpi=dpi, bbox_inches="tight")
        print(f"Plot {filename} saved!")
