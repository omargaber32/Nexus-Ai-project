import sys
import os

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QCheckBox, QDialog, QHeaderView, QAbstractItemView, QGridLayout,
    QFrame, QScrollArea, QSizePolicy, QMessageBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

import matplotlib
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from config import container
from state import setPlannedSteps

#  Constants 

DOWNLOAD_DIR = "./"

#  Helpers 


def _sep() -> QFrame:
    """Thin horizontal separator line."""
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setStyleSheet("color:#e0e0e0;")
    return line


#  Flight Chart 


class FlightChart(FigureCanvas):
    """Matplotlib line chart of two aircraft paths, embedded in PySide6."""

    COLOR_A = "#1565C0"
    COLOR_B = "#C62828"

    def __init__(self, config_data: dict, parent=None):
        self.fig = Figure(figsize=(9, 3.8), dpi=110)
        self.fig.patch.set_facecolor("#FAFBFC")
        self.fig.subplots_adjust(left=0.10, right=0.96, top=0.90, bottom=0.16)
        super().__init__(self.fig)
        self.setParent(parent)
        self.ax = self.fig.add_subplot(111)
        self.data = config_data
        self.show_planned = True
        self._draw()

    def _draw(self):
        ax = self.ax
        ax.clear()
        ax.set_facecolor("#ffffff")

        d = self.data
        a0, at = d["a_start"], d["a_target"]
        b0, bt = d["b_start"], d["b_target"]
        path_a = list(d.get("decision_sequence_first", []))
        path_b = list(d.get("decision_sequence_second", []))

        # step 0 = initial position
        full_a = [a0] + path_a
        full_b = [b0] + path_b
        steps = list(range(len(full_a)))
        n = len(full_a)

        # X = step,  Y = altitude
        ax.plot(steps, full_a, "o-", color=self.COLOR_A, lw=2.3, ms=7,
                mfc="white", mew=2, label="Aircraft A", zorder=5)
        ax.plot(steps, full_b, "s-", color=self.COLOR_B, lw=2.3, ms=7,
                mfc="white", mew=2, label="Aircraft B", zorder=5)

        if self.show_planned:
            # Use setPlannedSteps from state.py for planned paths
            planned_a = [a0] + setPlannedSteps(a0, at)
            planned_b = [b0] + setPlannedSteps(b0, bt,True)
            # Truncate to match actual path length
            planned_a = planned_a[:n]
            planned_b = planned_b[:n]

            ax.plot(steps[:n], planned_a, "--", color=self.COLOR_A, lw=1.4,
                    alpha=0.35, label="Planned A", zorder=3)
            ax.plot(steps[:n], planned_b, "--", color=self.COLOR_B, lw=1.4,
                    alpha=0.35, label="Planned B", zorder=3)

        ax.set_xlabel("Step", fontsize=11, color="#444", labelpad=8)
        ax.set_ylabel("Altitude Level", fontsize=11, color="#444", labelpad=8)
        ax.set_xlim(-0.3, max(n - 0.7, 6.7))
        ax.set_xticks(range(0, max(n, 7)))
        ax.set_ylim(0.5, 10.5)
        ax.set_yticks(range(1, 11))
        ax.tick_params(colors="#666", labelsize=9)
        ax.grid(False)
        for spine in ax.spines.values():
            spine.set_color("#ddd")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend(loc="best", fontsize=9, framealpha=0.9, edgecolor="#ddd")

        self.draw()

    def toggle_planned(self, visible: bool):
        self.show_planned = visible
        self._draw()


#  Config Tab 


