def format_table(df):

    numeric_cols = [
        "Posts",
        "Interacciones",
        "Impressions",
        "Reach",
        "Views"
    ]

    styled = df.style

    # Separador de miles
    for col in numeric_cols:
        if col in df.columns:
            styled = styled.format({col: "{:,.0f}"})

    # ER %
    if "ER" in df.columns:
        styled = styled.format({"ER": "{:.2%}"})

    # Alineaciones
    styled = styled.set_properties(
        subset=numeric_cols,
        **{"text-align": "right"}
    )

    if "ER" in df.columns:
        styled = styled.set_properties(
            subset=["ER"],
            **{"text-align": "center"}
        )

    return styled
