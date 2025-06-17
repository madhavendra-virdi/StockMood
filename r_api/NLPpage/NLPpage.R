library(networkD3)
library(dplyr)
library(readr)
library(shiny)
library(plotly)

# Define UI
ui <- fixedPage(
  fixedRow(
    width = 12,
    sankeyNetworkOutput("sankey")
  ),
  fixedRow(
    column(
      width = 5,
      plotlyOutput("linePlot")
    ),
    column(
      width = 7,
      div(
        tags$img(
          src = "sentiment.jpg", 
          style = "position: relative; left: 20px; top: 10px; width: 100%;"
        )
      )
    )
  )
)

# Define Server
server <- function(input, output) {
  data <- data.frame(
    Month = seq(as.Date("2024-08-01"), by = "month", length.out = 6),
    StockPrice = c(190, 250, 300, 500, 475, 447),
    SocialMentions = c(80, 85, 290, 150, 140, 50)
  )
  
  output$linePlot <- renderPlotly({
    plot_ly() %>%
      # Add the Stock Price line
      add_lines(
        x = ~data$Month,
        y = ~data$StockPrice,
        name = "Stock Price",
        line = list(color = "#a9c0e8", width = 2),
        yaxis = "y1"
      ) %>%
      # Add the Posts Count line
      add_lines(
        x = ~data$Month,
        y = ~data$SocialMentions,
        name = "Posts Count",
        line = list(color = "red", width = 2, dash = "dash"),
        yaxis = "y2"
      ) %>%
      # Configure the layout for dual y-axes
      layout(
        xaxis = list(
          title = "" # Removes the x-axis label
        ),
        yaxis = list(
          title = "Stock Price",
          titlefont = list(color = "#a9c0e8"),
          tickfont = list(color = "#a9c0e8")
        ),
        yaxis2 = list(
          title = "Posts Count",
          overlaying = "y",
          side = "right",
          titlefont = list(color = "red"),
          tickfont = list(color = "red"),
          standoff = 15 # Adds space between title and numbers
        ),
        showlegend = FALSE # Remove legend
      )
  })
  
  
  
  
  data_san <- read_csv("sankeytwo.csv") %>%
    mutate(
      IDsource = match(source, unique(c(source, target))) - 1,
      IDtarget = match(target, unique(c(source, target))) - 1
    )
  
  nodes <- data.frame(name = unique(c(data_san$source, data_san$target)))
  
  ColourScal <- 'd3.scaleOrdinal().range(["#f7fcfd", "#e0ecf4", "#bfd3e6", "#9ebcda", "#8c96c6", "#8c6bb1", "#88419d", "#810f7c", "#4d004b", "#000000"])'
  
  output$sankey <- renderSankeyNetwork({
    sankeyNetwork(
      Links = data_san, Nodes = nodes,
      Source = "IDsource", Target = "IDtarget",
      Value = "value", NodeID = "name",
      sinksRight = FALSE, colourScale = JS(ColourScal),
      nodeWidth = 40, fontSize = 13, nodePadding = 20
    )
  })
}

# Run App
shinyApp(ui = ui, server = server)
