# Create a data frame with the updated data
data <- data.frame(
  Label_Aspect = c("Context", "Emotion", "Culture", "Overall"),
  Total_Annotations = c(44, 47, 47, 138),
  Preference_Finetuned = c(29, 42, 35, 106),
  Preference_Baseline = c(15, 5, 12, 32),
  Preference_Percentage = c(66.37, 89.41, 74.64, 76.81)
)

# Function to calculate Cohen's h
cohens_h <- function(p1, p2) {
  return(2 * asin(sqrt(p1)) - 2 * asin(sqrt(p2)))
}

# Perform binomial tests for each label aspect and overall
results <- data.frame(
  Label_Aspect = character(),
  P_Value = numeric(),
  Effect_Size = numeric(),
  stringsAsFactors = FALSE
)

for (i in 1:nrow(data)) {
  label_aspect <- data$Label_Aspect[i]
  total_annotations <- data$Total_Annotations[i]
  pref_finetuned <- data$Preference_Finetuned[i]
  pref_baseline <- data$Preference_Baseline[i]
  pref_percentage <- data$Preference_Percentage[i] / 100
  
  binom_test <- binom.test(pref_finetuned, total_annotations, p = 0.5, alternative = "greater")
  p_value <- binom_test$p.value
  effect_size <- cohens_h(pref_finetuned / total_annotations, pref_baseline / total_annotations)
  
  
  results <- rbind(results, data.frame(Label_Aspect = label_aspect, P_Value = format(round(p_value, 5), nsmall = 2), Effect_Size = effect_size))
}

# Print the results
print(results)
print(binom_test)

library(ggplot2)
library(dplyr)

# Create a data frame with the information
data <- data.frame(
  Aspect = c("Context", "Emotion", "Culture"),
  Correct = c(29, 42, 35),
  Total = c(44, 47, 47)
)

# Calculate proportions
data <- data %>%
  mutate(Proportion = Correct / Total)

# Add overall data
overall <- data.frame(
  Aspect = "Overall",
  Correct = sum(data$Correct),
  Total = sum(data$Total),
  Proportion = sum(data$Correct) / sum(data$Total)
)

# Combine the overall data with the rest
data <- rbind(data, overall)

# Plot
ggplot(data, aes(x = Aspect, y = Proportion)) +
  geom_bar(stat = "identity", fill = "grey", width = 0.5) +
  geom_text(aes(label = scales::percent(Proportion)), 
            position = position_dodge(width = 0.8), 
            vjust = -0.25, 
            size = 3.5) +
  geom_hline(yintercept = 0.5, linetype = "dashed") +
  ylim(0, 1) +
  labs(y = "Proportion of Correct Responses", 
       x = "Aspect", 
       title = "Proportion of Correct Responses by Aspect") +
  theme_minimal() +
  theme(legend.position = "none")
