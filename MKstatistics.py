"""
Megakaryocyte Statistics Script

Author: Lilly-Flore CELMA

This script analyzes measurements from a TSV file containing megakaryocyte (MK) data. It generates statistical
histograms and tables, and combines them into a final PDF report. The analysis includes various parameters such as
the number of nuclei, area, diameter, circularity, and hematoxylin values.

1. Load Data:
   - Reads the measurements TSV file into a pandas DataFrame.

2. Generate Histograms:
   - Produces histograms for different MK and nuclei parameters, such as number, area, diameter, circularity,
   and hematoxylin.

3. Create Tables:
   - Computes and creates tables with summary statistics for MK and nuclei parameters.

4. Combine Histograms and Tables:
   - Merges the generated histograms and tables into separate PDFs.

5. Generate Final Report:
   - Combines the histograms and tables PDFs into a single comprehensive report.

Note: Exception handling is implemented for potential errors during file reading, data processing, and PDF creation.
"""
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer

########## GET TSV FILE ##########

# Load the TSV file into a pandas DataFrame, specifying the delimiter
measurements_file_tsv = '/Users/lilly-flore/Desktop/Bachelor_Project/MKProject/measurements.tsv'

try:
    df = pd.read_csv(measurements_file_tsv, delimiter='\t')
except FileNotFoundError:
    print(f"Error: The file {measurements_file_tsv} was not found.")
except pd.errors.EmptyDataError:
    print(f"Error: The file {measurements_file_tsv} is empty or contains no data.")
except pd.errors.ParserError:
    print(f"Error: There was an issue parsing the TSV file {measurements_file_tsv}.")


########## FILTER LIST ##########
def filter_list(in_list):
    """
    Filters out elements with NaN values from a list.

    Parameters:
    - list: The input list containing numeric values.

    Returns:
    list: A new list with NaN values removed.
    """
    new_list = [e for e in in_list if not math.isnan(e)]

    return new_list


########## CREATE SCATTER PLOT ##########
def scatter_plot(in_list_of_maps, x_label, y_label):
    """
    Create a scatter plot based on a list of maps, where each map represents data points for a specific image.

    Parameters:
    - list_of_maps (list of dict): A list of dictionaries, each containing data for a specific image.
    - x_label (str): The label for the x-axis, specifying the key in each map corresponding to the x-axis values.
    - y_label (str): The label for the y-axis, specifying the key in each map corresponding to the y-axis values.

    Returns:
    - fig (matplotlib.figure.Figure): The matplotlib figure containing the scatter plot.
    """

    fig, ax = plt.subplots()
    unique_images = set(item['Image'] for item in in_list_of_maps)

    # Iterate over each unique image and add a scatter plot
    for image in unique_images:
        filtered_maps = [item for item in in_list_of_maps if item['Image'] == image]
        x_values = [item[x_label] for item in filtered_maps]
        y_values = [item[y_label] for item in filtered_maps]

        ax.scatter(x_values, y_values, label=image.split('_')[0])

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(f"{x_label} vs {y_label}")
    ax.legend()

    # Explicitly close the figure to release memory
    plt.close(fig)

    return fig


########## CREATE STATISTICS HISTOGRAM ##########
def extract_unit_scientific_notation(number):
    """
    Extracts the unit from a number in scientific notation.

    Parameters:
    - number (float): The number in scientific notation.

    Returns:
    float: The extracted unit.
    """
    # Use scientific notation format with 2 decimal places
    scientific_notation = "{:e}".format(number)

    # Extract the unit (part after "e")
    after_e_part = scientific_notation.split('e')[0]

    return float(after_e_part)


def plot_histogram(in_list, x_label, y_label):
    """
    Plots a histogram for a given list of data.

    Parameters:
    - list (list): The list of data.
    - x_label (str): The label for the x-axis.
    - y_label (str): The label for the y-axis.

    Returns:
    matplotlib.figure.Figure: The matplotlib figure object.
    """

    try:
        # Calculate the bin edges and the number of occurrences in each bin
        min_value = min(in_list)
        max_value = max(in_list)
        gap = abs(max_value) - abs(min_value)

        if 0.01 <= gap <= 0.01:
            bin_width = 0.001
        elif 0.1 < gap <= 2:
            bin_width = 0.1
        elif 2 < gap <= 20:
            bin_width = 1
        elif 20 < gap <= 100:
            bin_width = 5
        elif 100 < gap <= 1000:
            bin_width = 10
        elif 1000 < gap <= 10000:
            bin_width = 50
        else:
            bin_width = 1

        num_bins = math.ceil(gap / bin_width)

        # Display the histogram
        fig, ax = plt.subplots()
        ax.hist(in_list, bins=num_bins, color='grey', edgecolor='darkgrey')
        ax.set_title(f"{x_label}{' distribution'}")
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.grid(False)

        # Explicitly close the figure to release memory
        plt.close(fig)

        return fig

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


