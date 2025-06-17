FROM rstudio/plumber

# Install required system packages
RUN apt-get update && apt-get install -y libmysqlclient-dev libglpk-dev pandoc

WORKDIR /app

# Install required R packages
RUN R -e "install.packages(c('plumber', 'DBI', 'RMySQL', 'plotly', 'htmlwidgets', 'htmltools', 'networkD3', 'readr', 'dplyr', 'wordcloud2', 'tidytext', 'stringr', 'igraph'))"

COPY . .

EXPOSE 8000

CMD ["Rscript", "RStudio/starter_rapi.R"]