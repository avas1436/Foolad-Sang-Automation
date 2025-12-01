import random
import sys

from PySide6.QtCore import QPoint, QSize, Qt, QTimer
from PySide6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QLinearGradient,
    QPainter,
    QPalette,
    QPen,
)
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QSplitter,
    QStyleFactory,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class ThemeManager:
    """مدیریت تم‌های برنامه"""

    # تم فلت روشن
    LIGHT_FLAT_THEME = {
        "primary": "#FFFFFF",  # رنگ اصلی
        "secondary": "#F8F9FA",  # رنگ ثانویه
        "accent": "#4285F4",  # رنگ تأکیدی (آبی گوگلی)
        "accent_hover": "#3367D6",  # رنگ تأکیدی هنگام هاور
        "text_primary": "#202124",  # متن اصلی
        "text_secondary": "#5F6368",  # متن ثانویه
        "text_light": "#80868B",  # متن روشن
        "border": "#DADCE0",  # رنگ حاشیه
        "border_light": "#E8EAED",  # رنگ حاشیه روشن
        "card": "#FFFFFF",  # رنگ کارت
        "card_shadow": "rgba(60, 64, 67, 0.1)",  # سایه کارت
        "success": "#34A853",  # موفقیت (سبز)
        "warning": "#FBBC05",  # هشدار (زرد)
        "error": "#EA4335",  # خطا (قرمز)
        "info": "#4285F4",  # اطلاعات (آبی)
        "sidebar": "#FFFFFF",  # رنگ نوار کناری
        "titlebar_gradient": "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #4285F4, stop:1 #34A853)",  # گرادیان نوار عنوان
        "chart_bg": "#FFFFFF",  # پس‌زمینه نمودار
        "chart_grid": "#F1F3F4",  # خطوط نمودار
        "table_header": "#F8F9FA",  # هدر جدول
        "table_row_even": "#FFFFFF",  # ردیف زوج جدول
        "table_row_odd": "#F8F9FA",  # ردیف فرد جدول
    }

    # تم فلت تاریک
    DARK_FLAT_THEME = {
        "primary": "#1E1E1E",  # رنگ اصلی
        "secondary": "#2D2D2D",  # رنگ ثانویه
        "accent": "#8AB4F8",  # رنگ تأکیدی (آبی روشن)
        "accent_hover": "#AECBFA",  # رنگ تأکیدی هنگام هاور
        "text_primary": "#E8EAED",  # متن اصلی
        "text_secondary": "#BDC1C6",  # متن ثانویه
        "text_light": "#9AA0A6",  # متن روشن
        "border": "#3C4043",  # رنگ حاشیه
        "border_light": "#5F6368",  # رنگ حاشیه روشن
        "card": "#2D2D2D",  # رنگ کارت
        "card_shadow": "rgba(0, 0, 0, 0.3)",  # سایه کارت
        "success": "#81C995",  # موفقیت (سبز روشن)
        "warning": "#FDD663",  # هشدار (زرد روشن)
        "error": "#F28B82",  # خطا (قرمز روشن)
        "info": "#8AB4F8",  # اطلاعات (آبی روشن)
        "sidebar": "#252525",  # رنگ نوار کناری
        "titlebar_gradient": "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #4285F4, stop:1 #34A853)",  # گرادیان نوار عنوان
        "chart_bg": "#2D2D2D",  # پس‌زمینه نمودار
        "chart_grid": "#3C4043",  # خطوط نمودار
        "table_header": "#3C4043",  # هدر جدول
        "table_row_even": "#2D2D2D",  # ردیف زوج جدول
        "table_row_odd": "#252525",  # ردیف فرد جدول
    }

    # تم‌های موجود
    THEMES = {
        "light_flat": LIGHT_FLAT_THEME,
        "dark_flat": DARK_FLAT_THEME,
    }


