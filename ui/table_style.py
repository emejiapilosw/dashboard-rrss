import pandas as pd

def style_table(df: pd.DataFrame):

    df_copy = df.copy()

    numeric_cols = df_copy.select_dtypes(include=["int64", "float64"]).columns

    for col in numeric_cols:
        if "ER" in col:
            df_copy[col] = df_copy[col].map(lambda x: f"{x:.2f}%")
        else:
            df_copy[col] = df_copy[col].map(lambda x: f"{x:,.0f}")

    styled = (
        df_copy.style
        .set_properties(**{
            "background-color": "#0f172a",
            "color": "#f8fafc",
            "border": "1px solid #1e293b",
            "font-size": "14px"
        })
        .set_table_styles([
            {
                "selector": "th",
                "props": [
                    ("background-color", "#1e293b"),
                    ("color", "#38bdf8"),
                    ("font-weight", "600"),
                    ("border", "1px solid #1e293b")
                ]
            }
        ])
    )

    return styled
