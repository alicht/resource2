import openai
import os

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def track_openai_usage(prompt, model="gpt-3.5-turbo"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        total_tokens = response["usage"]["total_tokens"]
        prompt_tokens = response["usage"]["prompt_tokens"]
        completion_tokens = response["usage"]["completion_tokens"]
        cost = calculate_cost(total_tokens, model)
        optimization_tip = get_optimization_tip(total_tokens, model)

        return {
            "response": response["choices"][0]["message"]["content"],
            "total_tokens": total_tokens,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "cost": cost,
            "optimization_tip": optimization_tip,
        }
    except Exception as e:
        return {"error": str(e)}

def calculate_cost(total_tokens, model):
    pricing = {"gpt-3.5-turbo": 0.002, "gpt-4": 0.03}  # Cost per 1k tokens
    cost_per_token = pricing.get(model, 0.001)
    return (total_tokens / 1000) * cost_per_token

def get_optimization_tip(total_tokens, model):
    if model == "gpt-4" and total_tokens > 1000:
        return "Switch to GPT-3.5-turbo for large prompts to save up to 93% on costs."
    elif model == "gpt-3.5-turbo" and total_tokens > 2000:
        return "Consider optimizing your prompt to reduce token usage."
    return "Your current model choice and usage are cost-effective."