class ConfigTab(QWidget):
    """One tab per configuration — chart + outcomes + node table + nav."""

    NODE_PREVIEW = 8

    def __init__(self, data: dict, idx: int, total: int, parent=None):
        super().__init__(parent)
        self.data = data
        self.idx = idx
        self.total = total
        self._build()

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setSpacing(14)
        lay.setContentsMargins(24, 18, 24, 18)

        #  Chart 
        self.chart = FlightChart(self.data, self)
        self.chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        lay.addWidget(self.chart)

        #  Planned-path checkbox
        self.cb = QCheckBox("Show Planned Paths")
        self.cb.setChecked(True)
        self.cb.toggled.connect(self.chart.toggle_planned)
        cb_row = QHBoxLayout()
        cb_row.addStretch()
        cb_row.addWidget(self.cb)
        cb_row.addStretch()
        lay.addLayout(cb_row)

        lay.addWidget(_sep())

        #  Outcome labels
        grid = QGridLayout()
        grid.setSpacing(8)
        outcomes = [
            ("Path of Aircraft A:",      self.data.get("decision_sequence_first", [])),
            ("Path of Aircraft B:",      self.data.get("decision_sequence_second", [])),
            ("Deviation of Aircraft A:", self.data.get("deviation_first", 0)),
            ("Deviation of Aircraft B:", self.data.get("deviation_second", 0)),
            ("Conflict Avoided:",        self.data.get("is_conflict_avoided", "N/A")),
        ]
        for r, (lbl, val) in enumerate(outcomes):
            k = QLabel(lbl)
            k.setFont(QFont("Segoe UI", 11, QFont.Bold))
            k.setStyleSheet("color:#2c3e50;")
            v = QLabel(str(val))
            v.setFont(QFont("Segoe UI", 11))
            v.setStyleSheet("color:#546e7a;")
            v.setWordWrap(True)
            grid.addWidget(k, r, 0, Qt.AlignTop)
            grid.addWidget(v, r, 1, Qt.AlignTop)
        lay.addLayout(grid)

        lay.addWidget(_sep())

        #  Comparison table
        title = QLabel("Node Evaluation Comparison")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title.setStyleSheet("color:#2c3e50;")
        lay.addWidget(title)

        self.tbl = QTableWidget()
        self._fill_table()
        self.tbl.setMaximumHeight(260)
        lay.addWidget(self.tbl)

        ab_n = self.data.get("num_of_alphabeta_nodes", 0)
        mm_n = self.data.get("num_of_minimax_nodes", 0)
        cnt = QLabel(f"Total  —  Alpha-Beta: {ab_n} nodes   |   Minimax: {mm_n} nodes")
        cnt.setFont(QFont("Segoe UI", 10))
        cnt.setStyleSheet("color:#78909c;")
        cnt.setAlignment(Qt.AlignCenter)
        lay.addWidget(cnt)

        show_btn = QPushButton("Show All Nodes")
        show_btn.setCursor(Qt.PointingHandCursor)
        show_btn.clicked.connect(self._show_all)
        lay.addWidget(show_btn)

        lay.addStretch()

        #  Navigation buttons
        nav = QHBoxLayout()
        nav.addStretch()
        if self.idx > 0:
            self.back_btn = QPushButton("\u2190  Back")
            self.back_btn.setFixedWidth(120)
            self.back_btn.setCursor(Qt.PointingHandCursor)
            nav.addWidget(self.back_btn)
        if self.idx < self.total:
            self.next_btn = QPushButton("Next  \u2192")
            self.next_btn.setFixedWidth(120)
            self.next_btn.setCursor(Qt.PointingHandCursor)
            nav.addWidget(self.next_btn)
        lay.addLayout(nav)

        scroll.setWidget(page)
        outer.addWidget(scroll)

    #  small comparison table

    def _fill_table(self):
        ab = self.data.get("nodes_evaluated", [])
        mm = self.data.get("nodes_evaluated_minimax", [])
        rows = min(max(len(ab), len(mm)), self.NODE_PREVIEW)

        self.tbl.setColumnCount(2)
        self.tbl.setRowCount(rows)
        self.tbl.setHorizontalHeaderLabels(["Alpha-Beta", "Minimax"])
        self.tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl.verticalHeader().setVisible(False)
        self.tbl.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tbl.setSelectionMode(QAbstractItemView.NoSelection)

        for i in range(rows):
            self.tbl.setItem(
                i, 0,
                QTableWidgetItem(str(ab[i]) if i < len(ab) else "\u2014"))
            self.tbl.setItem(
                i, 1,
                QTableWidgetItem(str(mm[i]) if i < len(mm) else "\u2014"))

    #  "Show All Nodes" popup

    def _show_all(self):
        ab = self.data.get("nodes_evaluated", [])
        mm = self.data.get("nodes_evaluated_minimax", [])
        n = max(len(ab), len(mm))

        dlg = QDialog(self)
        dlg.setWindowTitle(f"All Evaluated Nodes  —  Config {self.idx + 1}")
        dlg.setMinimumSize(750, 500)
        dlg.resize(820, 560)

        vl = QVBoxLayout(dlg)
        hdr = QLabel("All Evaluated Nodes")
        hdr.setFont(QFont("Segoe UI", 13, QFont.Bold))
        hdr.setStyleSheet("color:#2c3e50; margin-bottom:6px;")
        vl.addWidget(hdr)

        tbl = QTableWidget(n, 2)
        tbl.setHorizontalHeaderLabels(
            [f"Alpha-Beta  ({len(ab)} nodes)",
             f"Minimax  ({len(mm)} nodes)"])
        tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tbl.verticalHeader().setVisible(False)
        tbl.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tbl.setSelectionMode(QAbstractItemView.NoSelection)

        for i in range(n):
            if i < len(ab):
                tbl.setItem(i, 0, QTableWidgetItem(str(ab[i])))
            if i < len(mm):
                tbl.setItem(i, 1, QTableWidgetItem(str(mm[i])))
        vl.addWidget(tbl)

        close_btn = QPushButton("Close")
        close_btn.setFixedWidth(100)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(dlg.close)
        cl = QHBoxLayout()
        cl.addStretch()
        cl.addWidget(close_btn)
        vl.addLayout(cl)

        dlg.exec()


