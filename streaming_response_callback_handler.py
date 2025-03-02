from langchain_core.callbacks import BaseCallbackHandler

class StreamingResponseCallbackHandler(BaseCallbackHandler):
    def __init__(self, thinking_area, text_area):
        self.thinking_area = thinking_area
        self.thinking_text = ""
        self.text_area = text_area
        self.text = ""

    def on_llm_new_token(self, token: list[dict], **kwargs):
        """Handle new tokens from the LLM."""
        text_result = ""
        thinking_result = ""
        try:
            for item in token:
                if item.get('type') and item['type'] == 'text':
                    text_result += item['text']
                elif item.get('type') and item['type'] == 'tool_result':
                    text_result += item['text']
                elif item.get('type') and item['type'] == 'reasoning_content' and item['reasoning_content']['type'] == 'text':
                    thinking_result += f"<i style='color: darkgray;'>{item['reasoning_content']['text']}</i>"
        except Exception as e:
            print(f"Error: {e}")
            print(f"Token: {token}")
        self.text += text_result
        self.thinking_text += thinking_result
        self.text_area.markdown(self.text)
        self.thinking_area.markdown(self.thinking_text, unsafe_allow_html=True)