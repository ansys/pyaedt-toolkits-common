from PySide6.QtWidgets import QApplication, QTableWidgetItem
import sys
from ansys.aedt.toolkits.common.ui.utils.widgets import PyTableWidget

# Initialize a QApplication instance
app = QApplication(sys.argv)

# Create a `PyTableWidget` instance
table = PyTableWidget()

# Define the data
data = [['Hello', 'World'], ['Example', 'Data'], ['More', 'Rows']]

# Set the number of rows and columns in the table
table.setRowCount(len(data))
table.setColumnCount(len(data[0]))

# Populate the table with data
for i in range(len(data)):
    for j in range(len(data[i])):
        table.setItem(i, j, QTableWidgetItem(str(data[i][j])))

# Show the `PyTableWidget` instance
table.show()

# Start the application's event loop
sys.exit(app.exec())