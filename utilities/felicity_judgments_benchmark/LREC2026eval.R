library(tidyverse)


# Evaluation step

languages <- c("Akan", "Basque", "Cantonese", "Chinese", "Dutch", "Farsi", "Greek", "Hausa",
               "Hebrew", "Hindi", "Hungarian", "Igbo", "Japanese", "Khmer", "Kiitharaka", "Korean",
               "Mapudungun", "Russian", "Spanish", "Tagalog", "Telugu", "Thai", "Turkish",  "Vietnamese") 

num2myStr <- function(a){
  # convert a to 3-digit significant figures, include trailing 0's, remove initial 0
  o <- sprintf("%#.3g", a)
  
  ifelse(a < 1, substring(o, 2), o)
}


generateLaTeXrow <- function(m, n){
  # generate a LaTeX row from the m-th to the n-th (inclusive) language 
  latexRowStr <- ""
  
  for (i in m:n){
    language <- languages[i]
    
    dfComparison5 <- read_csv(paste(language, "ConsultantVSGPT5.csv", sep = ""),
                              col_types = cols(
                                ref = col_character(),
                                contextDescription = col_character(),
                                testSentence = col_character(),
                                comment.x = col_character(),
                                judgment = col_character(),
                                ChatGPT = col_character(),
                                ChatGPTnotes = col_character(),
                                contextDescriptionRepeated = col_character(),
                                testSentenceRepeated = col_character()
                              ))
    
    posEvi <- dfComparison5 %>% filter(judgment == "felicitous")
    agreeOnPos <- mean(posEvi$ChatGPT == "felicitous")
    negEvi <- dfComparison5 %>% filter(judgment %in% c("infelicitous", "*", "??", "???", "#/*"))
    agreeOnNeg <- mean(negEvi$ChatGPT == "infelicitous")
    
    latexRowStr <- paste(latexRowStr, paste(num2myStr(agreeOnPos), num2myStr(agreeOnNeg), sep = " / "), sep=" & ")
  }
  
  substring(latexRowStr, 4) # strip the initial " & "
}

generateLaTeXrow(1,8)
generateLaTeXrow(9,16)
generateLaTeXrow(17,24)
