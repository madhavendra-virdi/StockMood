library(shiny)
library(ggplot2)
library(plotly) # For interactive tooltips

# Define UI
ui <- fluidPage(
  plotlyOutput("debtChart") # Use Plotly for interactive tooltips
)

# Define Server
server <- function(input, output) {
  output$debtChart <- renderPlotly({
    # Define bar colors
    bar_colors <- ifelse(data$Company == "Panacea Biotec Limited", "#a9c0e8", "#f3f3f3")
    
    # Create the ggplot
    p <- ggplot(data, aes(x = Company, y = Debt_Percentage, text = paste("Company:", Company, 
                                                                         "<br>Debt %:", Debt_Percentage))) +
      geom_bar(stat = "identity", fill = bar_colors, show.legend = FALSE) +
      geom_hline(yintercept = mean(data$Debt_Percentage), linetype = "dashed", color = "#6e9fcf", size = 1) +
      labs(
        title = NULL,
        x = NULL,
        y = NULL
      ) +
      theme_minimal() +
      theme(
        axis.text.x = element_blank(), # Remove x-axis text
        axis.ticks.x = element_blank(), # Remove x-axis ticks
        panel.grid.major.x = element_blank() # Remove gridlines for x-axis
      )
    
    # Convert ggplot to Plotly for interactivity
    ggplotly(p, tooltip = "text")
  })
  
  # Example data
  data <- data.frame(
    Company = c("Biocon Limited", "Panacea Biotec Limited", "Hester Biosciences Limited", 
                "Zenotech Laboratories Limited", "Nirman Agri Genetics Limited", 
                'Bharat Immunologicals (BIBCOL)', 'Transgene Biotek Limited', 
                'Hindustan Bio Sciences Limited'),
    Debt_Percentage = c(43, 10, 51, 2.3, 1.7, 49, 92, 76)
  )
  data$Average <- mean(data$Debt_Percentage)
  
  data$Company <- factor(data$Company, levels = data$Company[order(data$Debt_Percentage)])
}

# Run the app
shinyApp(ui = ui, server = server)
