from datetime import datetime
from .instructions import sms_guide, seniors_guide
from .models import gemini_2_0_flash
import chromadb
import os
import tempfile
import uuid

db_path = os.path.join(tempfile.gettempdir(), 'chroma_db')

class MemoryChatbot:
    def __init__(self, user_id: str, db_path=db_path):
        self.user_id = user_id
        
        # Initialize ChromaDB client
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        
        # Create or get collection for conversation memory
        self.collection = self.chroma_client.get_or_create_collection(
            name='chat_memory',
            metadata={'description': 'Stores conversation context'}
        )

    def add_to_memory(self, message, response, user_id):
        # Set unique id and timestamp
        conversation_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        # Store the conversation exchange
        self.collection.add(
            documents=[f'User: {message}\nAssistant: {response}'],
            metadatas=[{
                'user_id': user_id,
                'timestamp': timestamp,
                'type': 'conversation'
            }],
            ids=[conversation_id]
        )
    
    def get_relevant_context(self, message, user_id, n_results=3):
        # Retrieve relevant past conversations
        try:
            results = self.collection.query(
                query_texts=[message],
                n_results=n_results,
                where={'user_id': user_id}
            )
            
            if results['documents']:
                return '\n'.join(results['documents'][0])
            return ''
        except:
            return ''
    
    def chat(self, message):
        # Get relevant context from memory
        user_id = self.user_id
        context = self.get_relevant_context(message, user_id)
        
        # Build prompt with context
        system_prompt = '''You are a helpful AI assistant. Use the provided conversation context to maintain continuity and remember previous interactions.'''
        
        messages = [
            {'role': 'system', 'content': system_prompt}
        ]
        
        if context:
            messages.append({
                'role': 'system', 
                'content': f'Previous conversation context:\n{context}'
            })
        
        messages.append({'role': 'user', 'content': message})
        
        response = gemini_2_0_flash(
            inbound_msg=str(messages),
            instructions=sms_guide + seniors_guide
        )
        
        # Store this exchange in memory
        self.add_to_memory(message, response, user_id)
        
        return response

if __name__ == '__main__':
    chatbot = MemoryChatbot(user_id='test_user')
    
    while True:
        user_input = input('You: ')
        if user_input.lower() == 'quit':
            break
        
        response = chatbot.chat(message=user_input)
        print(f'Bot: {response}\n')
    