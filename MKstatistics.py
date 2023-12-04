"""
Author: Lilly-Flore CELMA
"""
import PyPDF2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.pagesizes import letter

######################################## GET TSV FILE ########################################
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

################################### CREATE STATISTICS HISTOGRAM ########################################
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

def plot_histogram(list, x_label, y_label):
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
        min_value = min(list)
        max_value = max(list)
        bin_width = (max_value - min_value + 1) / len(set(list))
        gap = max_value - min_value
        if int(gap).__eq__(0):
            new_gap = extract_unit_scientific_notation(gap)
            num_bins = int(new_gap / bin_width)
        else:
            num_bins = int(gap / bin_width)

        # Display the histogram
        fig, ax = plt.subplots()
        ax.hist(list, bins=num_bins, color='grey', edgecolor='darkgrey')
        ax.set_title(f"{x_label}{' distribution'}")
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.grid(False)
        return fig

    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"Error: An unexpected error occurred in plot_histogram. {e}")


#####################################################################################

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

#####################################################################################
def create_pdf_with_tables(file_path, tables):
    """
    Creates a PDF document with multiple tables.

    Parameters:
    - file_path (str): The path to the PDF file.
    - tables (list): The list of reportlab table objects.
    """

    try:
        # Create a PDF document
        pdf = SimpleDocTemplate(file_path, pagesize=letter)

        # Build the content with tables and space between them
        content = []
        for table in tables:
            content.append(table)

            # Add space (Spacer) between tables
            content.append(Spacer(1, 12))  # Adjust the second parameter for the desired space

        # Build the PDF document
        pdf.build(content)

    except Exception as e:
        print(f"Error: An unexpected error occurred in create_pdf_with_tables. {e}")

#####################################################################################

def plot_2_y_for_1_x(x_list, y1_list, y2_list, y1_label, y2_label):
    """
    Plots two Y-values against one X-value.

    Parameters:
    - x_list (list): The list of X-axis values.
    - y1_list (list): The list of Y1-axis values.
    - y2_list (list): The list of Y2-axis values.
    - y1_label (str): The label for Y1-axis.
    - y2_label (str): The label for Y2-axis.

    Returns:
    matplotlib.figure.Figure: The matplotlib figure object.
    """

    try:
        # Plotting
        plt.plot(x_list, y1_list, label=y1_label)
        plt.plot(x_list, y2_list, label=y2_label)

        # Adding labels and title
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Two Y-values for One X-value Plot')

        return plt.savefig('two_y_for_one_x_plot.pdf')

    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"Error: An unexpected error occurred in plot_2_y_for_1_x. {e}")

#####################################################################################
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
            pdf_reader1 = PyPDF2.PdfFileReader(file1)
            pdf_reader2 = PyPDF2.PdfFileReader(file2)

            # Create a PDF writer
            pdf_writer = PyPDF2.PdfFileWriter()

            # Add pages from the first PDF
            for page_num in range(pdf_reader1.numPages):
                page = pdf_reader1.getPage(page_num)
                pdf_writer.addPage(page)

            # Add pages from the second PDF
            for page_num in range(pdf_reader2.numPages):
                page = pdf_reader2.getPage(page_num)
                pdf_writer.addPage(page)

            # Write the combined PDF to the output file
            with open(o_path, 'wb') as output_file:
                pdf_writer.write(output_file)

    except FileNotFoundError:
        print(f"Error: One or both of the PDF files {pdf1_path} and {pdf2_path} not found.")
    except PyPDF2.utils.PdfReadError:
        print(f"Error: There was an issue reading the PDF files {pdf1_path} or {pdf2_path}.")
    except Exception as e:
        print(f"Error: An unexpected error occurred during PDF merge. {e}")

################################### INITIATE VALUES ########################################

