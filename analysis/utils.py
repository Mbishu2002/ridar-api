import pandas as pd
import numpy as np
from docx import Document
import json
import matplotlib.pyplot as plt
import io

def perform_analysis(data):
    result = f"Analysis result for {data}"
    return result


def generate_chart(data, chart_type, chart_title):
    if chart_type == 'bar':
        chart_function = plt.bar
    elif chart_type == 'line':
        chart_function = plt.plot
    elif chart_type == 'histogram':
        chart_function = plt.hist
    elif chart_type == 'pie':
        chart_function = plt.pie
    elif chart_type == 'scatter':
        chart_function = plt.scatter
    else:
        raise ValueError(f"Invalid chart type: {chart_type}")

    chart_function(range(len(data)), data)
    plt.xlabel('X-axis Label')
    plt.ylabel('Y-axis Label')
    plt.title(f'{chart_title.capitalize()} Chart')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return buffer




def table2json(docx_filename):
    document = Document(docx_filename)
    tables_data = []

    for table in document.tables:
        table_data = {
            'headers': [cell.text for cell in table.rows[0].cells],
            'rows': []
        }

        for row in table.rows[1:]:
            row_data = [cell.text for cell in row.cells]
            table_data['rows'].append(row_data)

        tables_data.append(table_data)

    return tables_data


