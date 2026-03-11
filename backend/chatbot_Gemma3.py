import pandas as pd
import requests
import json
import os
import re
import textwrap

class CustomerSupportBot:
    def __init__(self, dataset_path, intents_path=None, max_response_length=600, max_tokens=300):
        self.support_data = self.load_dataset(dataset_path)
        self.intents_data = self.load_intents(intents_path) if intents_path else None
        self.model = "gemma3:1b"
        self.max_response_length = max_response_length
        self.max_tokens = max_tokens
        self.conversation_history = []
        self.max_history_length = 5

    def load_dataset(self, file_path):
        if not os.path.exists(file_path):
            print(f"Error: Dataset file {file_path} not found!")
            return []
        df = pd.read_csv(file_path)
        return [{column.lower(): row.get(column, '') for column in df.columns} 
                for _, row in df.iterrows()]

    def load_intents(self, file_path):
        if not os.path.exists(file_path):
            print(f"Error: Intents file {file_path} not found!")
            return []
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Could not parse {file_path} as JSON!")
            return []

    def extract_entities(self, query):
        entities = {
            "locations": [],
            "products": [],
            "services": [],
            "order_info": None,
            "intent": None
        }
        common_locations = ["canada", "usa", "us", "united states", "australia",
                          "uk", "united kingdom", "indonesia", "batam", "japan",
                          "china", "europe", "singapore", "malaysia"]
        entities["locations"] = [loc for loc in common_locations if loc in query.lower()]
        
        intent_keywords = {
            "shipping_inquiry": ["ship", "deliver", "send", "shipping"],
            "refund_request": ["refund", "return", "money back"],
            "order_tracking": ["track", "where", "status"]
        }
        for intent, keywords in intent_keywords.items():
            if any(kw in query.lower() for kw in keywords):
                entities["intent"] = intent
                break
        
        order_match = re.search(r'order\s*(?:number|#)?\s*[:#]?\s*(\w+)', query.lower())
        entities["order_info"] = order_match.group(1) if order_match else None
        return entities

    def get_relevant_context(self, user_query):
        entities = self.extract_entities(user_query)
        relevant_items = []
        
        # Existing context matching logic remains the same
        # ... [identical to original implementation] ...
        
        relevant_items.sort(key=lambda x: x.get('relevance', 0), reverse=True)
        return "\n".join([f"Q: {item['Q']}\nA: {item['A']}" 
                         for item in relevant_items[:5]])

    def get_response(self, user_query):
        self.conversation_history.append({"role": "user", "content": user_query})
        if len(self.conversation_history) > self.max_history_length * 2:
            self.conversation_history = self.conversation_history[-(self.max_history_length * 2):]
        
        context = self.get_relevant_context(user_query)
        entities = self.extract_entities(user_query)

        # Updated system prompt with formatting instructions
        system_prompt = f"""You are a helpful e-commerce customer support assistant.
Use this support data:
{context}

IMPORTANT:
1. Keep responses under {self.max_response_length} characters
2. Address the question directly
3. For shipping: Be specific about locations or state unknown
4. Be consistent with previous answers
5. Only ask for order numbers when necessary
6. ONLY OUTPUT PLAIN TEXT. NO JSON, CODE, OR MARKDOWN.
7. Always complete sentences, even if slightly longer than the limit.

Detected intent: {entities["intent"] or "general"}
Locations: {", ".join(entities["locations"]) if entities["locations"] else "none"}"""

        # Add conversation history context
        if len(self.conversation_history) > 2:
            history_context = "Conversation history:\n" + "\n".join(
                f"{entry['role'].capitalize()}: {entry['content']}" 
                for entry in self.conversation_history[:-1])
            system_prompt += f"\n\n{history_context}"

        try:
            # API call with improved error handling
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    "model": self.model,
                    "prompt": user_query,
                    "system": system_prompt,
                    "stream": False,
                    "options": {"num_predict": self.max_tokens}
                },
                headers={'Content-Type': 'application/json; charset=utf-8'},
                timeout=60
            )

           
            # Improved response parsing
            try:
                response_data = response.json()
                extracted_response = response_data.get('response', '')
            except json.JSONDecodeError:
                match = re.search(r'"response":"((?:\\"|[^"])*)"', response.text)
                extracted_response = match.group(1).replace('\\"', '"') if match else "Response error"

            self.conversation_history.append({"role": "assistant", "content": extracted_response})
            return self.format_response(extracted_response)

        except Exception as e:
            print(f"API Error: {str(e)}")
            return "I'm having trouble connecting to the service. Please try again later."

    def format_response(self, response):
        if len(response) <= self.max_response_length:
            return response
        
        # Intelligent truncation
        sentences = re.split(r'(?<=[.!?])\s+', response)
        truncated = []
        total_length = 0
        for sentence in sentences:
            if total_length + len(sentence) <= self.max_response_length - 3:
                truncated.append(sentence)
                total_length += len(sentence)
            else:
                break
        return ' '.join(truncated) if truncated else response[:self.max_response_length-3] + "..."

def main():
    dataset_path = "../data/Cleaned_DataSet.csv"
    intents_path = "../data/intents.json"
    support_bot = CustomerSupportBot(dataset_path, intents_path, max_response_length=600, max_tokens=300)

    print("E-Commerce Support Bot (type 'exit' to quit)")
    print("-----------------------------------------")
    print(f"Response limited to {support_bot.max_tokens} tokens and {support_bot.max_response_length} chars")
    print("-----------------------------------------")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Bot: Thank you for using our support service. Goodbye!")
            break
        response = support_bot.get_response(user_input)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()