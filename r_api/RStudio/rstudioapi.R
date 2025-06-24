# Load libraries
library(plumber)
library(DBI)
library(RMySQL)
library(plotly)
library(htmlwidgets)
library(htmltools)
library(networkD3)
library(readr)
library(dplyr)
library(wordcloud2)
library(tidytext)
library(stringr)




#* @get /plot1
#* @param stock_name The name of the stock to fetch
#* @serializer html
function(stock_name = "") {
  if (stock_name == "") {
    return(HTML("<h3>Error: No stock name provided.</h3>"))
  }
  
  # Connect to DB
  # Connect to DB
  db <- dbConnect(
    RMySQL::MySQL(),
    dbname = "my_database",
    host = "mysql",
    port = 3306,
    user = "stock_user",
    password = "stock_pass"
  )
  
  # Safe query
  query <- paste0(
    "SELECT * FROM FinancialData WHERE LOWER(Name) = LOWER(", 
    dbQuoteString(db, stock_name), ")"
  )
  
  data <- tryCatch({
    dbGetQuery(db, query)
  }, error = function(e) {
    dbDisconnect(db)
    return(HTML(paste("<h3>Query failed:</h3><p>", e$message, "</p>")))
  })
  
  if (nrow(data) == 0) {
    dbDisconnect(db)
    return(HTML("<h3>No data found for stock.</h3>"))
  }
  
  # Prepare plot
  compare_df <- data.frame(
    Type = c("Actual Price", "Predicted Price"),
    Value = as.numeric(c(data$Price[1], data$share_price[1]))
  )
  
  p <- plot_ly(compare_df, x = ~Type, y = ~Value, type = 'bar', color = ~Type,
               colors = c('#a9c0e8', '#f4f4f4')) %>%
    layout(
      title = list(
        text = paste("Price vs Predicted Share Price for", stock_name),
        x = 0.5,
        xanchor = "center",
        font=list(size=14)
      ),
      yaxis = list(title = "Price"),
      xaxis = list(title = ""),
      margin = list(t = 100)  # <-- This adds top spacing
    )

  
  # Save & return
  tmp_file <- tempfile(fileext = ".html")
  saveWidget(p, tmp_file, selfcontained = TRUE)
  dbDisconnect(db)
  readChar(tmp_file, file.info(tmp_file)$size)
}

###############################################################################################################################

#* @get /plot2
#* @param stock_name The name of the stock to fetch
#* @serializer html
function(stock_name = "") {
  if (stock_name == "") {
    return(HTML("<h3>Error: No stock name provided.</h3>"))
  }
  
  # Connect to DB
   # Connect to DB
  db <- dbConnect(
    RMySQL::MySQL(),
    dbname = "my_database",
    host = "mysql",
    port = 3306,
    user = "stock_user",
    password = "stock_pass"
  )

  
  # Get sub-industry of the given stock
  query <- paste0("SELECT Sub_Industry FROM FinancialData WHERE LOWER(Name) = LOWER(", dbQuoteString(db, stock_name), ")")
  sub_industry <- dbGetQuery(db, query)
  if (nrow(sub_industry) == 0) {
    dbDisconnect(db)
    return(HTML("<h3>No sub-industry found for the given stock name.</h3>"))
  }
  
  sub_industry_val <- sub_industry[[1]]
  query2 <- paste0("SELECT Name, sales_2024 FROM FinancialData WHERE LOWER(Sub_Industry) = LOWER(", dbQuoteString(db, sub_industry_val), ")")
  data <- dbGetQuery(db, query2)
  

  # Preprocess
  data$sales_2024 <- as.numeric(data$sales_2024)
  data$label <- ifelse(tolower(data$Name) == tolower(stock_name), stock_name, "Others")
  agg_data <- aggregate(sales_2024 ~ label, data = data, sum)
  
  # Plotly donut chart
  library(plotly)
  p <- plot_ly(
    data = agg_data,
    labels = ~label,
    values = ~sales_2024,
    type = 'pie',
    textinfo = 'label+percent',
    insidetextorientation = 'radial',
    marker = list(colors = c("#a9c0e8", "#f4f4f4")),
    hole = 0.5
  ) %>%
    layout(
      title = list(
        text = paste("Market Share in", sub_industry_val, "Sub-Industry"),
        x = 0.5,
        xanchor = "center",
        font = list(size = 14)
      ),
      showlegend = FALSE,
      margin = list(t = 100)
    )
  
  # Convert plot to HTML
  tmp_file <- tempfile(fileext = ".html")
  saveWidget(p, tmp_file, selfcontained = TRUE)
  dbDisconnect(db)
  readChar(tmp_file, file.info(tmp_file)$size)
}

