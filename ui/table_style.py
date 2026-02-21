import pandas as pd

def style_table(df):

    numeric_cols = [
        "Interacciones",
        "Impressions",
        "Reach",
        "Views"
    ]

    # Formato miles
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].map(lambda x: f"{x:,.0f}")

    if "ER" in df.columns:
        df["ER"] = df["ER"].map(lambda x: f"{x:.2f}%")

    # Styling
    styled = (
        df.style
        .set_properties(subset=numeric_cols, **{
            "text-align": "right"
        })
        .set_properties(subset=["Posts", "ER"], **{
            "text-align": "center"
        })
    )

    return styled