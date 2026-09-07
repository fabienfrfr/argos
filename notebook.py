import marimo

__generated_with = "0.24.0"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from pathlib import Path

    import numpy as np
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as goS
    from data_profiling import ProfileReport

    from autogluon.tabular import TabularPredictor

    from sklearn.model_selection import GroupShuffleSplit, ShuffleSplit
    from sklearn.metrics import (
        average_precision_score,
        roc_auc_score,
    )

    return (
        GroupShuffleSplit,
        Path,
        ProfileReport,
        ShuffleSplit,
        TabularPredictor,
        average_precision_score,
        np,
        pd,
        px,
        roc_auc_score,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Argos

    ## Auto EDA + AutoML + Time Series

    **Stack**

    - Marimo
    - fg-data-profiling
    - AutoGluon
    - Hampel Filter
    - Plotly

    **Dataset**

    ```text
    data/skab_dataset.csv
    ```
    """)
    return


@app.cell
def _(Path, pd):
    dataset_path = Path("data/skab_dataset.csv")

    if not dataset_path.exists():
        raise FileNotFoundError(f"Missing file: {dataset_path}")

    raw_df = pd.read_csv(
        dataset_path,
        sep=",",
        encoding="utf-8",
    )

    # SKAB typically uses "datetime"
    if "datetime" in raw_df.columns and "timestamp" not in raw_df.columns:
        raw_df = raw_df.rename(columns={"datetime": "timestamp"})

    if "Unnamed: 0" in raw_df.columns:
        raw_df = raw_df.drop(columns=["Unnamed: 0"])

    if "timestamp" in raw_df.columns:
        raw_df["timestamp"] = pd.to_datetime(
            raw_df["timestamp"],
            errors="coerce",
        )

    for column in raw_df.columns:
        if column not in ["timestamp"]:
            raw_df[column] = pd.to_numeric(
                raw_df[column],
                errors="ignore",
            )

    sort_columns = [column for column in ["object_id", "timestamp"] if column in raw_df.columns]

    if sort_columns:
        raw_df = raw_df.sort_values(sort_columns).reset_index(drop=True)
    raw_df
    return (raw_df,)


@app.cell
def _(raw_df):
    target_column = "labels"

    feature_columns = [
        column
        for column in raw_df.columns
        if column
        not in [
            "timestamp",
            "object_id",
            target_column,
        ]
    ]
    feature_columns
    return (feature_columns,)


@app.cell
def _(mo, pd, raw_df):
    dataset_stats = pd.DataFrame(
        {
            "metric": [
                "rows",
                "columns",
                "assets",
                "fault_rows",
                "normal_rows",
                "duplicates",
                "missing_values",
            ],
            "value": [
                len(raw_df),
                len(raw_df.columns),
                (raw_df["object_id"].nunique() if "object_id" in raw_df.columns else 1),
                ((raw_df["labels"] == -1).sum() if "labels" in raw_df.columns else 0),
                ((raw_df["labels"] == 1).sum() if "labels" in raw_df.columns else 0),
                raw_df.duplicated().sum(),
                raw_df.isna().sum().sum(),
            ],
        }
    )

    mo.ui.table(dataset_stats)
    return


@app.cell
def _(ProfileReport, raw_df):
    profile_report = ProfileReport(
        raw_df,
        minimal=True,
        explorative=True,
        progress_bar=False,
    )

    profile_description = profile_report.get_description()
    return (profile_description,)


@app.cell
def _(pd, profile_description):
    profile_variables = pd.DataFrame(profile_description.variables).T.reset_index().rename(columns={"index": "feature"})
    profile_variables
    return (profile_variables,)


@app.cell
def _(mo, profile_variables):
    if not profile_variables.empty:
        mo.ui.table(profile_variables)
    return


@app.cell
def _(pd, profile_description):
    profile_alerts = pd.DataFrame({"alert": [str(alert) for alert in profile_description.alerts]})
    return (profile_alerts,)


@app.cell
def _(mo, profile_alerts):
    if not profile_alerts.empty:
        mo.ui.table(profile_alerts)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Dataset Overview
    """)
    return


@app.cell
def _(feature_columns, mo):
    feature_selector = mo.ui.dropdown(
        options=feature_columns,
        value=feature_columns[0] if feature_columns else None,
        label="Feature",
    )
    return (feature_selector,)