#  Summary Tab 


class SummaryTab(QWidget):
    """Summary table across all configs + Save-to-PDF."""

    FIELDS = {
        "decision_sequence_first":  "Path of A",
        "decision_sequence_second": "Path of B",
        "deviation_first":          "Deviation of A",
        "deviation_second":         "Deviation of B",
        "num_of_alphabeta_nodes":   "Alpha-Beta Nodes",
        "num_of_minimax_nodes":     "Minimax Nodes",
        "is_conflict_avoided":      "Conflict Avoided",
    }

    def __init__(self, cont: list, parent=None):
        super().__init__(parent)
        self.cont = cont
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setSpacing(16)
        lay.setContentsMargins(24, 20, 24, 20)

        title = QLabel("Summary Table")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setStyleSheet("color:#2c3e50;")
        lay.addWidget(title)

        ncols = len(self.cont) + 1
        self.tbl = QTableWidget(len(self.FIELDS), ncols)
        self.tbl.setHorizontalHeaderLabels(
            ["Field"] + [f"Config {i+1}" for i in range(len(self.cont))])
        self.tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl.verticalHeader().setVisible(False)
        self.tbl.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tbl.setSelectionMode(QAbstractItemView.NoSelection)
        self.tbl.setAlternatingRowColors(True)

        for r, (key, label) in enumerate(self.FIELDS.items()):
            fi = QTableWidgetItem(label)
            fi.setFont(QFont("Segoe UI", 10, QFont.Bold))
            self.tbl.setItem(r, 0, fi)
            for c, cfg in enumerate(self.cont):
                self.tbl.setItem(r, c + 1, QTableWidgetItem(str(cfg.get(key, "-"))))

        lay.addWidget(self.tbl)

        save_btn = QPushButton("Save to PDF")
        save_btn.setFixedWidth(160)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.clicked.connect(self._save_pdf)
        lay.addWidget(save_btn, alignment=Qt.AlignCenter)

    #  PDF export

    def _save_pdf(self):
        try:
            os.makedirs(DOWNLOAD_DIR, exist_ok=True)

            fig, ax = plt.subplots(figsize=(11, 4.5))
            ax.axis("off")

            cols = ["Field"] + [f"Config {i+1}" for i in range(len(self.cont))]
            cells = []
            for key, label in self.FIELDS.items():
                row = [label] + [str(cfg.get(key, "-")) for cfg in self.cont]
                cells.append(row)

            tbl = ax.table(
                cellText=cells,
                colLabels=cols,
                cellLoc="center",
                loc="center",
                colWidths=[0.22] + [0.19] * len(self.cont),
            )
            tbl.auto_set_font_size(False)
            tbl.set_fontsize(9)
            tbl.scale(1, 1.8)

            for (r, c), cell in tbl.get_celld().items():
                if r == 0:
                    cell.set_facecolor("#2c3e50")
                    cell.set_text_props(color="white", fontweight="bold")
                else:
                    cell.set_facecolor("#f8f9fa" if r % 2 == 0 else "#ffffff")
                cell.set_edgecolor("#ddd")

            fig.suptitle(
                "Nexus Air Traffic Conflict Resolver  -  Summary",
                fontsize=14, fontweight="bold", color="#2c3e50", y=0.98,
            )
            path = os.path.join(DOWNLOAD_DIR, "summary.pdf")
            fig.savefig(path, bbox_inches="tight", facecolor="white")
            plt.close(fig)

            QMessageBox.information(self, "Saved",
                                    f"Summary table saved to:\n{path}")
        except Exception as exc:
            QMessageBox.critical(self, "Error",
                                 f"Failed to save PDF:\n{exc}")