########## CREATE TABLE ##########

def create_table(MK_name, nuc_name, MK_value, nuc_value):
    """
    Creates a table with specified values and styling.

    Parameters:
    - MK_name (str): The name for the first row.
    - nuc_name (str): The name for the second row.
    - MK_value (str): The value for the first row.
    - nuc_value (str): The value for the second row.

    Returns:
    reportlab.platypus.tables.Table: The reportlab table object.
    """

    try:
        data = [
            ["Type", "Value"],
            [MK_name, MK_value],
            [nuc_name, nuc_value]
        ]

        # Create a table with the data
        table = Table(data, colWidths=150, rowHeights=20)

        # Style the table
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 3),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                            ('GRID', (0, 0), (-1, -1), 1, colors.dimgrey),
                            ])

        table.setStyle(style)
        return table

    except Exception as e:
        print(f"Error: An unexpected error occurred in create_table. {e}")


######### CREATE PDF ###########
def create_pdf_with_tables(file_path, in_tables):
    """
    Creates a PDF document with multiple tables.

    Parameters:
    - file_path (str): The path to the PDF file.
    - tables (list): The list of reportlab table objects.
    """

    try:
        # Create a PDF document
        in_pdf = SimpleDocTemplate(file_path, pagesize=letter)

        # Build the content with tables and space between them
        content = []
        for table in in_tables:
            content.append(table)

            # Add space (Spacer) between tables
            content.append(Spacer(1, 12))  # Adjust the second parameter for the desired space

        # Build the PDF document
        in_pdf.build(content)

    except Exception as e:
        print(f"Error: An unexpected error occurred in create_pdf_with_tables. {e}")


def merge_pdfs(pdf1_path, pdf2_path, o_path):
    """
    Merges two PDF files into one.

    Parameters:
    - pdf1_path (str): The path to the first PDF file.
    - pdf2_path (str): The path to the second PDF file.
    - o_path (str): The path to the output PDF file.
    """
    try:
        with open(pdf1_path, 'rb') as file1, open(pdf2_path, 'rb') as file2:
            pdf_reader1 = PdfReader(file1)
            pdf_reader2 = PdfReader(file2)

            # Create a PDF writer
            pdf_writer = PdfWriter()

            # Add pages from the first PDF
            for page_num in range(len(pdf_reader1.pages)):
                page = pdf_reader1.pages[page_num]
                pdf_writer.add_page(page)

            # Add pages from the second PDF
            for page_num in range(len(pdf_reader2.pages)):
                page = pdf_reader2.pages[page_num]
                pdf_writer.add_page(page)

            # Write the combined PDF to the output file
            with open(o_path, 'wb') as output_file:
                pdf_writer.write(output_file)

    except FileNotFoundError:
        print(f"Error: One or both of the PDF files {pdf1_path} and {pdf2_path} not found.")
    except Exception as e:
        print(f"Error: An unexpected error occurred during PDF merge. {e}")


########## INITIATE VALUES ##########

# Create a list to store the maps for each row
list_of_maps = []

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    # Convert the row to a dictionary and append it to the list
    row_map = row.to_dict()
    list_of_maps.append(row_map)

columns_to_extract = ['Image', 'Object ID', 'Name', 'Number of nuclei',
                      'Area µm^2', 'Area Ratio %', 'Nuclei Area µm^2: Mean',
                      'Min diameter µm', 'Nuclei diameter µm: Mean Min', 'Diameter Ratio %: Min'
                                                                         'Max diameter µm',
                      'Nuclei diameter µm: Mean Max', 'Diameter Ratio %: Max',
                      'Circularity', 'Nuclei Circularity µm: Mean', 'Circularity Ratio %',
                      'Hematoxylin: Mean', 'Hematoxylin: Min', 'Hematoxylin: Max',
                      'Nuclei Hematoxylin: Max', 'Nuclei Hematoxylin: Min', 'Nuclei Hematoxylin: Mean',
                      'Nuclei Hematoxylin: Std.Dev.'
                      ]