@app.cell
def _(feature_selector, px, raw_df):
    selected_feature_histogram = feature_selector.value

    histogram_fig = px.histogram(
        raw_df,
        x=selected_feature_histogram,
        color="labels" if "labels" in raw_df.columns else None,
        marginal="box",
        title=f"Distribution - {selected_feature_histogram}",
    )
    return (histogram_fig,)


@app.cell
def _(histogram_fig):
    histogram_fig
    return


@app.cell
def _(feature_selector, px, raw_df):
    selected_feature_violin = feature_selector.value

    violin_fig = px.violin(
        raw_df,
        x="labels" if "labels" in raw_df.columns else None,
        y=selected_feature_violin,
        color="labels" if "labels" in raw_df.columns else None,
        box=True,
        title=f"Violin Plot - {selected_feature_violin}",
    )
    return (violin_fig,)


@app.cell
def _(violin_fig):
    violin_fig
    return


@app.cell
def _(feature_columns, px, raw_df):
    correlation_matrix = raw_df[feature_columns].corr()

    correlation_fig = px.imshow(
        correlation_matrix,
        text_auto=".2f",
        aspect="auto",
        title="Correlation Matrix",
    )
    correlation_matrix
    return correlation_fig, correlation_matrix


@app.cell
def _(correlation_matrix):
    top_correlations = (
        correlation_matrix.stack()
        .reset_index()
        .rename(
            columns={
                "level_0": "feature_1",
                "level_1": "feature_2",
                0: "correlation",
            }
        )
        .query("feature_1 != feature_2")
        .sort_values(
            "correlation",
            ascending=False,
        )
        .head(20)
    )
    return (top_correlations,)


@app.cell
def _(mo, top_correlations):
    mo.ui.table(top_correlations)
    return


@app.cell
def _(correlation_fig):
    correlation_fig
    return


@app.cell
def _(mo, raw_df):
    if "object_id" in raw_df.columns:
        asset_options = sorted(raw_df["object_id"].dropna().unique().tolist())
    else:
        asset_options = [0]

    asset_selector = mo.ui.dropdown(
        options=asset_options,
        value=asset_options[0],
        label="Asset",
    )
    return (asset_selector,)


@app.cell
def _(asset_selector, feature_selector, px, raw_df):
    selected_asset = asset_selector.value
    selected_feature_timeseries = feature_selector.value

    if "object_id" in raw_df.columns:
        asset_subset = raw_df.loc[raw_df["object_id"] == selected_asset].copy()
    else:
        asset_subset = raw_df.copy()

    asset_signal_fig = px.line(
        asset_subset,
        x=("timestamp" if "timestamp" in asset_subset.columns else asset_subset.index),
        y=selected_feature_timeseries,
        color=("labels" if "labels" in asset_subset.columns else None),
        title=(f"Asset {selected_asset} - {selected_feature_timeseries}"),
        render_mode="svg",
    )
    return (asset_signal_fig,)


@app.cell
def _(asset_signal_fig):
    asset_signal_fig
    return


@app.cell
def _(feature_columns, raw_df):
    engineered_df = raw_df.copy()

    rolling_window = 30

    group_column = "object_id" if "object_id" in engineered_df.columns else None

    for feature_name in feature_columns:
        delta_column = f"{feature_name}_delta_1"
        mean_column = f"{feature_name}_mean_30"
        std_column = f"{feature_name}_std_30"

        if group_column:
            engineered_df[delta_column] = engineered_df.groupby(group_column)[feature_name].diff()

            engineered_df[mean_column] = engineered_df.groupby(group_column)[feature_name].transform(
                lambda series: series.rolling(
                    rolling_window,
                    min_periods=rolling_window,
                ).mean()
            )

            engineered_df[std_column] = engineered_df.groupby(group_column)[feature_name].transform(
                lambda series: series.rolling(
                    rolling_window,
                    min_periods=rolling_window,
                ).std()
            )

        else:
            engineered_df[delta_column] = engineered_df[feature_name].diff()

            engineered_df[mean_column] = (
                engineered_df[feature_name]
                .rolling(
                    rolling_window,
                    min_periods=rolling_window,
                )
                .mean()
            )

            engineered_df[std_column] = (
                engineered_df[feature_name]
                .rolling(
                    rolling_window,
                    min_periods=rolling_window,
                )
                .std()
            )

    if "labels" in engineered_df.columns:
        engineered_df["failure"] = (engineered_df["labels"] == -1).astype(int)

    engineered_df = engineered_df.dropna().reset_index(drop=True)
    return (engineered_df,)


