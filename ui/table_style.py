import pandas as pd


def style_table(df):

    df = df.copy()

    # =====================
    # Columnas numéricas conocidas
    # =====================

    numeric_cols = [
        "Interacciones",
        "Impressions",
        "Reach",
        "Views"
    ]

    # =====================
    # Formato miles
    # =====================

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].map(
                lambda x: f"{x:,.0f}" if pd.notnull(x) else ""
            )

    # =====================
    # Formato ER %
    # =====================

    if "ER" in df.columns:
        df["ER"] = pd.to_numeric(df["ER"], errors="coerce")
        df["ER"] = df["ER"].map(
            lambda x: f"{x:.2f}%" if pd.notnull(x) else ""
        )

    styled = df.style

    # =====================
    # Alineación derecha métricas
    # =====================

    right_align = [c for c in numeric_cols if c in df.columns]

    if right_align:
        styled = styled.set_properties(
            subset=right_align,
            **{"text-align": "right"}
        )

    # =====================
    # Centrado Posts y ER
    # =====================

    center_cols = [c for c in ["Posts", "ER"] if c in df.columns]

    if center_cols:
        styled = styled.set_properties(
            subset=center_cols,
            **{"text-align": "center"}
        )

    return styled