############################################################################################################


#* @get /plot3
#* @param stock_name The name of the stock to fetch
#* @serializer html
function(stock_name = "") {
  if (stock_name == "") {
    return(HTML("<h3>Error: No stock name provided.</h3>"))
  }
  
  library(RMySQL)
  library(DBI)
  library(plotly)
  library(htmlwidgets)
  
  # Connect to DB
  db <- dbConnect(
    RMySQL::MySQL(),
    dbname = "my_database",
    host = "mysql",
    port = 3306,
    user = "stock_user",
    password = "stock_pass"
  )

  
  # Get sub-industry
  query1 <- paste0("SELECT Sub_Industry FROM FinancialData WHERE LOWER(Name) = LOWER(", dbQuoteString(db, stock_name), ")")
  sub_industry <- dbGetQuery(db, query1)
  
  if (nrow(sub_industry) == 0) stop("Stock not found.")
  
  sub_industry_val <- sub_industry[[1]]
  
  # Get DE data
  query2 <- paste0("SELECT Name, DE FROM FinancialData WHERE LOWER(Sub_Industry) = LOWER(", dbQuoteString(db, sub_industry_val), ")")
  data <- dbGetQuery(db, query2)
  
  # Clean and sort
  data$Name <- iconv(data$Name, from = "UTF-8", to = "ASCII//TRANSLIT")
  data$DE <- as.numeric(data$DE)
  data <- data[!is.na(data$DE), ]
  data$highlight <- ifelse(tolower(data$Name) == tolower(stock_name), "selected",
                           ifelse(data$DE < 0, "negative", "normal"))
  
  data$fill <- ifelse(data$highlight == "selected", "#a9c0e8",
                      ifelse(data$highlight == "negative", "#e74c3c", "#f3f3f3"))
  
  # Order companies by DE
  data <- data[order(data$DE), ]
  data$Name <- factor(data$Name, levels = data$Name)
  
  # Create interactive bar chart
  p <- plot_ly(data,
               x = ~Name,
               y = ~DE,
               type = "bar",
               marker = list(color = ~fill),
               hoverinfo = "text",
               text = ~paste0(Name, "<br>DE: ", round(DE, 2))
  ) %>%
    layout(
      title = list(
        text = paste0("Debt-to-Equity Ratio in ", sub_industry_val, " Sub-Industry"),
        x = 0.5,
        xanchor = "center",
        font=list(size=14)
      ),
      xaxis = list(title = "", showticklabels = FALSE),
      yaxis = list(title = "Debt-to-Equity"),
      margin = list(t = 100),
      shapes = list(
        list(type = "line",
            x0 = -0.5,
            x1 = length(data$Name) - 0.5,
            y0 = mean(data$DE, na.rm = TRUE),
            y1 = mean(data$DE, na.rm = TRUE),
            line = list(dash = "dash", color = "#6e9fcf", width = 1))
      )
    )

  
  # Save as self-contained HTML
  tmp_file <- tempfile(fileext = ".html")
  saveWidget(p, tmp_file, selfcontained = TRUE)
  dbDisconnect(db)
  readChar(tmp_file, file.info(tmp_file)$size)
}

############################################################################################################