columns_to_extract = ['Name', 'Number of nuclei',
                      'Area µm^2', 'Area Ratio %', 'Nuclei Area µm^2: Mean',
                      'Min diameter µm', 'Nuclei diameter µm: Mean Min', 'Diameter Ratio %: Min'
                      'Max diameter µm', 'Nuclei diameter µm: Mean Max', 'Diameter Ratio %: Max',
                      'Circularity', 'Nuclei Circularity µm: Mean', 'Circularity Ratio %',
                      'Nuclei Hematoxylin: Max', 'Nuclei Hematoxylin: Min', 'Nuclei Hematoxylin: Mean', 'Nuclei Hematoxylin: Std.Dev.'
                      ]

# Lists creation
name_list = df['Name'].tolist()
num_nuclei_list = df['Number of nuclei'].tolist()

area_list = df['Area µm^2'].tolist()
nuc_area_list = df['Nuclei Area µm^2: Mean'].tolist()
area_ratio_list = df['Area Ratio %'].tolist()

max_diameter_list = df['Max diameter µm'].tolist()
nuc_max_diam_list = df['Nuclei diameter µm: Mean Max'].tolist()
max_diam_ratio_list = df['Diameter Ratio %: Max'].tolist()

min_diameter_list = df['Min diameter µm'].tolist()
nuc_min_diam_list = df['Nuclei diameter µm: Mean Min'].tolist()
min_diam_ratio_list = df['Diameter Ratio %: Min'].tolist()

circularity_list = df['Circularity'].tolist()
nuc_circ_list = df['Nuclei Circularity µm: Mean'].tolist()
circ_ratio_list = df['Circularity Ratio %'].tolist()

min_hema_list = df['Nuclei Hematoxylin: Min'].tolist()
max_hema_list = df['Nuclei Hematoxylin: Max'].tolist()
mean_hema_list = df['Nuclei Hematoxylin: Mean'].tolist()
std_hema_list = df['Nuclei Hematoxylin: Std.Dev.'].tolist()

# Create pdf file
graphs_pdf = "Graphs.pdf"
with PdfPages(graphs_pdf) as pdf:

    num_nuclei_fig = plot_histogram(num_nuclei_list, 'Number of nuclei', 'Number of Megakaryocytes')
    pdf.savefig(num_nuclei_fig)

    areaFig = plot_histogram(area_list, 'MK Area µm^2', 'Number of Megakaryocytes')
    pdf.savefig(areaFig)
    nuc_area_fig = plot_histogram(nuc_area_list, 'Nuclei Area µm^2', 'Number of Nuclei')
    pdf.savefig(nuc_area_fig)
    area_ratio_fig = plot_histogram(area_ratio_list, 'Area Ratio %', 'Number of Megakaryocytes')
    pdf.savefig(area_ratio_fig)

    max_diam_fig = plot_histogram(max_diameter_list, 'MK max diameter µm', 'Number of Megakaryocytes')
    pdf.savefig(max_diam_fig)
    nuc_max_diam_fig = plot_histogram(nuc_max_diam_list, 'Nuclei mean max diameter µm', 'Number of Nuclei')
    pdf.savefig(nuc_max_diam_fig)
    max_diam_ratio_fig = plot_histogram(max_diam_ratio_list, 'Max diameter Ratio %', 'Number of Megakaryocytes')
    pdf.savefig(max_diam_ratio_fig)

    min_diam_fig = plot_histogram(min_diameter_list, 'MK min diameter µm', 'Number of Megakaryocytes')
    pdf.savefig(min_diam_fig)
    nuc_min_diam_fig = plot_histogram(nuc_min_diam_list, 'Nuclei mean min diameter µm', 'Number of Nuclei')
    pdf.savefig(nuc_min_diam_fig)
    min_diam_ratio_fig = plot_histogram(min_diam_ratio_list, 'Min diameter Ratio %', 'Number of Megakaryocytes')
    pdf.savefig(min_diam_ratio_fig)

    circularity_fig = plot_histogram(circularity_list, 'MK circularity µm', 'Number of Megakaryocytes')
    pdf.savefig(circularity_fig)
    nuc_circ_fig = plot_histogram(nuc_circ_list, 'Nuclei mean circularity µm', 'Number of Nuclei')
    pdf.savefig(nuc_circ_fig)
    circ_ratio_fig = plot_histogram(circ_ratio_list, 'Circularity Ratio %', 'Number of Megakaryocytes')
    pdf.savefig(circ_ratio_fig)

    min_hema_fig = plot_histogram(min_hema_list, 'Hematoxylin: Min', 'Number of Nuclei')
    pdf.savefig(min_hema_fig)
    max_hema_fig = plot_histogram(max_hema_list, 'Hematoxylin: Max', 'Number of Nuclei')
    pdf.savefig(max_hema_fig)
    mean_hema_fig = plot_histogram(mean_hema_list, 'Hematoxylin: Mean', 'Number of Nuclei')
    pdf.savefig(mean_hema_fig)
    std_hema_fig = plot_histogram(std_hema_list, 'Hematoxylin: Std.Dev.', 'Number of Nuclei')
    pdf.savefig(std_hema_fig)

