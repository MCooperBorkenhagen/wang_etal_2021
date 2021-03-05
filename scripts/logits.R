



probability_from_odds = function(odds){
  #' Calculate the probability from an odds value
  #' 
  #' @param odds The odds value
  #' @return The associated probability for odds
  P <- odds / (1 + odds)
  return(P)
}

from_logit <- function(logit, return_probability = TRUE){
  #' Calculate the probability or odds from a logit (log-odds) value
  #' 
  #' @param logit The log-odds from which you'd like to calculate
  #' @param return_probability If TRUE, return the probability, else return odds
  #' @return A value of class numeric representing either the probability or odds calculation of logit.
  #' @examples None
  odds <- exp(logit)
  P <- probability_from_odds(odds)
  if (return_probability){return(P)}
  else{return(odds)}
}

intercept_probability = function(model){
  #' Calculate the probability associated with the intercept of a statistical model
  #' 
  #' @param model A model of class glmerMod or glm
  #' @return The probability associated with the intercept of model
  #' @examples None
  coefficients = summary(model)$coefficients
  P = from_logit(coefficients['(Intercept)', 'Estimate'])
  return(P)
}


predictor_probability = function(model, predictor, return_unit_difference = TRUE){
  #' Calculate the probability associated with the predictor of a statistical model
  #' @param model A model of class glmerMod or glm
  #' @param predictor The predictor for which the probability should be calculated
  #' @param return_unit_increase If TRUE, return the probability associated with a one-unit increase in predictor, else return its probability at intercept.
  #' @return A probability of class numeric.

  # assumes a one-unit increase in the predictor
  coefficients = summary(model)$coefficients
  odds = from_logit(coefficients[predictor, 'Estimate'], return_probability = F) # Gets your odds associated with a one unit increase in variable
  intercept <- from_logit(coefficients['(Intercept)', 'Estimate'], return_probability = F) # This gives you odds at intercept (wherever you have centered)
  odds_one_unit_increase <- odds*intercept #calculate the odds ratio with one unit increase
  P_intercept <- from_logit(coefficients['(Intercept)', 'Estimate']) #generate a probability from the odds caluculation; P is the probability at intercept of getting a 1 on DV
  P_one_unit_increase <- probability_from_odds(odds_one_unit_increase) #this is the probability with a one unit increase in the variable, ie, getting a 1 on the DV with a one unit increase in the IV
  diff_P <- P_one_unit_increase - P_intercept #calculate the difference in probability with a one unit increase
  diff_P # This is the difference in probability of X at zero plus one versus X at zero
  if (return_unit_difference){return(diff_P)} # returns the probability difference between intercept and intercept plus one on your predictor
  else{return(P_one_unit_increase)} # returns the probability at intercept plus one on your predictor
}


