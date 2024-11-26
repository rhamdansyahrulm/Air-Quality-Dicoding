import pandas as pd
import altair as alt


def donut_chart(data, city, pollutant):
    color_pallete = {
      "Excellent" : "#0af531",
      "Good" : "#63ff7d",
      "Lightly Polluted" : "#bcf514",
      "Moderately Polluted" : "#d4fa64",
      "Heavily Polluted" : "#fc8260",
      "Severely Polluted" : "#f53d0a" 
  }

    value, class_val = data.loc[data["station"] == city, [pollutant, f"class_{pollutant}"]].iloc[-1]
    df = pd.DataFrame({
        "category": ["index", "Total"],
        "value": [value, 600 - value]
    })

    # Create the donut chart
    donut_chart = alt.Chart(df).mark_arc(innerRadius=60, outerRadius=90).encode(
        theta=alt.Theta(field="value", type="quantitative"),
        color=alt.Color(field="category", type="nominal", scale=alt.Scale(
            domain=['index', 'Total'],
            range=[color_pallete[class_val], '#E0E0E0']
        )),
        tooltip=[alt.Tooltip("category:N"), alt.Tooltip("value:Q")]
    ).properties(
        width=200,
        height=200
    )

    center_text = alt.Chart(pd.DataFrame({"text": [class_val]})).mark_text(
        fontSize=14, fontWeight="bold", color=color_pallete[class_val], align="center"
    ).encode(
        text="text:N"
    ).properties(
        width=200,
        height=200
    )


    # Combine the charts
    final_chart = (donut_chart + center_text).configure_legend(disable=True)

    return final_chart