#  Main Window 


class NexusATCRWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nexus Air Traffic Conflict Resolver")
        self.setMinimumSize(960, 760)
        self.resize(1020, 820)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)

        self.tabs = QTabWidget()
        root.addWidget(self.tabs)

        # Config tabs
        self._cfg_tabs: list[ConfigTab] = []
        for i, d in enumerate(container):
            tab = ConfigTab(d, i, len(container), self)
            self._cfg_tabs.append(tab)
            self.tabs.addTab(tab, f"Config {i + 1}")

        # Summary tab
        self._sum_tab = SummaryTab(container, self)
        self.tabs.addTab(self._sum_tab, "Summary")

        # Wire Next / Back navigation
        for i, tab in enumerate(self._cfg_tabs):
            if hasattr(tab, "next_btn"):
                target = i + 1
                tab.next_btn.clicked.connect(
                    lambda _, t=target: self.tabs.setCurrentIndex(t))
            if hasattr(tab, "back_btn"):
                target = i - 1
                tab.back_btn.clicked.connect(
                    lambda _, t=target: self.tabs.setCurrentIndex(t))


#  Stylesheet 

STYLE = """
QMainWindow {
    background: #f5f6fa;
}
QTabWidget::pane {
    border: none;
    background: #fff;
}
QTabBar::tab {
    background: #ecf0f1;
    color: #555;
    padding: 10px 26px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-size: 13px;
    font-weight: bold;
}
QTabBar::tab:selected {
    background: #fff;
    color: #2c3e50;
    border-bottom: 2px solid #1976D2;
}
QTabBar::tab:hover {
    background: #dfe6e9;
}
QPushButton {
    background: #1976D2;
    color: white;
    border: none;
    padding: 8px 20px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: bold;
}
QPushButton:hover {
    background: #1565C0;
}
QPushButton:pressed {
    background: #0D47A1;
}
QTableWidget {
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    gridline-color: #f0f0f0;
    font-size: 11px;
}
QTableWidget::item {
    padding: 6px;
}
QHeaderView::section {
    background: #ecf0f1;
    color: #2c3e50;
    padding: 8px;
    border: none;
    font-weight: bold;
    font-size: 11px;
}
QCheckBox {
    font-size: 12px;
    color: #546e7a;
    spacing: 8px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid #b0bec5;
}
QCheckBox::indicator:checked {
    background: #1976D2;
    border-color: #1976D2;
}
QScrollArea {
    border: none;
}
QScrollBar:vertical {
    border: none;
    background: #f5f6fa;
    width: 10px;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background: #ccc;
    min-height: 30px;
    border-radius: 5px;
}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}
"""


#  Entry Point 


def launch_gui():
    """Create and show the GUI window. Call after running all Config objects."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)

    win = NexusATCRWindow()
    win.show()
    sys.exit(app.exec())