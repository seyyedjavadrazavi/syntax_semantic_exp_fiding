import pandas as pd
import xml.etree.ElementTree as et

df_cols = ["Id", "PostId", "Score", "Text", "CreationDate", "UserId", "ContentLicense"]

root = et.parse("../../data/bioinformatics/Posts.xml")
rows= root.findall('.//row')

xml_data = [[row.get("Id"), row.get("PostId"), row.get("Score"), row.get("Text"), row.get("CreationDate"),
 row.get("UserId"), row.get("ContentLicense")] for row in rows]

xml_df = pd.DataFrame(xml_data, columns=df_cols)

xml_df.to_csv(r"../../data/bioinformatics/bioinformatics_Comments.csv", index = False, header=True)