@app.cell
def _(GroupShuffleSplit, ShuffleSplit, engineered_df):
    if "object_id" in engineered_df.columns:
        group_splitter = GroupShuffleSplit(
            n_splits=1,
            test_size=0.30,
            random_state=42,
        )

        train_indices, test_indices = next(
            group_splitter.split(
                engineered_df,
                groups=engineered_df["object_id"],
            )
        )
    else:
        group_splitter = ShuffleSplit(
            n_splits=1,
            test_size=0.30,
            random_state=42,
        )

        train_indices, test_indices = next(group_splitter.split(engineered_df))

    train_df = engineered_df.iloc[train_indices].copy()
    test_df = engineered_df.iloc[test_indices].copy()
    return test_df, train_df


@app.cell
def _(test_df, train_df):
    # IMPORTANT:
    # - labels is the original target
    # - failure is the ML target
    # Therefore labels must NOT be given to AutoGluon.
    #
    # object_id is also removed because the split is already
    # performed by group.

    automl_drop_columns = [
        "failure",
        "labels",
        "timestamp",
        "object_id",
    ]

    automl_feature_columns = [column for column in train_df.columns if column not in automl_drop_columns]

    automl_train_df = train_df[automl_feature_columns + ["failure"]].copy()

    automl_test_df = test_df[automl_feature_columns + ["failure"]].copy()
    return automl_test_df, automl_train_df


@app.cell
def _(TabularPredictor, automl_train_df):
    automl_predictor = None

    if "failure" in automl_train_df.columns:
        automl_predictor = TabularPredictor(
            label="failure",
            eval_metric="average_precision",
            verbosity=2,
        ).fit(
            automl_train_df,
            presets="best_quality",
            time_limit=60,
        )
    return (automl_predictor,)


@app.cell
def _(automl_predictor):
    automl_leaderboard = None

    if automl_predictor is not None:
        automl_leaderboard = automl_predictor.leaderboard(silent=True)
    return (automl_leaderboard,)


@app.cell
def _(automl_leaderboard, px):
    automl_leaderboard_fig = None

    if automl_leaderboard is not None:
        automl_leaderboard_fig = px.bar(
            automl_leaderboard.head(20),
            x="model",
            y="score_val",
            title="AutoML Leaderboard",
        )
    return (automl_leaderboard_fig,)


@app.cell
def _(automl_leaderboard_fig):
    if automl_leaderboard_fig is not None:
        automl_leaderboard_fig
    return


@app.cell
def _(automl_predictor, automl_test_df):
    automl_feature_importance = None

    if automl_predictor is not None:
        automl_feature_importance = automl_predictor.feature_importance(automl_test_df)
    return (automl_feature_importance,)


@app.cell
def _(automl_feature_importance, px):
    feature_importance_fig = None

    if automl_feature_importance is not None:
        importance_plot_df = automl_feature_importance.head(25).reset_index()

        # AutoGluon usually returns the feature name
        # as the index. Handle both possible names.
        feature_name_column = "index" if "index" in importance_plot_df.columns else importance_plot_df.columns[0]

        feature_importance_fig = px.bar(
            importance_plot_df,
            x="importance",
            y=feature_name_column,
            orientation="h",
            title="Feature Importance",
        )
    return (feature_importance_fig,)


@app.cell
def _(feature_importance_fig):
    if feature_importance_fig is not None:
        feature_importance_fig
    return


