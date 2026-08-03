from backend.config import load_workspace
from backend.conversation_manager import ConversationManager
from backend.llm import OpenRouterLLM
from backend.prompt_builder import PromptBuilder
from backend.cognitive_engine import CognitiveEngine

workspace = load_workspace("config/workspaces/clinical.yaml")

manager = ConversationManager(workspace)

llm = OpenRouterLLM(
    model=workspace.model
)

builder = PromptBuilder()

engine = CognitiveEngine()
engine.start()

conversations = manager.list_conversations()

print("\nAvailable Conversations\n")

print("N) New Conversation")

for i, conversation in enumerate(conversations, start=1):
    print(f"{i}) {conversation.stem}")

choice = input("\nChoice: ").strip()

if choice.upper() == "N":
    filepath = manager.create_conversation()
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

user_message = input("You: ")

conversation.append_user(user_message)

messages = builder.build(
    workspace,
    conversation,
)

assistant_reply = llm.generate(messages)

conversation.append_assistant(assistant_reply)

print("\nUpdated Conversation:\n")
print(conversation.content)