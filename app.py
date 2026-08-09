from backend.config import load_workspace
from backend.conversation_manager import ConversationManager
from backend.llm import OpenRouterLLM
from backend.prompt_builder import PromptBuilder

workspace = load_workspace("config/workspaces/clinical.yaml")

manager = ConversationManager(workspace)

llm = OpenRouterLLM(
    model=workspace.model
)

builder = PromptBuilder()

conversations = manager.list_conversations()

print("\nAvailable Conversations\n")

print("N) New Conversation")

for i, conversation in enumerate(conversations, start=1):
    print(f"{i}) {conversation.stem}")

choice = input("\nChoice: ").strip()

if choice.upper() == "N":
    filepath = manager.create_conversation(model=workspace.model)
    conversation = manager.load_conversation(filepath)

else:
    try:
        index = int(choice) - 1

        if 0 <= index < len(conversations):
            conversation = manager.load_conversation(
                conversations[index]
            )
        else:
            print("\nInvalid conversation number.")
            raise SystemExit

    except ValueError:
        print("\nInvalid choice.")
        raise SystemExit

print(f"\nConversation: {conversation.title}\n")
print("Type 'exit' or 'quit' to end the conversation.\n")

# Multi-turn conversation loop
while True:
    user_message = input("You: ").strip()
    
    # Check for exit command
    if user_message.lower() in ['exit', 'quit']:
        print("\nGoodbye!")
        break
    
    # Skip empty messages
    if not user_message:
        continue
    
    # Add user message to conversation
    conversation.append_user(user_message)
    
    # Build prompt with context
    messages = builder.build(
        workspace,
        conversation,
    )
    
    # Generate assistant reply
    assistant_reply = llm.generate(messages)
    
    # Add assistant reply to conversation
    conversation.append_assistant(assistant_reply)
    
    # Show the reply
    print(f"\nAssistant: {assistant_reply}\n")

print("\nUpdated Conversation:\n")
print(conversation.content)