class ModernWindow(QWidget):
    """کلاس اصلی پنجره برنامه با قابلیت‌های سفارشی و تغییر تم"""

    def __init__(self):
        super().__init__()
        # تنظیم پنجره بدون فریم (بدون حاشیه استاندارد)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Professional Data Analytics Dashboard")

        # تعیین تم پیش‌فرش (روشن و فلت)
        self.current_theme = "light_flat"
        self.theme = ThemeManager.THEMES[self.current_theme]

        # تعیین اندازه اولیه پنجره
        self.resize(800, 600)

        # استایل کلی برنامه
        self.setStyleSheet(
            """
            QWidget {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 13px;
            }
        """
        )

        # ایجاد نوار عنوان سفارشی
        self._create_title_bar()
        # ایجاد نوار تنظیمات
        self._create_settings_bar()
        # ایجاد محتوای اصلی برنامه
        self._create_main_content()

        # اتصال رویدادهای برنامه
        self._connect_events()

        # اعمال تم اولیه
        self.apply_theme()

    def _create_title_bar(self):
        """ایجاد نوار عنوان سفارشی در بالای پنجره"""
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(50)  # کمی بلندتر برای ظاهر مدرن
        self.title_bar.setObjectName("titleBar")

        # ایجاد لایه برای نوار عنوان
        title_bar_layout = QHBoxLayout(self.title_bar)
        title_bar_layout.setContentsMargins(15, 0, 15, 0)

        # ایجاد لوگو و عنوان برنامه
        logo_label = QLabel("📊")
        logo_label.setStyleSheet("font-size: 24px;")
        self.title_label = QLabel("Professional Data Analytics Dashboard")
        self.title_label.setObjectName("titleLabel")

        # ایجاد دکمه‌های کنترل پنجره
        self.btn_min = self._create_title_button("−", self.theme["warning"])
        self.btn_max = self._create_title_button("□", self.theme["success"])
        self.btn_close = self._create_title_button("×", self.theme["error"])

        # اتصال رویدادها به دکمه‌ها
        self.btn_close.clicked.connect(self.close)
        self.btn_min.clicked.connect(self.showMinimized)
        self.btn_max.clicked.connect(self.toggle_maximize)

        # اضافه کردن ویجت‌ها به لایه نوار عنوان
        title_bar_layout.addWidget(logo_label)
        title_bar_layout.addWidget(self.title_label)
        title_bar_layout.addStretch()
        title_bar_layout.addWidget(self.btn_min)
        title_bar_layout.addWidget(self.btn_max)
        title_bar_layout.addWidget(self.btn_close)

    def _create_title_button(self, text, color):
        """تابع کمکی برای ایجاد دکمه‌های نوار عنوان"""
        btn = QPushButton(text)
        btn.setFixedSize(25, 25)
        btn.setObjectName("titleButton")
        # استایل دینامیک در apply_theme تنظیم می‌شود
        return btn

    def _create_settings_bar(self):
        """ایجاد نوار تنظیمات زیر نوار عنوان"""
        self.settings_bar = QWidget()
        self.settings_bar.setFixedHeight(60)
        self.settings_bar.setObjectName("settingsBar")

        # ایجاد لایه برای نوار تنظیمات
        settings_layout = QHBoxLayout(self.settings_bar)
        settings_layout.setContentsMargins(20, 10, 20, 10)

        # ایجاد دکمه‌های تنظیمات اصلی
        settings_buttons = [
            ("⚙️", "Settings", self.theme["info"]),
            ("📁", "File", self.theme["success"]),
            ("📊", "Analysis", self.theme["accent"]),
            ("📈", "Charts", self.theme["warning"]),
            ("👤", "Profile", self.theme["error"]),
        ]

        # اضافه کردن دکمه‌های تنظیمات به نوار
        for icon, text, color in settings_buttons:
            btn = self._create_flat_button(icon, text, color)
            settings_layout.addWidget(btn)

        # اضافه کردن فضای خالی برای جدا کردن بخش‌ها
        settings_layout.addStretch()

        # ایجاد دکمه تغییر تم
        self.theme_toggle_btn = self._create_flat_button(
            "🌙", "Dark Theme", self.theme["info"]
        )
        self.theme_toggle_btn.clicked.connect(self.toggle_theme)
        settings_layout.addWidget(self.theme_toggle_btn)

    def _create_flat_button(self, icon, text, color):
        """ایجاد دکمه‌های فلت"""
        btn = QPushButton(f"{icon} {text}")
        btn.setFixedHeight(40)
        btn.setObjectName("flatButton")
        # رنگ به عنوان property ذخیره می‌شود
        btn.setProperty("buttonColor", color)
        return btn

    def _create_main_content(self):
        """ایجاد محتوای اصلی برنامه شامل نوار کناری و ناحیه اصلی"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # اضافه کردن نوار عنوان و تنظیمات به لایه اصلی
        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(self.settings_bar)

        # ایجاد ویجت مرکزی
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        central_layout = QHBoxLayout(central_widget)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)

        # ایجاد نوار کناری برای انتخاب پردازش‌ها
        self._create_sidebar(central_layout)

        # ایجاد ناحیه اصلی برای نمایش داده‌ها
        self._create_main_area(central_layout)

        # اضافه کردن ویجت مرکزی به لایه اصلی
        main_layout.addWidget(central_widget)

    def _create_sidebar(self, parent_layout):
        """ایجاد نوار کناری سمت چپ برای انتخاب انواع پردازش‌ها"""
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(300)
        self.sidebar.setObjectName("sidebar")

        # ایجاد لایه برای نوار کناری
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(15)

        # ایجاد عنوان نوار کناری
        sidebar_title = QLabel("📈 Data Processing")
        sidebar_title.setObjectName("sidebarTitle")

        # ایجاد لیست پردازش‌های قابل انتخاب
        self.process_list = QListWidget()
        self.process_list.setObjectName("processList")

        # ایجاد آیتم‌های مختلف برای پردازش داده‌ها
        process_items = [
            ("📊", "Statistical Analysis", "Descriptive and inferential data analysis"),
            ("📈", "Time Series Forecasting", "Modeling and trend prediction"),
            ("🔍", "Clustering", "Grouping similar data points"),
            ("📉", "Regression", "Modeling relationships between variables"),
            ("🧮", "PCA", "Dimensionality reduction"),
            ("🧠", "Neural Networks", "Complex nonlinear modeling"),
            ("📋", "NLP", "Text and language data analysis"),
            ("🖼️", "Image Processing", "Image analysis and processing"),
        ]

        # اضافه کردن آیتم‌ها به لیست
        for icon, title, desc in process_items:
            # ایجاد ویجت سفارشی برای هر آیتم
            item_widget = QWidget()
            item_widget.setObjectName("processItem")
            item_layout = QVBoxLayout(item_widget)
            item_layout.setContentsMargins(12, 12, 12, 12)
            item_layout.setSpacing(5)

            # ایجاد برچسب عنوان
            title_label = QLabel(f"{icon} {title}")
            title_label.setObjectName("processItemTitle")

            # ایجاد برچسب توضیحات
            desc_label = QLabel(desc)
            desc_label.setObjectName("processItemDesc")
            desc_label.setWordWrap(True)

            # اضافه کردن برچسب‌ها به لایه آیتم
            item_layout.addWidget(title_label)
            item_layout.addWidget(desc_label)

            # ایجاد آیتم لیست و تنظیم ویجت سفارشی روی آن
            list_item = QListWidgetItem(self.process_list)
            list_item.setSizeHint(item_widget.sizeHint())
            self.process_list.addItem(list_item)
            self.process_list.setItemWidget(list_item, item_widget)

        # ایجاد بخش فیلترها
        filter_group = QGroupBox("⚙️ Filters")
        filter_group.setObjectName("filterGroup")

        filter_layout = QVBoxLayout(filter_group)

        # ایجاد رادیو باتن‌های فیلتر زمانی
        time_filter_group = QButtonGroup(self)
        time_filters = ["Today", "This Week", "This Month", "All Data"]

        for filter_text in time_filters:
            radio = QRadioButton(filter_text)
            radio.setObjectName("timeFilterRadio")
            time_filter_group.addButton(radio)
            filter_layout.addWidget(radio)

        # انتخاب اولین فیلتر به صورت پیش‌فرض
        if time_filters:
            time_filter_group.buttons()[0].setChecked(True)

        # ایجاد دکمه شروع پردازش
        self.start_btn = QPushButton("🚀 Start Processing")
        self.start_btn.setFixedHeight(50)
        self.start_btn.setObjectName("startButton")

        # اضافه کردن ویجت‌ها به نوار کناری
        sidebar_layout.addWidget(sidebar_title)
        sidebar_layout.addWidget(self.process_list)
        sidebar_layout.addWidget(filter_group)
        sidebar_layout.addWidget(self.start_btn)
        sidebar_layout.addStretch()

        # اضافه کردن نوار کناری به لایه والد
        parent_layout.addWidget(self.sidebar)

    def _create_main_area(self, parent_layout):
        """ایجاد ناحیه اصلی سمت راست برای نمایش نمودارها و جداول"""
        self.main_area = QWidget()
        self.main_area.setObjectName("mainArea")

        # ایجاد لایه برای ناحیه اصلی
        main_area_layout = QVBoxLayout(self.main_area)
        main_area_layout.setContentsMargins(20, 20, 20, 20)
        main_area_layout.setSpacing(20)

        # ایجاد عنوان ناحیه اصلی
        main_title = QLabel("📊 Data Visualization Dashboard")
        main_title.setObjectName("mainTitle")

        # ایجاد ویجت تب برای نمایش انواع مختلف داده
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("tabWidget")

        # ایجاد تب اول: نمودارها
        chart_tab = QWidget()
        chart_tab.setObjectName("chartTab")
        chart_layout = QVBoxLayout(chart_tab)
        chart_layout.setContentsMargins(0, 0, 0, 0)
        self._create_chart_area(chart_layout)

        # ایجاد تب دوم: جداول داده
        table_tab = QWidget()
        table_tab.setObjectName("tableTab")
        table_layout = QVBoxLayout(table_tab)
        table_layout.setContentsMargins(0, 0, 0, 0)
        self._create_table_area(table_layout)

        # ایجاد تب سوم: تنظیمات
        settings_tab = QWidget()
        settings_tab.setObjectName("settingsTab")
        settings_layout = QVBoxLayout(settings_tab)
        settings_layout.setContentsMargins(0, 0, 0, 0)
        self._create_settings_area(settings_layout)

        # اضافه کردن تب‌ها به ویجت تب
        self.tab_widget.addTab(chart_tab, "📈 Charts")
        self.tab_widget.addTab(table_tab, "📊 Tables")
        self.tab_widget.addTab(settings_tab, "⚙️ Settings")

        # ایجاد بخش کنترل‌های نمایش
        controls_widget = QWidget()
        controls_widget.setObjectName("controlsWidget")
        controls_layout = QHBoxLayout(controls_widget)
        controls_layout.setContentsMargins(0, 0, 0, 0)

        # ایجاد دکمه‌های کنترل
        control_buttons = [
            ("🔄", "Refresh", self.theme["info"]),
            ("💾", "Save", self.theme["success"]),
            ("📤", "Export", self.theme["accent"]),
            ("🖨️", "Print", self.theme["warning"]),
        ]

        # اضافه کردن دکمه‌های کنترل
        for icon, text, color in control_buttons:
            btn = self._create_small_flat_button(icon, text, color)
            controls_layout.addWidget(btn)

        controls_layout.addStretch()

        # اضافه کردن ویجت‌ها به ناحیه اصلی
        main_area_layout.addWidget(main_title)
        main_area_layout.addWidget(self.tab_widget, 1)
        main_area_layout.addWidget(controls_widget)

        # اضافه کردن ناحیه اصلی به لایه والد
        parent_layout.addWidget(self.main_area, 1)

    def _create_small_flat_button(self, icon, text, color):
        """ایجاد دکمه‌های فلت کوچک"""
        btn = QPushButton(f"{icon} {text}")
        btn.setFixedHeight(36)
        btn.setObjectName("smallFlatButton")
        btn.setProperty("buttonColor", color)
        return btn

    def _create_chart_area(self, layout):
        """ایجاد ناحیه نمودار"""
        chart_container = QWidget()
        chart_container.setObjectName("chartContainer")
        chart_container.setMinimumHeight(400)

        chart_layout = QVBoxLayout(chart_container)
        chart_layout.setContentsMargins(20, 20, 20, 20)

        # ایجاد نمودار ساده با QPainter
        self.chart_widget = QWidget()
        self.chart_widget.setObjectName("chartWidget")
        self.chart_widget.setMinimumHeight(300)

        # تولید داده‌های نمونه برای نمودار
        self.chart_data = [random.uniform(20, 80) for _ in range(15)]

        # اضافه کردن نمودار
        chart_layout.addWidget(self.chart_widget)

        # اضافه کردن کنترل‌های نمودار
        chart_controls = QWidget()
        chart_controls_layout = QHBoxLayout(chart_controls)
        chart_controls_layout.setContentsMargins(0, 10, 0, 0)

        # ایجاد دکمه‌های کنترل نمودار
        chart_btns = ["Line Chart", "Bar Chart", "Pie Chart", "Scatter Plot"]
        for btn_text in chart_btns:
            btn = QPushButton(btn_text)
            btn.setObjectName("chartTypeButton")
            chart_controls_layout.addWidget(btn)

        chart_controls_layout.addStretch()

        chart_layout.addWidget(chart_controls)
        layout.addWidget(chart_container)

    def _create_table_area(self, layout):
        """ایجاد ناحیه جدول"""
        table_container = QWidget()
        table_container.setObjectName("tableContainer")

        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(0, 0, 0, 0)

        # ایجاد جدول
        self.table_widget = QTableWidget()
        self.table_widget.setObjectName("dataTable")
        self.table_widget.setRowCount(20)
        self.table_widget.setColumnCount(6)

        # تنظیم هدرهای جدول
        headers = ["ID", "Name", "Value", "Status", "Date", "Action"]
        self.table_widget.setHorizontalHeaderLabels(headers)

        # پر کردن جدول با داده‌های نمونه
        status_options = ["Active", "Pending", "Completed", "Failed"]
        for row in range(20):
            for col in range(6):
                if col == 0:
                    item = QTableWidgetItem(f"{row + 1}")
                elif col == 1:
                    item = QTableWidgetItem(f"Data Point {row + 1}")
                elif col == 2:
                    item = QTableWidgetItem(f"{random.uniform(10, 100):.2f}")
                elif col == 3:
                    item = QTableWidgetItem(random.choice(status_options))
                elif col == 4:
                    item = QTableWidgetItem(
                        f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
                    )
                else:
                    btn = QPushButton("View")
                    btn.setObjectName("tableActionButton")
                    self.table_widget.setCellWidget(row, col, btn)
                    continue

                item.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setItem(row, col, item)

        # تنظیم ستون‌ها
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setVisible(False)

        table_layout.addWidget(self.table_widget)
        layout.addWidget(table_container)

    def _create_settings_area(self, layout):
        """ایجاد ناحیه تنظیمات"""
        settings_container = QWidget()
        settings_container.setObjectName("settingsContainer")

        settings_layout = QVBoxLayout(settings_container)
        settings_layout.setContentsMargins(20, 20, 20, 20)

        # بخش انتخاب تم
        theme_group = QGroupBox("🎨 Theme Settings")
        theme_group.setObjectName("themeGroup")

        theme_layout = QVBoxLayout(theme_group)

        # انتخاب تم
        theme_label = QLabel("Select Theme:")
        theme_label.setObjectName("settingsLabel")

        theme_combo = QComboBox()
        theme_combo.setObjectName("themeCombo")
        theme_combo.addItems(["Light Flat", "Dark Flat", "Blue Flat", "Green Flat"])
        theme_combo.setCurrentText("Light Flat")
        theme_combo.currentTextChanged.connect(self.change_theme_by_name)

        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(theme_combo)

        # بخش تنظیمات نمایش
        display_group = QGroupBox("🖥️ Display Settings")
        display_group.setObjectName("displayGroup")

        display_layout = QGridLayout(display_group)

        # اضافه کردن کنترل‌های نمایش
        display_settings = [
            ("Show Grid Lines", QCheckBox()),
            ("Animation Speed", QSlider(Qt.Horizontal)),
            ("Chart Opacity", QSpinBox()),
            ("Font Size", QComboBox()),
        ]

        for i, (label, widget) in enumerate(display_settings):
            label_widget = QLabel(label)
            label_widget.setObjectName("settingsLabel")
            display_layout.addWidget(label_widget, i, 0)
            display_layout.addWidget(widget, i, 1)

            # تنظیمات اولیه برای ویجت‌ها
            if isinstance(widget, QSlider):
                widget.setRange(1, 10)
                widget.setValue(5)
            elif isinstance(widget, QSpinBox):
                widget.setRange(10, 100)
                widget.setValue(80)
            elif isinstance(widget, QComboBox):
                widget.addItems(["Small", "Medium", "Large"])
                widget.setCurrentText("Medium")

        # اضافه کردن گروه‌ها به لایه
        settings_layout.addWidget(theme_group)
        settings_layout.addWidget(display_group)
        settings_layout.addStretch()

        layout.addWidget(settings_container)

    def paint_chart(self):
        """رسم نمودار"""
        if hasattr(self, 'chart_widget'):
            # تابع paintEvent برای chart_widget
            def paint_event(event):
                painter = QPainter(self.chart_widget)
                painter.setRenderHint(QPainter.Antialiasing)

                # پس‌زمینه
                painter.fillRect(
                    self.chart_widget.rect(), QColor(self.theme["chart_bg"])
                )

                # اندازه‌ها
                width = self.chart_widget.width()
                height = self.chart_widget.height()

                # رسم خطوط شبکه
                painter.setPen(QPen(QColor(self.theme["chart_grid"]), 1))
                grid_size = 40
                for x in range(0, width, grid_size):
                    painter.drawLine(x, 0, x, height)
                for y in range(0, height, grid_size):
                    painter.drawLine(0, y, width, y)

                # اگر داده وجود دارد
                if hasattr(self, 'chart_data') and self.chart_data:
                    # رسم خط نمودار
                    painter.setPen(QPen(QColor(self.theme["accent"]), 3))

                    points = []
                    max_val = max(self.chart_data)
                    min_val = min(self.chart_data)
                    range_val = max_val - min_val if max_val != min_val else 1

                    for i, value in enumerate(self.chart_data):
                        x = (
                            40 + (i * (width - 80) / (len(self.chart_data) - 1))
                            if len(self.chart_data) > 1
                            else width / 2
                        )
                        y = (
                            height
                            - 40
                            - ((value - min_val) / range_val * (height - 80))
                        )
                        points.append(QPoint(int(x), int(y)))

                    # رسم خط‌های اتصال
                    for i in range(len(points) - 1):
                        painter.drawLine(points[i], points[i + 1])

                    # رسم نقاط
                    painter.setBrush(QBrush(QColor(self.theme["success"])))
                    for point in points:
                        painter.drawEllipse(point, 6, 6)

                painter.end()

            self.chart_widget.paintEvent = paint_event
            self.chart_widget.update()

    def apply_theme(self):
        """اعمال تم انتخاب شده به تمام اجزای برنامه"""
        self.theme = ThemeManager.THEMES[self.current_theme]

        # استایل اصلی
        main_style = f"""
            QWidget {{
                background-color: {self.theme["primary"]};
                color: {self.theme["text_primary"]};
            }}
        """
        self.setStyleSheet(main_style)

        # نوار عنوان
        title_bar_style = f"""
            QWidget#titleBar {{
                background: {self.theme["titlebar_gradient"]};
                border-bottom: 2px solid {self.theme["border"]};
            }}
            
            QLabel#titleLabel {{
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 5px;
            }}
            
            QPushButton#titleButton {{
                border: none;
                border-radius: 18px;
                color: white;
                font-weight: bold;
                font-size: 16px;
            }}
            
            QPushButton#titleButton:hover {{
                background-color: rgba(255, 255, 255, 0.2);
            }}
        """
        self.title_bar.setStyleSheet(title_bar_style)

        # نوار تنظیمات
        settings_bar_style = f"""
            QWidget#settingsBar {{
                background-color: {self.theme["secondary"]};
                border-bottom: 1px solid {self.theme["border"]};
            }}
            
            QPushButton#flatButton {{
                background-color: {self.theme["card"]};
                color: {self.theme["text_primary"]};
                border: 1px solid {self.theme["border"]};
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: 500;
                font-size: 13px;
            }}
            
            QPushButton#flatButton:hover {{
                background-color: {self.theme["accent"]};
                color: white;
                border-color: {self.theme["accent_hover"]};
            }}
        """
        self.settings_bar.setStyleSheet(settings_bar_style)

        # نوار کناری
        sidebar_style = f"""
            QWidget#sidebar {{
                background-color: {self.theme["sidebar"]};
                border-right: 1px solid {self.theme["border"]};
            }}
            
            QLabel#sidebarTitle {{
                color: {self.theme["accent"]};
                font-size: 18px;
                font-weight: bold;
                padding-bottom: 10px;
                border-bottom: 2px solid {self.theme["accent"]};
            }}
            
            QListWidget#processList {{
                background-color: {self.theme["card"]};
                border: 1px solid {self.theme["border"]};
                border-radius: 8px;
                outline: none;
            }}
            
            QListWidget#processList::item {{
                border-bottom: 1px solid {self.theme["border_light"]};
            }}
            
            QListWidget#processList::item:selected {{
                background-color: {self.theme["accent"]};
                color: white;
                border-radius: 6px;
            }}
            
            QWidget#processItem {{
                background-color: transparent;
            }}
            
            QLabel#processItemTitle {{
                color: {self.theme["text_primary"]};
                font-size: 14px;
                font-weight: 500;
            }}
            
            QLabel#processItemDesc {{
                color: {self.theme["text_light"]};
                font-size: 11px;
            }}
            
            QGroupBox#filterGroup {{
                color: {self.theme["accent"]};
                font-size: 14px;
                font-weight: bold;
                border: 1px solid {self.theme["border"]};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
            }}
            
            QGroupBox#filterGroup::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }}
            
            QRadioButton#timeFilterRadio {{
                color: {self.theme["text_primary"]};
                padding: 5px;
                font-size: 12px;
            }}
            
            QRadioButton#timeFilterRadio::indicator {{
                width: 16px;
                height: 16px;
            }}
            
            QPushButton#startButton {{
                background-color: {self.theme["accent"]};
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }}
            
            QPushButton#startButton:hover {{
                background-color: {self.theme["accent_hover"]};
            }}
        """
        self.sidebar.setStyleSheet(sidebar_style)

        # ناحیه اصلی
        main_area_style = f"""
            QWidget#mainArea {{
                background-color: {self.theme["primary"]};
            }}
            
            QLabel#mainTitle {{
                color: {self.theme["text_primary"]};
                font-size: 20px;
                font-weight: bold;
                padding-bottom: 5px;
            }}
            
            QTabWidget#tabWidget::pane {{
                background-color: {self.theme["card"]};
                border: 1px solid {self.theme["border"]};
                border-radius: 8px;
            }}
            
            QTabBar::tab {{
                background-color: {self.theme["secondary"]};
                color: {self.theme["text_primary"]};
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-size: 13px;
                font-weight: 500;
                border: 1px solid {self.theme["border"]};
                border-bottom: none;
            }}
            
            QTabBar::tab:selected {{
                background-color: {self.theme["accent"]};
                color: white;
            }}
            
            QTabBar::tab:hover {{
                background-color: {self.theme["accent_hover"]};
                color: white;
            }}
            
            QWidget#chartContainer {{
                background-color: {self.theme["card"]};
                border: 1px solid {self.theme["border"]};
                border-radius: 8px;
            }}
            
            QWidget#chartWidget {{
                background-color: {self.theme["chart_bg"]};
                border-radius: 6px;
            }}
            
            QPushButton#chartTypeButton {{
                background-color: {self.theme["secondary"]};
                color: {self.theme["text_primary"]};
                border: 1px solid {self.theme["border"]};
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
            }}
            
            QPushButton#chartTypeButton:hover {{
                background-color: {self.theme["accent"]};
                color: white;
            }}
            
            QWidget#tableContainer {{
                background-color: {self.theme["card"]};
                border: 1px solid {self.theme["border"]};
                border-radius: 8px;
            }}
            
            QTableWidget#dataTable {{
                background-color: {self.theme["card"]};
                color: {self.theme["text_primary"]};
                border: none;
                gridline-color: {self.theme["border"]};
                font-size: 12px;
                selection-background-color: {self.theme["accent"]};
                selection-color: white;
            }}
            
            QHeaderView::section {{
                background-color: {self.theme["table_header"]};
                color: {self.theme["text_primary"]};
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 12px;
            }}
            
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {self.theme["border_light"]};
            }}
            
            QPushButton#tableActionButton {{
                background-color: {self.theme["secondary"]};
                color: {self.theme["text_primary"]};
                border: 1px solid {self.theme["border"]};
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 11px;
            }}
            
            QPushButton#tableActionButton:hover {{
                background-color: {self.theme["accent"]};
                color: white;
            }}
            
            QWidget#settingsContainer {{
                background-color: {self.theme["card"]};
                border: 1px solid {self.theme["border"]};
                border-radius: 8px;
            }}
            
            QGroupBox#themeGroup, QGroupBox#displayGroup {{
                color: {self.theme["accent"]};
                font-size: 14px;
                font-weight: bold;
                border: 1px solid {self.theme["border"]};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
            }}
            
            QGroupBox#themeGroup::title, QGroupBox#displayGroup::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }}
            
            QLabel#settingsLabel {{
                color: {self.theme["text_primary"]};
                font-size: 12px;
            }}
            
            QComboBox#themeCombo {{
                background-color: {self.theme["secondary"]};
                color: {self.theme["text_primary"]};
                border: 1px solid {self.theme["border"]};
                border-radius: 6px;
                padding: 6px;
                font-size: 12px;
            }}
            
            QComboBox#themeCombo:hover {{
                border-color: {self.theme["accent"]};
            }}
            
            QPushButton#smallFlatButton {{
                background-color: {self.theme["card"]};
                color: {self.theme["text_primary"]};
                border: 1px solid {self.theme["border"]};
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: 500;
            }}
            
            QPushButton#smallFlatButton:hover {{
                background-color: {self.theme["accent"]};
                color: white;
            }}
            
            QWidget#controlsWidget {{
                background-color: transparent;
            }}
        """
        self.main_area.setStyleSheet(main_area_style)

        # به روزرسانی دکمه تغییر تم
        if self.current_theme == "light_flat":
            self.theme_toggle_btn.setText("🌙 Dark Theme")
        else:
            self.theme_toggle_btn.setText("☀️ Light Theme")

        # به روزرسانی رنگ دکمه‌های کنترل پنجره
        self.btn_min.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.theme["warning"]};
                color: white;
                border: none;
                border-radius: 18px;
                font-weight: bold;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.2);
            }}
        """
        )

        self.btn_max.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.theme["success"]};
                color: white;
                border: none;
                border-radius: 18px;
                font-weight: bold;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.2);
            }}
        """
        )

        self.btn_close.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.theme["error"]};
                color: white;
                border: none;
                border-radius: 18px;
                font-weight: bold;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.2);
            }}
        """
        )

        # به روزرسانی دکمه‌های فلت
        for widget in self.findChildren(QPushButton):
            if widget.objectName() in ["flatButton", "smallFlatButton"]:
                color = widget.property("buttonColor")
                if color:
                    widget.setStyleSheet(
                        f"""
                        QPushButton {{
                            background-color: {self.theme["card"]};
                            color: {self.theme["text_primary"]};
                            border: 1px solid {self.theme["border"]};
                            border-radius: 8px;
                            font-weight: 500;
                        }}
                        QPushButton:hover {{
                            background-color: {color};
                            color: white;
                            border-color: {color};
                        }}
                    """
                    )

        # رسم مجدد نمودار
        self.paint_chart()

    def toggle_theme(self):
        """تغییر تم بین حالت روشن و تاریک"""
        if self.current_theme == "light_flat":
            self.current_theme = "dark_flat"
        else:
            self.current_theme = "light_flat"

        self.apply_theme()

    def change_theme_by_name(self, theme_name):
        """تغییر تم بر اساس نام انتخاب شده"""
        theme_map = {
            "Light Flat": "light_flat",
            "Dark Flat": "dark_flat",
            "Blue Flat": "light_flat",  # در حال حاضر فقط دو تم داریم
            "Green Flat": "light_flat",
        }

        if theme_name in theme_map:
            self.current_theme = theme_map[theme_name]
            self.apply_theme()

    def _connect_events(self):
        """اتصال رویدادهای برنامه به توابع مربوطه"""
        self.process_list.currentRowChanged.connect(self._on_process_changed)
        self.start_btn.clicked.connect(self._on_start_processing)

        # اتصال رویداد تغییر اندازه برای رسم مجدد نمودار
        self.chart_widget.resizeEvent = lambda event: self.paint_chart()

    def _on_process_changed(self, index):
        """تابع مدیریت تغییر پردازش انتخاب شده"""
        print(f"Selected process: {index}")
        # در اینجا می‌توانید منطق تغییر نمایش داده‌ها بر اساس پردازش انتخاب شده را اضافه کنید

    def _on_start_processing(self):
        """شروع پردازش داده‌ها"""
        print("Starting data processing...")

        # شبیه‌سازی پردازش
        self.start_btn.setText("⏳ Processing...")
        self.start_btn.setEnabled(False)

        # ایجاد داده‌های جدید برای نمودار
        self.chart_data = [random.uniform(10, 90) for _ in range(15)]

        # تأخیر برای شبیه‌سازی پردازش
        QTimer.singleShot(1500, self._finish_processing)

    def _finish_processing(self):
        """پایان پردازش داده‌ها"""
        self.start_btn.setText("✅ Processing Complete")
        self.paint_chart()

        # بازنشانی دکمه پس از 2 ثانیه
        QTimer.singleShot(2000, lambda: self.start_btn.setText("🚀 Start Processing"))
        QTimer.singleShot(2000, lambda: self.start_btn.setEnabled(True))

    def toggle_maximize(self):
        """تغییر حالت پنجره بین حداکثر و حالت عادی"""
        if self.isMaximized():
            self.showNormal()
            self.btn_max.setText("□")
        else:
            self.showMaximized()
            self.btn_max.setText("🗗")

    def mousePressEvent(self, event):
        """مدیریت رویداد کلیک ماوس برای قابلیت کشیدن پنجره"""
        if event.button() == Qt.LeftButton and event.pos().y() <= 50:
            # ذخیره موقعیت کلیک برای محاسبه حرکت
            self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        """مدیریت رویداد حرکت ماوس برای کشیدن پنجره"""
        if event.buttons() == Qt.LeftButton and hasattr(self, 'dragPos'):
            # محاسبه موقعیت جدید پنجره بر اساس حرکت ماوس
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()

    def showEvent(self, event):
        """هنگام نمایش پنجره، نمودار را رسم کن"""
        super().showEvent(event)
        QTimer.singleShot(100, self.paint_chart)


# نقطه ورود اصلی برنامه
if __name__ == "__main__":
    # ایجاد برنامه Qt
    app = QApplication(sys.argv)

    # تنظیم استایل کلی برنامه به Fusion
    app.setStyle(QStyleFactory.create("Fusion"))

    # تنظیم فونت بهتر
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # ایجاد و نمایش پنجره اصلی
    window = ModernWindow()
    window.show()

    # اجرای حلقه رویداد برنامه
    sys.exit(app.exec())
    # اجرای حلقه رویداد برنامه
    sys.exit(app.exec())
