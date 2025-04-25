"""
Utilities for printing portfolio cards.
"""

import yaml
import pandas as pd

# import sys
# sys.path.append("src/python")
# from cards import sync_projects
# from src.python.cards import sync_projects


def sync_projects(
  src_path: str,
  targ_path: str,
  src_cols: list,
  targ_cols: list,
  join_key: str = "title",
  how: str = "outer"
) -> None:
  """
  Retrieve records from a spreadsheet and use to update portfolio card data.
  """
  df_src = pd.read_csv(src_path)
  with open(targ_path) as f:
    df_targ = pd.DataFrame(yaml.safe_load(f))
  
  df_merged = pd.merge(
    df_src,
    df_targ[targ_cols],
    on=join_key,
    how=how
  )[[*targ_cols, *src_cols]]
  
  df_merged["in_portfolio"] = df_merged["in_portfolio"].fillna(True)
  df_merged["tools"] = df_merged["tools"].astype(str)
  df_merged["link"] = df_merged["link"].astype(str)
  df_merged["link_text"] = df_merged["link_text"].astype(str)

  with open(targ_path, "w") as f:
    yaml.dump(
      df_merged.to_dict(orient="records"),
      f,
      sort_keys=False,
      allow_unicode=True,
      default_flow_style=False
    )


def format_projects(
  df: pd.DataFrame,
  default_img: str,
  default_img_alt: str
) -> pd.DataFrame: 
  """
  Prepare project data for printing in portfolio cards.
  """
  # Replace missing values
  df["text"] = (
    df["text"]
    .fillna(df["short_summary"])
    .apply(lambda x: "I " + x[:1].lower() + x[1:] + ".")
  )
  df["img"] = df["img"].fillna(default_img)
  df["img_alt"] = df["img_alt"].fillna(default_img_alt)
  
  # Filter and drop unneeded fields
  df = (
    df[df['in_portfolio']]
    .drop(['title', 'in_portfolio', 'short_summary'], axis=1)
  )
  return df
