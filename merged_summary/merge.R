# R Script to Vertically Merge CSV Files and Add a Source Column

# --- Instructions ---
# 1. Place all the CSV files you want to merge into a single folder.
# 2. Set the `folder_path` variable below to the path of that folder.
#    - Example for Windows: "C:/Users/YourUser/Documents/CSV_Data"
#    - Example for macOS/Linux: "/Users/youruser/Documents/CSV_Data"
# 3. Run the entire script.

# --- Configuration ---
# DEFINE THE PATH TO YOUR FOLDER CONTAINING THE CSV FILES
folder_path <- "~/Desktop/dataset creation/merge" # The "." means the current working directory. Change this to your folder path.

# --- Package Management ---
# This script uses the 'dplyr' package for a more robust merge.
# The following code will check if dplyr is installed, and install it if not.
if (!require(dplyr)) {
  install.packages("dplyr")
  library(dplyr)
}


# --- Script Logic ---

# Step 1: Get a list of all CSV files in the specified folder
# The `pattern` argument ensures we only select files ending with .csv
# The `full.names = TRUE` provides the complete path to each file, which is needed for reading.
csv_files <- list.files(path = folder_path, pattern = "*.csv", full.names = TRUE)

# Check if any CSV files were found
if (length(csv_files) == 0) {
  stop("No CSV files found in the specified directory. Please check the 'folder_path'.")
}

# Step 2: Read each CSV and add a source column
# We use lapply to apply a function to each file in our list of csv_files.
list_of_dataframes <- lapply(csv_files, function(file_path) {
  
  # Read the CSV file into a dataframe.
  # CRITICAL FIX: `colClasses = "character"` reads all columns as text first.
  # This prevents errors when a column has a different data type in different files
  # (e.g., all numbers in one file, but contains text in another).
  df <- read.csv(file_path, stringsAsFactors = FALSE, colClasses = "character")
  
  # Extract the base name of the file (e.g., "data_2023" from "/path/to/data_2023.csv")
  # This will be used as the value in our new column.
  file_name <- tools::file_path_sans_ext(basename(file_path))
  
  # Add the new 'source_file' column to the dataframe.
  # The value in this column will be the file's base name for every row.
  df[["source_file"]] <- file_name
  
  # Return the modified dataframe
  return(df)
})

# Step 3: Merge all the dataframes in the list vertically (row-binding)
# We use dplyr's bind_rows() function. It is more flexible than base R's rbind()
# because it will match columns by name and fill in missing values with NA.
# This resolves the "names do not match" error if your CSVs have slightly different columns.
merged_data <- dplyr::bind_rows(list_of_dataframes)


# --- Output ---

# Display the first few rows of the final merged dataframe
cat("--- Merged Data Head ---\n")
print(head(merged_data))

# Display the last few rows to show data from different files
cat("\n--- Merged Data Tail ---\n")
print(tail(merged_data))

# Display the structure of the final dataframe to show all columns
cat("\n--- Merged Data Structure ---\n")
str(merged_data)

# Optional: Save the merged dataframe to a new CSV file
# Uncomment the line below to enable saving.
write.csv(merged_data, file.path(folder_path, "merged_output_vertical.csv"), row.names = FALSE)

cat("\nScript finished successfully.\n")
cat(length(csv_files), "files were merged into a dataframe with", 
    nrow(merged_data), "rows and", ncol(merged_data), "columns.\n")