@app.cell
def _(
    automl_predictor,
    automl_test_df,
    average_precision_score,
    np,
    pd,
    roc_auc_score,
):
    evaluation_metrics = None
    prediction_scores = None

    if automl_predictor is not None:
        evaluation_features = automl_test_df.drop(columns=["failure"])

        evaluation_target = automl_test_df["failure"]

        prediction_probabilities = automl_predictor.predict_proba(evaluation_features)

        if 1 in prediction_probabilities.columns:
            prediction_scores = prediction_probabilities[1]
        else:
            prediction_scores = prediction_probabilities.iloc[:, -1]

        metric_values = {
            "average_precision": np.nan,
            "roc_auc": np.nan,
        }

        # Metrics requiring both classes
        if evaluation_target.nunique() >= 2:
            metric_values["average_precision"] = average_precision_score(
                evaluation_target,
                prediction_scores,
            )

            metric_values["roc_auc"] = roc_auc_score(
                evaluation_target,
                prediction_scores,
            )

        evaluation_metrics = pd.DataFrame(
            {
                "metric": list(metric_values.keys()),
                "value": list(metric_values.values()),
            }
        )
    return (evaluation_metrics,)


@app.cell
def _(evaluation_metrics, mo):
    if evaluation_metrics is not None:
        mo.ui.table(evaluation_metrics)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Anomaly Detection — Hampel Filter
    """)
    return


@app.cell
def _(asset_selector, feature_selector, np, raw_df):
    hampel_feature = feature_selector.value
    hampel_asset = asset_selector.value

    if "object_id" in raw_df.columns:
        hampel_signal = raw_df.loc[
            raw_df["object_id"] == hampel_asset,
            hampel_feature,
        ].reset_index(drop=True)
    else:
        hampel_signal = raw_df[hampel_feature].reset_index(drop=True)

    def hampel_filter(
        series,
        window_size=15,
        n_sigma=3,
    ):
        rolling_median = series.rolling(
            window=window_size,
            min_periods=1,
            center=True,
        ).median()

        absolute_deviation = (series - rolling_median).abs()

        rolling_mad = absolute_deviation.rolling(
            window=window_size,
            min_periods=1,
            center=True,
        ).median()

        threshold = n_sigma * 1.4826 * rolling_mad

        difference = (series - rolling_median).abs()

        # Avoid treating zero-MAD regions as anomalies
        valid_threshold = threshold > 0

        anomaly_mask = (difference > threshold) & valid_threshold

        return anomaly_mask

    hampel_anomaly_mask = hampel_filter(hampel_signal)

    hampel_anomaly_indices = np.flatnonzero(hampel_anomaly_mask)
    return hampel_anomaly_indices, hampel_feature, hampel_signal


@app.cell
def _(go, hampel_anomaly_indices, hampel_feature, hampel_signal, np):
    hampel_fig = go.Figure()

    hampel_fig.add_trace(
        go.Scatter(
            x=np.arange(len(hampel_signal)),
            y=hampel_signal,
            mode="lines",
            name=hampel_feature,
        )
    )

    if len(hampel_anomaly_indices) > 0:
        hampel_fig.add_trace(
            go.Scatter(
                x=hampel_anomaly_indices,
                y=hampel_signal.iloc[hampel_anomaly_indices],
                mode="markers",
                name="Anomaly",
                marker=dict(
                    color="red",
                    size=8,
                ),
            )
        )

    hampel_fig.update_layout(
        title="Hampel Filter Anomaly Detector",
        xaxis_title="Observation",
        yaxis_title=hampel_feature,
    )
    return (hampel_fig,)


@app.cell
def _(hampel_fig):
    hampel_fig
    return


@app.cell
def _(px, raw_df):
    target_distribution_fig = None

    if "labels" in raw_df.columns:
        target_counts = raw_df["labels"].value_counts().rename_axis("labels").reset_index(name="count")

        target_distribution_fig = px.pie(
            target_counts,
            names="labels",
            values="count",
            title="Target Distribution",
        )
    return (target_distribution_fig,)


@app.cell
def _(target_distribution_fig):
    if target_distribution_fig is not None:
        target_distribution_fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Résultat

    - **EDA automatique** : profiling, qualité des données,
      alertes, duplicats, distributions et corrélations
    - **Feature engineering** : deltas, moyennes et écarts-types
      glissants
    - **AutoML** : AutoGluon, leaderboard et feature importance
    - **Time Series / Anomaly Detection** : Hampel Filter
    - **Split** : GroupShuffleSplit par `object_id`
    - **Visualisation** : Marimo + Plotly
    """)
    return


if __name__ == "__main__":
    app.run()
