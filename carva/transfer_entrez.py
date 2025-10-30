import pandas as pd
import sys

rename_mapping = {'Entrez': 'Entrez_old','Gene Symbol': 'Entrez', "MAPPED_GENE": "Entrez"}

trait = sys.argv[1]
print(f"working on: {trait}")
path = f"../data/{trait}_"
if len(sys.argv)<4:
    sys.argv.append(None)

if sys.argv[2] == "cv" or sys.argv[3] == "cv":
    df_cv = pd.read_csv(path + "cv.txt", sep="\t")
    df_cv2 = df_cv.rename(columns=rename_mapping)
    df_cv2.to_csv(path + "cv2.txt",sep="\t",index=False)

if sys.argv[2] == "rv" or sys.argv[3] == "rv":
    df_rv = pd.read_csv(path + "rv.txt", sep="\t")
    df_rv2 = df_rv.rename(columns=rename_mapping)
    df_rv2.to_csv(path + "rv2.txt",sep="\t",index=False)