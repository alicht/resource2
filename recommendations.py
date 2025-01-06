import pandas as pd

# Cost-Saving Rules Engine
def generate_cost_saving_recommendations(df):
    recommendations = []
    
    # Rule 1: Suggest switching models if applicable
    for _, row in df.iterrows():
        if row["Model"] == "gpt-4" and row["Total Tokens"] > 100:
            recommendations.append(
                f"Consider switching from GPT-4 to GPT-3.5-turbo for prompt: '{row['Prompt']}' to save up to 90%."
            )
    
    # Rule 2: Highlight high-cost queries
    high_cost_threshold = 0.05  # Set a threshold for high-cost queries
    for _, row in df.iterrows():
        if row["Cost"] > high_cost_threshold:
            recommendations.append(
                f"The prompt '{row['Prompt']}' cost ${row['Cost']:.2f}. Consider optimizing it to reduce costs."
            )

    # Rule 3: General advice for prompts with high tokens
    token_threshold = 150  # Arbitrary token threshold for advice
    for _, row in df.iterrows():
        if row["Total Tokens"] > token_threshold:
            recommendations.append(
                f"The prompt '{row['Prompt']}' used {row['Total Tokens']} tokens. Shorten the prompt to reduce token usage."
            )

    return recommendations
