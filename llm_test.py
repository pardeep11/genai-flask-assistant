from model import gemini_response,local_llama_response

def call_all_models(system_prompt, user_prompt):
    gemini_result =gemini_response(system_prompt, user_prompt)
    local_llama_result = local_llama_response(system_prompt, user_prompt)

    print("local_llama_result:\n", local_llama_result.content)
    print("\ngemini_response:\n", gemini_result.content)

# Example call to test all models
call_all_models("You are a helpful assistant who provides concise and accurate answers", "What is the capital of Canada? Tell me a cool fact about it as well")
