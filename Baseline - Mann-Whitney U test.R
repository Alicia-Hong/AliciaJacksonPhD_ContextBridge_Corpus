#install.packages("reshape")
#install.packages("reshape2")
#install.packages("car")

# Load required libraries
library(dplyr)
library(ggplot2)
library(pwr)
library(reshape2)
library(car)  # For assumption testing
library(moments)  # For assumption testing
library(knitr)  # For table formatting

setwd("C:\\Users\\pjack\\Desktop\\thesis analysis")

# Load data 
data <- read.csv("thesis test2.csv")

# Split data by language
chinese_data <- data %>% filter(language == "CN")
english_data <- data %>% filter(language == "EN")

# Combine context, emotion, and cultural scores
# Load a new combined dataset
combined_data <- read.csv("combined thesis test2.csv")

# Split data by language
combined_chinese_data <- combined_data %>% filter(language == "CN")
combined_english_data <- combined_data %>% filter(language == "EN")

##################################STEP 1.ASSUMPTION TESTS#########################################
# Assumption testing for t-test
# 1. Normality assumption
shapiro_test_chinese1 <- shapiro.test(combined_chinese_data$accuracy)
shapiro_test_english1 <- shapiro.test(combined_english_data$accuracy)
shapiro_test_chinese2 <- shapiro.test(combined_chinese_data$sufficiency_or_confidence)
shapiro_test_english2 <- shapiro.test(combined_english_data$sufficiency_or_confidence)
shapiro_test_chinese
shapiro_test_english
shapiro_test_chinese2
shapiro_test_english2
# 2. Homogeneity of variance assumption
combined_data$language <- factor(combined_data$language)
levene_test1 <- leveneTest(accuracy ~ language, data = combined_data)
levene_test1
levene_test2 <- leveneTest(sufficiency_or_confidence ~ language, data = combined_data)
levene_test2
# 3. Independence assumption (assumed to be satisfied based on the study design)

# Print assumption test results
print("Assumption Testing Results:")
print(paste("Shapiro-Wilk Normality Test - Chinese Data: p =", round(shapiro_test_chinese$p.value, 3)))
print(paste("Shapiro-Wilk Normality Test - English Data: p =", round(shapiro_test_english$p.value, 3)))
print(paste("Levene's Test for Homogeneity of Variance: p =", round(levene_test$`Pr(>F)`[1], 3)))

#######################STEP 2.NON-PARAMETRICS TESTS (normality violated)#########################

# Function to perform Mann-Whitney U test and store results in a data frame
perform_mann_whitney_test <- function(chinese_data, english_data, var_name) {
  mann_whitney_result <- wilcox.test(chinese_data[[var_name]], english_data[[var_name]], alternative = "two.sided")
  
  # Extract relevant information from the Mann-Whitney U test result
  w_val <- round(mann_whitney_result$statistic, 3)
  p_val <- round(mann_whitney_result$p.value, 3)
  mean_chinese <- round(mean(chinese_data[[var_name]], na.rm = TRUE), 3)
  mean_english <- round(mean(english_data[[var_name]], na.rm = TRUE), 3)
  sd_chinese <- round(sd(chinese_data[[var_name]], na.rm = TRUE), 3)
  sd_english <- round(sd(english_data[[var_name]], na.rm = TRUE), 3)
  
  # Calculate Cohen's d effect size
  pooled_sd <- sqrt(((nrow(chinese_data) - 1) * sd_chinese^2 + (nrow(english_data) - 1) * sd_english^2) / (nrow(chinese_data) + nrow(english_data) - 2))
  cohen_d <- round((mean_chinese - mean_english) / pooled_sd, 3)
  
  # Create a data frame with the Mann-Whitney U test results and additional statistics
  mann_whitney_df <- data.frame(
    Metric = var_name,
    n_CN = nrow(chinese_data),
    n_EN = nrow(english_data),
    W_Val = w_val,
    p_Val = p_val,
    Mean_CN = mean_chinese,
    Mean_EN = mean_english,
    SD_CN = sd_chinese,
    SD_EN = sd_english,
    Cohen_d = cohen_d,
    u1 <- w_val,
    u2 <- n_chinese * n_english - u1,
    effect_size <- (2 * min(u1, u2) / (n_chinese * n_english)) - 1
  )
  
  return(mann_whitney_df)
}

# Perform Mann-Whitney U tests for individual variables and store results in a data frame
mann_whitney_results <- rbind(
  perform_mann_whitney_test(chinese_data, english_data, "context_accuracy"),
  perform_mann_whitney_test(chinese_data, english_data, "context_sufficiency"),
  perform_mann_whitney_test(chinese_data, english_data, "emotion_accuracy"),
  perform_mann_whitney_test(chinese_data, english_data, "emotion_confidence"),
  perform_mann_whitney_test(chinese_data, english_data, "culture_accuracy"),
  perform_mann_whitney_test(chinese_data, english_data, "culture_sufficiency")
)

# Perform Mann-Whitney U tests for overall variables and store results in a data frame
mann_whitney_results_overall <- rbind(
  perform_mann_whitney_test(combined_chinese_data, combined_english_data, "accuracy"),
  perform_mann_whitney_test(combined_chinese_data, combined_english_data, "sufficiency_or_confidence")
)

# Print Mann-Whitney U test results data frame
print("Mann-Whitney U Test Results:")
kable(mann_whitney_results, digits = 3)

print("Overall Mann-Whitney U Test Results:")
kable(mann_whitney_results_overall, digits = 3)

all_mann_whitney_results <- union(mann_whitney_results,mann_whitney_results_overall )

write.csv(all_mann_whitney_results, file = "ann_whitney_results.csv")


