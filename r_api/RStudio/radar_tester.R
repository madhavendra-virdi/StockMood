library(plotly)
library(grDevices)

# Example sentiment score
overall_sentiment_score <- 0.8  # Try with -0.5, 0, 1, etc.

# Define color gradients
red_to_yellow <- colorRampPalette(c("red", "yellow"))(50)
yellow_to_darkgreen <- colorRampPalette(c("yellow", "#006400"))(50)

# Define color steps from -1 to 1
steps <- list()
for (i in 1:50) {
  steps[[i]] <- list(
    range = c(-1 + (i - 1) * (1 / 50), -1 + i * (1 / 50)),
    color = red_to_yellow[i]
  )
}
for (i in 1:50) {
  steps[[50 + i]] <- list(
    range = c(0 + (i - 1) * (1 / 50), 0 + i * (1 / 50)),
    color = yellow_to_darkgreen[i]
  )
}

# Convert sentiment score to angle
angle_deg <- 180 * (1 - (overall_sentiment_score + 1) / 2)
angle_rad <- angle_deg * pi / 180

# Needle base and tip in paper coordinates
center_x <- 0.5
center_y <- 0.5  # Shifted up from 0 to align with visible semicircle
needle_length <- 0.4  # Adjust to fit nicely in the semicircle

needle_x <- center_x + needle_length * cos(angle_rad)
needle_y <- center_y + needle_length * sin(angle_rad)

# Create gauge chart
fig <- plot_ly(
  type = "indicator",
  mode = "gauge+number",
  value = overall_sentiment_score,
  gauge = list(
    shape = "angular",
    axis = list(range = list(-1, 1), tickwidth = 2, tickcolor = "black", showticklabels = FALSE),
    bar = list(color = "rgba(0,0,0,0)", thickness = 0),
    steps = steps
  ),
  domain = list(x = c(0, 1), y = c(0, 1))
) %>% layout(
  margin = list(l = 20, r = 30, t = 60, b = 0),
  height = 400,
  shapes = list(
    list( # Needle line
      type = "line",
      x0 = center_x,
      y0 = center_y,
      x1 = needle_x,
      y1 = needle_y,
      line = list(color = "black", width = 4),
      xref = "paper",
      yref = "paper"
    ),
    list( # Needle center dot
      type = "circle",
      x0 = center_x - 0.015,
      y0 = center_y - 0.015,
      x1 = center_x + 0.015,
      y1 = center_y + 0.015,
      fillcolor = "black",
      line = list(color = "black"),
      xref = "paper",
      yref = "paper"
    )
  )
)

fig
