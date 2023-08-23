import src.hemnet_requests as hemreq
import src.hemnet_url_builder as hemurl

import pandas as pd



df = pd.DataFrame()

urls = hemurl.urls

# Loop to call the function and add values
for i in range(6):  # Replace 10 with the desired number of iterations
    extracted_values = hemreq.extract_values_from_html(hemreq.load_html(urls[i]))
    for ele in extracted_values : print(ele, end='\n')
    df = pd.concat([df, pd.DataFrame(extracted_values)])

# Print the final DataFrame
print(df)