'''
# Calculate statistical power
power_analysis <- pwr.t.test(n = nrow(chinese_data) + nrow(english_data), d = 0.5, sig.level = 0.05, power = NULL, alternative = "two.sided")
print("Power Analysis:")
print(power_analysis)

# Calculate desired statistical power
desired_power_analysis <- pwr.t.test(n = NULL, d = 0.5, sig.level = 0.05, power = 0.8, alternative = "two.sided")
print("Desired Power Analysis:")
print(desired_power_analysis)

# Suggest sample size improvement
suggested_sample_size <- ceiling(desired_power_analysis$n / 2)
print(paste("To achieve a statistical power of 0.8 with a significance level of 0.05, it is recommended to have a sample size of at least", suggested_sample_size, "for each language."))

'''

#########################################STEP 3 VISUALIZATION######################################

# Visualize data
ggplot(data, aes(x = language, y = context_accuracy, fill = language)) +
  geom_boxplot() +
  labs(title = "Context Accuracy by Language", x = "Language", y = "Context Accuracy")

ggplot(data, aes(x = language, y = context_sufficiency, fill = language)) +
  geom_boxplot() +
  labs(title = "Context Sufficiency by Language", x = "Language", y = "Context Sufficiency")

# Create combined boxplot
boxplot_data <- melt(data, id.vars = "language", measure.vars = c("context_accuracy", "context_sufficiency", "emotion_accuracy", "emotion_confidence", "culture_accuracy", "culture_sufficiency"))
ggplot(boxplot_data, aes(x = language, y = value, fill = language)) +
  geom_boxplot() +
  facet_wrap(~variable, ncol = 2, scales = "free_y") +
  labs(title = "Accuracy, Sufficiency or Confidence Scores by Language", x = "Language", y = "Score") +
  theme_bw()

# Create combined boxplot
boxplot_data2 <- melt(combined_data, id.vars = "language", measure.vars = c("accuracy", "sufficiency_or_confidence"))
ggplot(boxplot_data2, aes(x = language, y = value, fill = language)) +
  geom_boxplot() +
  facet_wrap(~variable, ncol = 2, scales = "free_y") +
  labs(title = "Overall Accuracy and Sufficiency/Confidence Scores by Language", x = "Language", y = "Score") +
  theme_bw()


# Create density plots for individual variables
density_data <- melt(data, id.vars = "language", measure.vars = c("context_accuracy", "context_sufficiency", "emotion_accuracy", "emotion_confidence", "culture_accuracy", "culture_sufficiency"))

ggplot(density_data, aes(x = value, fill = language)) +
  geom_density(alpha = 0.5) +
  facet_wrap(~variable, ncol = 2, scales = "free") +
  labs(title = "Density Plots of Accuracy, Sufficiency or Confidence Scores by Language",
       x = "Score", y = "Density") +
  theme_bw()

# Create density plots for overall variables
density_data2 <- melt(combined_data, id.vars = "language", measure.vars = c("accuracy", "sufficiency_or_confidence"))

ggplot(density_data2, aes(x = value, fill = language)) +
  geom_density(alpha = 0.5) +
  facet_wrap(~variable, ncol = 2, scales = "free") +
  labs(title = "Density Plots of Overall Accuracy and Sufficiency/Confidence Scores by Language",
       x = "Score", y = "Density") +
  theme_bw()

# Create density plots for individual variables
density_data <- melt(data, id.vars = "language", measure.vars = c("context_accuracy", "context_sufficiency", "emotion_accuracy", "emotion_confidence", "culture_accuracy", "culture_sufficiency"))

ggplot(density_data, aes(x = value, fill = language)) +
  geom_density(alpha = 0.5) +
  facet_wrap(~variable, ncol = 2, scales = "free") +
  labs(title = "Density Plots of Accuracy, Sufficiency or Confidence Scores by Language",
       x = "Score", y = "Density") +
  theme_bw()

# Create density plots for overall variables
density_data2 <- melt(combined_data, id.vars = "language", measure.vars = c("accuracy", "sufficiency_or_confidence"))

ggplot(density_data2, aes(x = value, fill = language)) +
  geom_density(alpha = 0.5) +
  facet_wrap(~variable, ncol = 2, scales = "free") +
  labs(title = "Density Plots of Overall Accuracy and Sufficiency/Confidence Scores by Language",
       x = "Score", y = "Density") +
  theme_bw()

# Create violin plots for individual variables
violin_data <- melt(data, id.vars = "language", measure.vars = c("context_accuracy", "context_sufficiency", "emotion_accuracy", "emotion_confidence", "culture_accuracy", "culture_sufficiency"))

ggplot(violin_data, aes(x = language, y = value, fill = language)) +
  geom_violin() +
  geom_boxplot(width = 0.1, fill = "white", outlier.shape = NA) +
  facet_wrap(~variable, ncol = 2, scales = "free_y") +
  labs(title = "Violin Plots of Accuracy, Sufficiency or Confidence Scores by Language",
       x = "Language", y = "Score") +
  theme_bw()

# Create violin plots for overall variables
violin_data2 <- melt(combined_data, id.vars = "language", measure.vars = c("accuracy", "sufficiency_or_confidence"))

ggplot(violin_data2, aes(x = language, y = value, fill = language)) +
  geom_violin() +
  geom_boxplot(width = 0.1, fill = "white", outlier.shape = NA) +
  facet_wrap(~variable, ncol = 2, scales = "free_y") +
  labs(title = "Violin Plots of Overall Accuracy and Sufficiency/Confidence Scores by Language",
       x = "Language", y = "Score") +
  theme_bw()