# Creation of lists
name_list = df['Name'].tolist()
num_nuclei_list = filter_list(df['Number of nuclei'].tolist())

area_list = filter_list(df['Area µm^2'].tolist())
nuc_area_list = filter_list(df['Nuclei Area µm^2: Mean'].tolist())
area_ratio_list = filter_list(df['Area Ratio %'].tolist())

max_diameter_list = filter_list(df['Max diameter µm'].tolist())
nuc_max_diam_list = filter_list(df['Nuclei diameter µm: Mean Max'].tolist())
max_diam_ratio_list = filter_list(df['Diameter Ratio %: Max'].tolist())

min_diameter_list = filter_list(df['Min diameter µm'].tolist())
nuc_min_diam_list = filter_list(df['Nuclei diameter µm: Mean Min'].tolist())
min_diam_ratio_list = filter_list(df['Diameter Ratio %: Min'].tolist())

circularity_list = filter_list(df['Circularity'].tolist())
nuc_circ_list = filter_list(df['Nuclei Circularity µm: Mean'].tolist())
circ_ratio_list = filter_list(df['Circularity Ratio %'].tolist())

min_hema_list = filter_list(df['Hematoxylin: Min'].tolist())
max_hema_list = filter_list(df['Hematoxylin: Max'].tolist())
mean_hema_list = filter_list(df['Hematoxylin: Mean'].tolist())
nuc_min_hema_list = filter_list(df['Nuclei Hematoxylin: Min'].tolist())
nuc_max_hema_list = filter_list(df['Nuclei Hematoxylin: Max'].tolist())
nuc_mean_hema_list = filter_list(df['Nuclei Hematoxylin: Mean'].tolist())
nuc_std_hema_list = filter_list(df['Nuclei Hematoxylin: Std.Dev.'].tolist())

# Create pdf file
graphs_pdf = "Graphs.pdf"
with PdfPages(graphs_pdf) as pdf:
    # Creation of histograms
    y_label_MK = 'Number of Megakaryocytes'
    y_label_nuclei = 'Number of Nuclei'

    num_nuclei_fig = plot_histogram(num_nuclei_list, 'Number of nuclei', y_label_MK)
    pdf.savefig(num_nuclei_fig)

    areaFig = plot_histogram(area_list, 'MK Area µm^2', y_label_MK)
    pdf.savefig(areaFig)
    nuc_area_fig = plot_histogram(nuc_area_list, 'Nuclei Area µm^2', y_label_nuclei)
    pdf.savefig(nuc_area_fig)
    area_ratio_fig = plot_histogram(area_ratio_list, 'Area Ratio %', y_label_MK)
    pdf.savefig(area_ratio_fig)

    max_diam_fig = plot_histogram(max_diameter_list, 'MK max diameter µm', y_label_MK)
    pdf.savefig(max_diam_fig)
    nuc_max_diam_fig = plot_histogram(nuc_max_diam_list, 'Nuclei mean max diameter µm', y_label_nuclei)
    pdf.savefig(nuc_max_diam_fig)
    max_diam_ratio_fig = plot_histogram(max_diam_ratio_list, 'Max diameter Ratio %', y_label_MK)
    pdf.savefig(max_diam_ratio_fig)

    min_diam_fig = plot_histogram(min_diameter_list, 'MK min diameter µm', y_label_MK)
    pdf.savefig(min_diam_fig)
    nuc_min_diam_fig = plot_histogram(nuc_min_diam_list, 'Nuclei mean min diameter µm', y_label_nuclei)
    pdf.savefig(nuc_min_diam_fig)
    min_diam_ratio_fig = plot_histogram(min_diam_ratio_list, 'Min diameter Ratio %', y_label_MK)
    pdf.savefig(min_diam_ratio_fig)

    circularity_fig = plot_histogram(circularity_list, 'MK circularity µm', y_label_MK)
    pdf.savefig(circularity_fig)
    nuc_circ_fig = plot_histogram(nuc_circ_list, 'Nuclei mean circularity µm', y_label_nuclei)
    pdf.savefig(nuc_circ_fig)
    circ_ratio_fig = plot_histogram(circ_ratio_list, 'Circularity Ratio %', y_label_MK)
    pdf.savefig(circ_ratio_fig)

    min_hema_fig = plot_histogram(min_hema_list, 'Hematoxylin: Min', y_label_MK)
    pdf.savefig(min_hema_fig)
    max_hema_fig = plot_histogram(max_hema_list, 'Hematoxylin: Max', y_label_MK)
    pdf.savefig(max_hema_fig)
    mean_hema_fig = plot_histogram(mean_hema_list, 'Hematoxylin: Mean', y_label_MK)
    pdf.savefig(mean_hema_fig)

    nuc_min_hema_fig = plot_histogram(nuc_min_hema_list, 'Hematoxylin: Min', y_label_nuclei)
    pdf.savefig(nuc_min_hema_fig)
    nuc_max_hema_fig = plot_histogram(nuc_max_hema_list, 'Hematoxylin: Max', y_label_nuclei)
    pdf.savefig(nuc_max_hema_fig)
    nuc_mean_hema_fig = plot_histogram(nuc_mean_hema_list, 'Hematoxylin: Mean', y_label_nuclei)
    pdf.savefig(nuc_mean_hema_fig)
    nuc_std_hema_fig = plot_histogram(nuc_std_hema_list, 'Hematoxylin: Std.Dev.', y_label_nuclei)
    pdf.savefig(nuc_std_hema_fig)

    # Creation of scatter plots
    area_circ_scatter = scatter_plot(list_of_maps, 'Area µm^2', 'Circularity')
    pdf.savefig(area_circ_scatter)

