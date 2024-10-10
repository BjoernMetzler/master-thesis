import pandas as pd

def csv_to_specific_latex(csv_file, tex_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file, sep=';')
    
    # Start writing the LaTeX table
    with open(tex_file, 'w') as f:
        f.write('% \\pgfplotstableread[col sep=semicolon]{analysis_relevant_instances.csv}\\datatable\n\n')
        f.write('\\begin{table}[h!]\n')
        f.write('\\caption{Running times (in seconds) and number of nodes of \\textsc{Enum\\_Approach} and \\textsc{SL\\_sos}. The time limit was set to $10800$ seconds (or $3$ hours). Here, the "faster" instances are used.}\n')
        f.write('\\centering\n')
        f.write('\\label{table:fastInstances_nodes_and_time}\n')
        f.write('\\begin{adjustbox}{max width=\\textwidth}\n')
        f.write('\\small\n')
        f.write('\\begin{tabular}{|c|cc|cc|cc|cc|cc|cc|}\n')
        f.write('\\hline\n')
        f.write('Algorithm & \\multicolumn{2}{|c|}{K = 0} & \\multicolumn{2}{|c|}{K = 1} & \\multicolumn{2}{|c|}{K = 2} & \\multicolumn{2}{|c|}{K = 3} & \\multicolumn{2}{|c|}{K = 4} & \\multicolumn{2}{|c|}{K = 5} \\\\\n')
        f.write(' & Time & \\#Nodes & Time & \\#Nodes & Time & \\#Nodes & Time & \\#Nodes & Time & \\#Nodes & Time & \\#Nodes \\\\\n')
        f.write('\\hline\n')
        
        # Iterate over the DataFrame to add rows
        for instance in df['instance'].unique():
            f.write(f'\\multicolumn{13}|c|{{{instance}}} \\\\\n')
            f.write('\\hline\n')
            instance_data = df[df['instance'] == instance]
            for _, row in instance_data.iterrows():
                f.write(f"{row['algorithm']} & {row['K=0_time']} & {row['K=0_nodes']} & {row['K=1_time']} & {row['K=1_nodes']} & {row['K=2_time']} & {row['K=2_nodes']} & {row['K=3_time']} & {row['K=3_nodes']} & {row['K=4_time']} & {row['K=4_nodes']} & {row['K=5_time']} & {row['K=5_nodes']} \\\\\n")
            f.write('\\hline\n')
        
        f.write('\\end{tabular}\n')
        f.write('\\end{adjustbox}\n')
        f.write('\\end{table}\n')

# Example usage
csv_to_specific_latex('analysis_relevant_instances.csv', 'formatted_table.tex')
