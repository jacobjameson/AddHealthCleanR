# Load necessary libraries
library(dplyr)
library(jsonlite)

#' Clean and Label Dataset
#'
#' This function applies labels from the built-in Add Health codebook to the given dataset.
#'
#' @param dataset A data frame representing the Add Health dataset to be cleaned and labeled.
#' @return A data frame with applied value labels.
#' @export
clean_and_label <- function(dataset) {
  # Path to the built-in codebook
  codebook_path <- system.file("extdata", "codebook.json", package = "AddHealthCleaner")
  
  # Load the codebook JSON
  codebook <- fromJSON(codebook_path)
  
  # Loop through each variable in the codebook
  for (var in names(codebook)) {
    if (var %in% names(dataset)) {
      # Create a named vector for the variable labels
      labels <- setNames(codebook[[var]]$response_label, codebook[[var]]$response_value)
      
      # Apply the labels to the dataset
      dataset[[var]] <- factor(dataset[[var]], levels = names(labels), labels = labels)
    }
  }
  
  return(dataset)
}

#' Replace "Don't know" or "Refused" with NA
#'
#' This function replaces all instances of "Don't know" or "Refused" in variables with NA.
#'
#' @param dataset A data frame representing the dataset where replacements should be made.
#' @return A data frame with "Don't know" or "Refused" replaced by NA.
#' @export
replace_dont_know_refused <- function(dataset) {
  dataset <- dataset %>%
    mutate(across(everything(), ~na_if(., "Don't know"), .names = "na_{.col}")) %>%
    mutate(across(everything(), ~na_if(., "Refused"), .names = "na_{.col}"))
  
  return(dataset)
}
