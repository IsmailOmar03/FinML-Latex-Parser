#make necessary imports to handle data
import sys

import pandas as pd
import numpy as np

def print_csv(df, var):
    #array of p-levels
    sig_lvls = [0.5, 2.5, 5]
    f.write(' & ')
    s_count = 0
    for j in range(len(sig_lvls)):
        if (df.iloc[i][f'{sig_lvls[j]}_percentile_{var}'] * df.iloc[i][f'{100 - sig_lvls[j]}_percentile_{var}']) > 0:
            s_count = 3 - j
            break
    f.write(f' ${df.iloc[i][f"lambda_{var}"]:.2e}^' + '{' + f'{"*" * s_count}' + '}$ ')
    f.write(f' & ({df.iloc[i][f"st_error_{var}"]:.2e}) ')

#main function
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Provide command line args. First one for Two-pass csv, second for Five-step")
        exit()
    #read in data from csv file into dataframe
    df_tp = pd.read_csv(sys.argv[1])
    df_fs = pd.read_csv(sys.argv[2])
    #header for the tex file
    doc_header = r"""\begin{document}
\begin{tabular}{lcccccccc}
\toprule
\multirow{2}{*}{Factor} & \multicolumn{4}{c}{Two-pass (FF5)} & \multicolumn{4}{c}{Five-step (5PCs)} \\
\cmidrule(lr){2-5}  \cmidrule(lr){6-9}
 & $\lambda_C$ & SE & $\lambda_J$ & SE & $\lambda_C$ & SE & $\lambda_J$ & SE \\
\midrule
"""
    #footer for the tex file
    doc_footer = r"""\bottomrule
\end{tabular}
\end{document}"""

    #open file buffer in order to write output
    f=open("./table.tex", "w")

    f.write(doc_header)

    for i in range(df_tp.shape[0]):
        f.write(df_tp.iloc[i]["factor"].replace('_','\_'))
        print_csv(df_tp, "cont")
        print_csv(df_tp, "jump")
        print_csv(df_fs, "cont")
        print_csv(df_fs, "jump")
        f.write(r" \\")
        f.write("\n")

    f.write(doc_footer)

    f.close()
