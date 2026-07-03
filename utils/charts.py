import plotly.express as px


def magnitude_histogram(df):
    fig = px.histogram(
        df,
        x="Magnitude",
        nbins=20,
        color="Magnitude",
        title="Magnitude Distribution"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    return fig


def depth_boxplot(df):
    fig = px.box(
        df,
        y="Depth (km)",
        title="Depth Distribution"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    return fig


def magnitude_timeline(df):
    fig = px.scatter(
        df,
        x="Time",
        y="Magnitude",
        size="Magnitude",
        hover_name="Place",
        color="Magnitude",
        title="Earthquake Timeline"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500
    )

    return fig


def top_locations(df):

    top = (
        df["Place"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top.columns = ["Location", "Count"]

    fig = px.bar(
        top,
        x="Location",
        y="Count",
        color="Count",
        title="Top 10 Earthquake Locations"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500
    )

    return fig


def risk_pie(df):

    risk = (
        df["Risk"]
        .value_counts()
        .reset_index()
    )

    risk.columns = ["Risk", "Count"]

    fig = px.pie(
        risk,
        names="Risk",
        values="Count",
        hole=0.5,
        title="Risk Distribution"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500
    )

    return fig