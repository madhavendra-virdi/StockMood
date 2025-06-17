library(shiny)
library(DT)
library(ggplot2)

# Sample data
data <- data.frame(
  Column1 = c('PV(Terminal value)','PV (10yr CFs)','Sum of PV',' - Debt',' +  Cash',' + Non-operating assets','Value of equity','Number of shares','Estimated value /share','Price'),
  Column2 = c(93986,50450,144436,9361,4717,75549,215341,608,354,446)
)

# UI
ui <- fixedPage(
  tags$head(
    # Custom CSS for the table styles
    tags$style(HTML("
      body {
        font-family: 'Roboto', Arial, sans-serif;
        margin: 0;
        padding: 0;
        background: #f9f9f9;
        color: #333;
        font-size: 16px;
        line-height: 1.5;
        font-weight: bold;
      }

      /* Container Styles */
      #table-container {
        width: 100%;
        max-width: 1180px;
        max-height: none;
        overflow-y: auto;
        margin-bottom: 50px;
        background: #fff;
        border: 1px solid #ddd;
        border-radius: 16px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      }

      /* Table Styles */
      #data-table {
        width: 100%;
        border-collapse: collapse;
        background: #fff;
        color: #333;
      }

      #data-table th,
      #data-table td {
        border-right: 1px solid #ddd; /* Add a right border for each column */
        padding: 16px;
        text-align: center;
        font-size: 14px;
      }

      /* Remove right border from last column */
      #data-table td:last-child, 
      #data-table th:last-child {
        border-right: none;
      }

      #data-table th {
        background: #f3f3f3;
        color: #333;
        text-transform: uppercase;
        font-weight: bold;
      }

      #data-table tr:nth-child(even) {
        background: #f9f9f9;
      }

      #data-table tr:nth-child(1) {
        background: #a9c0e8; 
        font-weight: bold;
        color: #fff;
        border-top: 2px solid #333;  /* Add a line in the middle of the table */
      }

      #data-table tr:hover {
        background: #e8f0fe;
        cursor: pointer;
        transition: background 0.3s ease-out;
      }

      /* Scrollbar Styling */
      #table-container::-webkit-scrollbar {
        width: 8px;
      }

      #table-container::-webkit-scrollbar-thumb {
        background: #ccc;
        border-radius: 10px;
      }

      #table-container::-webkit-scrollbar-thumb:hover {
        background: #bbb;
      }

      #table-container::-webkit-scrollbar-track {
        background: #f3f3f3;
        border-radius: 10px;
      }

      /* Responsive Design */
      @media screen and (max-width: 1024px) {
        #table-container {
          width: 90%;
        }
      }
    "))
  ),
  
  # Main content
  fixedRow(
    column(6,
           div(id = "table-container",
               DTOutput("data_table")
           )
    ), column(
      width = 6, plotOutput("auc_plot"))
    )
  )

# Server
server <- function(input, output) {
  
  output$auc_plot <- renderPlot({
    # Generate x and y values
    x <- c(0,5,10,20,40,60,80,100)
    y <- c(150,150,200,346,445,700,900,1800)
    
    # Create data frame for plot
    data <- data.frame(x, y)
    
    # Plot the curve using ggplot
    ggplot(data = data, aes(x = x, y = y)) +
      geom_line() +
      geom_ribbon(aes(ymin = 0, ymax = y), fill = "#a9c0e8", alpha = 0.4) +
      # Using geom_point with data argument for highlighting points
      geom_point(data = data.frame(x = 20, y = 346), aes(x = x, y = y), color = "green", size = 3) +  # Highlight point (20, 346)
      geom_point(data = data.frame(x = 40, y = 445), aes(x = x, y = y), color = "red", size = 3) +    # Highlight point (40, 445)
      labs(x = "Growth rates", y = "Price") +
      theme_minimal()
  })
  
  
  
  output$data_table <- renderDT({
    datatable(
      data,
      rownames = FALSE,
      colnames = "",  # Remove column headers
      options = list(
        dom = 't',
        scrollX = TRUE,
        ordering = FALSE  # Disable sorting arrows
      ),
      class = 'display compact',
      escape = FALSE
    ) %>% 
      formatStyle(
        'Column1', target = 'row',
        backgroundColor = styleEqual(2, '#a9c0e8'),
        color = styleEqual(2, 'white')
      )
  })
}

# Run the app
shinyApp(ui = ui, server = server)