#* @get /plot4
#* @param stock_name The name of the stock to fetch
#* @serializer html
function(stock_name = "") {
  if (stock_name == "") {
    return(HTML("<h3>Error: No stock name provided.</h3>"))
  }
  
  library(networkD3)
  library(readr)
  library(dplyr)
  
  # Connect to DB
  db <- dbConnect(
    RMySQL::MySQL(),
    dbname = "my_database",
    host = "mysql",
    port = 3306,
    user = "stock_user",
    password = "stock_pass"
  )
  
  # Safe query
  query <- paste0(
    "SELECT * FROM SentimentData WHERE LOWER(stock) = LOWER(", 
    dbQuoteString(db, stock_name), ")"
  )
  
  data <- tryCatch({
    dbGetQuery(db, query)
  }, error = function(e) {
    dbDisconnect(db)
    return(HTML(paste("<h3>Query failed:</h3><p>", e$message, "</p>")))
  })
  
  if (nrow(data) == 0) {
    dbDisconnect(db)
    return(HTML("<h3>No data found for stock.</h3>"))
  }
  
  print(data)
  
  # Prepare Sankey links
  layer1 <- data %>%
    group_by(stock, platform) %>%
    summarise(value = n(), .groups = 'drop') %>%
    rename(source = stock, target = platform)
  
  layer2 <- data %>%
    group_by(platform, type) %>%
    summarise(value = n(), .groups = 'drop') %>%
    rename(source = platform, target = type)
  
  sankey_links <- bind_rows(layer1, layer2)
  
  # Create unique node list
  nodes <- data.frame(name = unique(c(sankey_links$source, sankey_links$target)), stringsAsFactors = FALSE)
  
  # Map source/target to indices
  sankey_links$source_id <- match(sankey_links$source, nodes$name) - 1
  sankey_links$target_id <- match(sankey_links$target, nodes$name) - 1
  
  color_scale <- 
    'd3.scaleOrdinal()
    .range(["#a9c0e8", "#6ea8de", "#4c6faf", "#9966cc", "#2a2a72", "#b19cd9", "#8393d9", "#647ec1", "#3b5998", "#483d8b"])'
  
  # Build Sankey plot
  sankey <- sankeyNetwork(Links = sankey_links,
                          Nodes = nodes,
                          Source = "source_id",
                          Target = "target_id",
                          Value = "value",
                          NodeID = "name",
                          fontSize = 14,
                          nodeWidth = 30,
                          colourScale = color_scale)
  
  # Save widget to HTML and return
  tmp_file <- tempfile(fileext = ".html")
  saveWidget(sankey, tmp_file, selfcontained = TRUE)
  dbDisconnect(db)
  readChar(tmp_file, file.info(tmp_file)$size)
}

#########################################################################################################

#* @get /plot5
#* @param stock_name The name of the stock to fetch
#* @serializer html
function(stock_name = "") {
  if (stock_name == "") {
    return(HTML("<h3>Error: No stock name provided.</h3>"))
  }
  
  # Connect to DB
  # Connect to DB
  db <- dbConnect(
    RMySQL::MySQL(),
    dbname = "my_database",
    host = "mysql",
    port = 3306,
    user = "stock_user",
    password = "stock_pass"
  )

  
  # Safe query
  query <- paste0(
    "SELECT * FROM SentimentData WHERE LOWER(stock) = LOWER(", 
    dbQuoteString(db, stock_name), ")"
  )
  
  data <- tryCatch({
    dbGetQuery(db, query)
  }, error = function(e) {
    dbDisconnect(db)
    return(HTML(paste("<h3>Query failed:</h3><p>", e$message, "</p>")))
  })
  
  if (nrow(data) == 0) {
    dbDisconnect(db)
    return(HTML("<h3>No data found for stock.</h3>"))
  }
  
  # Define additional stopwords related to URLs
  url_stopwords <- c("http", "https", "www", "com", "tco",'t.co', "co", "org",'amp','stocks','yoy' ,"net",'share','shares','market','crore','india','financial','revenue','profit','results','stock','price','indian','company','news','profit')
  
  # Convert stock_name to lower case and split into words
  stock_words <- tolower(stock_name) %>%
    gsub("[^a-z ]", "", .) %>%
    strsplit(split = "\\s+") %>%
    unlist()
  
  word_freq <- data %>%
    select(text) %>%
    unnest_tokens(word, text) %>%
    filter(!str_detect(word, "^[0-9,.%$]+$")) %>%  # New: removes all number-like tokens
    count(word, sort = TRUE) %>%
    filter(!word %in% stop_words$word) %>%
    filter(!word %in% stock_words) %>%
    filter(!word %in% url_stopwords) %>%
    filter(nchar(word) > 2) %>%
    rename(freq = n)
  
  custom_colors <- c(
    "#a9c0e8", "#6ea8de", "#4c6faf", "#9966cc", "#2a2a72",
    "#b19cd9", "#8393d9", "#647ec1", "#3b5998", "#483d8b"
  )
  
  wc_widget <- wordcloud2(data = word_freq,
                          size = 1,
                          color = rep(custom_colors, length.out = nrow(word_freq)),
                          backgroundColor = "white",
                          fontWeight = 'bold',
                          rotateRatio = 0.5)
  
  
  # Save widget to HTML and return
  tmp_file <- tempfile(fileext = ".html")
  saveWidget(wc_widget, tmp_file, selfcontained = TRUE)
  dbDisconnect(db)
  readChar(tmp_file, file.info(tmp_file)$size)
}

#############################################################################################################

