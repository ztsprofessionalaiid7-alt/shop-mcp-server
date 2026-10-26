import pandas as pd
from huggingface_hub import hf_hub_download

path = hf_hub_download(
    repo_id="millat/e-commerce-orders",
    filename="ecommerce_orders_clean.csv",
    repo_type="dataset",
    local_dir="data",
)
df = pd.read_csv(path)

print("file   :", path)
print("shape  :", df.shape)
print("columns:", list(df.columns))
print(df.head(3).to_string())
