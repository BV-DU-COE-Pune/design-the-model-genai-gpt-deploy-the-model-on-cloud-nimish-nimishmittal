import tkinter as tk
from tkinter import scrolledtext
import boto3
import json

# Initialize the Bedrock client
bedrock = boto3.client(service_name="bedrock-runtime", region_name="us-west-2")

def generate_response():
    user_prompt = prompt_entry.get("1.0", tk.END).strip()
    if not user_prompt:
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Please enter a prompt.")
        output_text.config(state=tk.DISABLED)
        return
    
    try:
        response = bedrock.invoke_model(
            modelId="meta.llama3-70b-instruct-v1:0",
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "prompt": user_prompt,
                "max_gen_len": 512,
                "temperature": 0.5,
                "top_p": 0.9
            })
        )
        result = json.loads(response["body"].read().decode("utf-8"))
        output = result.get("generated_text", "No response generated.")
    except Exception as e:
        output = f"Error: {str(e)}"
    
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, output)
    output_text.config(state=tk.DISABLED)

# Tkinter UI setup
root = tk.Tk()
root.title("Llama 3 Chatbot")
root.geometry("500x400")

tk.Label(root, text="Enter Prompt:").pack(pady=5)
prompt_entry = scrolledtext.ScrolledText(root, width=60, height=5)
prompt_entry.pack(pady=5)

generate_button = tk.Button(root, text="Generate", command=generate_response)
generate_button.pack(pady=5)

tk.Label(root, text="Response:").pack(pady=5)
output_text = scrolledtext.ScrolledText(root, width=60, height=10, state=tk.DISABLED)
output_text.pack(pady=5)

root.mainloop()