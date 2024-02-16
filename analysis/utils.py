import pandas as pd
import numpy as np
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