tables_pdf = "Tables.pdf"
tables = []

number_table = create_table('Number of megakaryocytes', 'Number of nuclei', len(name_list), sum(num_nuclei_list))
tables.append(number_table)

mean_area_table = create_table('MK mean area', 'Nuclei mean area', f"{round(np.mean(area_list), 2)} (µm^2)", f"{round(np.mean(nuc_area_list), 2)} (µm^2)")
tables.append(mean_area_table)
std_area_table = create_table('MK area std', 'Nuclei area std', f"{round(np.std(area_list), 2)} (µm^2)", f"{round(np.std(nuc_area_list), 2)} (µm^2)")
tables.append(std_area_table)

mean_max_diam_table = create_table('MK mean max diameter', 'Nuclei mean max diameter', f"{round(np.mean(max_diameter_list), 2)} (µm)", f"{round(np.mean(nuc_max_diam_list), 2)}")
tables.append(mean_max_diam_table)
std_max_diam_table = create_table('MK max diameter std', 'Nuclei max diameter std', f"{round(np.std(max_diameter_list), 2)} (µm)", f"{round(np.std(nuc_max_diam_list), 2)}")
tables.append(std_max_diam_table)

mean_min_diam_table = create_table('MK mean min diameter', 'Nuclei mean min diameter', f"{round(np.mean(min_diameter_list), 2)} (µm)", f"{round(np.mean(nuc_min_diam_list), 2)} (µm)")
tables.append(mean_min_diam_table)
std_min_diam_table = create_table('MK min diameter std', 'Nuclei min diameter std', f"{round(np.std(min_diameter_list), 2)} (µm)", f"{round(np.std(nuc_min_diam_list), 2)} (µm)")
tables.append(std_min_diam_table)

mean_circularity_table = create_table('MK mean circularity', 'Nuclei mean circularity', f"{round(np.mean(circularity_list), 2)} (µm)", f"{round(np.mean(nuc_circ_list), 2)} (µm)")
tables.append(mean_circularity_table)
std_circularity_table = create_table('MK circularity std', 'Nuclei circularity std', f"{round(np.std(circularity_list), 2)} (µm)", f"{round(np.std(nuc_circ_list), 2)} (µm)")
tables.append(std_circularity_table)

mean_hema_table = create_table('Nuclei mean hematoxylin', 'Nuclei hematoxylin std', f"{round(np.mean(mean_hema_list), 2)}", f"{round(np.mean(std_hema_list), 2)}")
tables.append(mean_hema_table)

# Create the PDF with multiple tables
create_pdf_with_tables(tables_pdf, tables)


# Merge graph pdf and table pdf
output_path = '/Users/lilly-flore/Desktop/MK_statistics.pdf'
merge_pdfs(tables_pdf, graphs_pdf, output_path)
print("The pdf has been saved under " + output_path)