tables_pdf = "Tables.pdf"
tables = []

number_table = create_table('Number of megakaryocytes', 'Number of nuclei', len(name_list), sum(num_nuclei_list))
tables.append(number_table)

mean_area_table = create_table('MK mean area', 'Nuclei mean area', f"{round(np.mean(area_list), 2)} (µm^2)",
                               f"{round(np.mean(nuc_area_list), 2)} (µm^2)")
tables.append(mean_area_table)
std_area_table = create_table('MK area std', 'Nuclei area std', f"{round(np.std(area_list), 2)} (µm^2)",
                              f"{round(np.std(nuc_area_list), 2)} (µm^2)")
tables.append(std_area_table)

mean_max_diam_table = create_table('MK mean max diameter', 'Nuclei mean max diameter',
                                   f"{round(np.mean(max_diameter_list), 2)} (µm)",
                                   f"{round(np.mean(nuc_max_diam_list), 2)} (µm)")
tables.append(mean_max_diam_table)
std_max_diam_table = create_table('MK max diameter std', 'Nuclei max diameter std',
                                  f"{round(np.std(max_diameter_list), 2)} (µm)",
                                  f"{round(np.std(nuc_max_diam_list), 2)} (µm)")
tables.append(std_max_diam_table)

mean_min_diam_table = create_table('MK mean min diameter', 'Nuclei mean min diameter',
                                   f"{round(np.mean(min_diameter_list), 2)} (µm)",
                                   f"{round(np.mean(nuc_min_diam_list), 2)} (µm)")
tables.append(mean_min_diam_table)
std_min_diam_table = create_table('MK min diameter std', 'Nuclei min diameter std',
                                  f"{round(np.std(min_diameter_list), 2)} (µm)",
                                  f"{round(np.std(nuc_min_diam_list), 2)} (µm)")
tables.append(std_min_diam_table)

mean_circularity_table = create_table('MK mean circularity', 'Nuclei mean circularity',
                                      f"{round(np.mean(circularity_list), 2)} (µm)",
                                      f"{round(np.mean(nuc_circ_list), 2)} (µm)")
tables.append(mean_circularity_table)
std_circularity_table = create_table('MK circularity std', 'Nuclei circularity std',
                                     f"{round(np.std(circularity_list), 2)} (µm)",
                                     f"{round(np.std(nuc_circ_list), 2)} (µm)")
tables.append(std_circularity_table)

mean_hema_table = create_table('MK mean hematoxylin', 'Nuclei mean hematoxylin', f"{round(np.mean(mean_hema_list), 2)}",
                               f"{round(np.mean(nuc_mean_hema_list), 2)}")
tables.append(mean_hema_table)
mean_hema_table = create_table('MK hematoxylin std', 'Nuclei hematoxylin std', f"{round(np.std(mean_hema_list), 2)}",
                               f"{round(np.mean(nuc_std_hema_list), 2)}")
tables.append(mean_hema_table)

# Create the PDF with multiple tables
create_pdf_with_tables(tables_pdf, tables)

# Merge graph pdf and table pdf
output_path = '/Users/lilly-flore/Desktop/MK_statistics.pdf'
merge_pdfs(tables_pdf, graphs_pdf, output_path)
print("The pdf has been saved under " + output_path)
