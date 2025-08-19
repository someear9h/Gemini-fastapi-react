

from sqlalchemy.orm import Session
# <<< CHANGED: Import ChatGoogleGenerativeAI instead of ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.prompts import STORY_PROMPT
from models.story import Story, StoryNode
from core.models import StoryLLMResponse, StoryNodeLLM
from dotenv import load_dotenv
import os

# This will load your GEMINI_API_KEY from the .env file
load_dotenv()

class StoryGenerator:

    @classmethod
    def _get_llm(cls):
        # <<< CHANGED: This entire method is updated for Google Gemini
        google_api_key = os.getenv("GEMINI_API_KEY")
        if not google_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")

        # We instantiate the Google model here.
        # "gemini-1.5-flash-latest" is the recommended name for the 1.5 Flash model.
        # Temperature controls creativity. 0.7 is a good starting point.
        return ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=google_api_key, temperature=0.7)

    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy") -> Story:
        # --- NO CHANGES NEEDED IN THIS METHOD ---
        # This method is perfectly written. By swapping the LLM in _get_llm(),
        # the rest of the logic works seamlessly with the new model.

        llm = cls._get_llm()
        story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                STORY_PROMPT
            ),
            (
                "human",
                f"Create the story with this theme: {theme}"
            )
        ]).partial(format_instructions=story_parser.get_format_instructions())

        raw_response = llm.invoke(prompt.invoke({}))

        response_text = raw_response
        if hasattr(raw_response, "content"):
            response_text = raw_response.content

        story_structure = story_parser.parse(response_text)

        story_db = Story(title=story_structure.title, session_id=session_id)
        db.add(story_db)
        db.flush()

        root_node_data = story_structure.rootNode
        if isinstance(root_node_data, dict):
            root_node_data = StoryNodeLLM.model_validate(root_node_data)

        cls._process_story_node(db, story_db.id, root_node_data, is_root=True)

        db.commit()
        return story_db

    @classmethod
    def _process_story_node(cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool = False) -> StoryNode:
        # --- NO CHANGES NEEDED IN THIS METHOD ---
        # This is all database logic and is independent of the LLM used.

        node = StoryNode(
            story_id=story_id,
            content=node_data.content if hasattr(node_data, "content") else node_data["content"],
            is_root=is_root,
            is_ending=node_data.isEnding if hasattr(node_data, "isEnding") else node_data["isEnding"],
            is_winning_ending=node_data.isWinningEnding if hasattr(node_data, "isWinningEnding") else node_data["isWinningEnding"],
            options=[]
        )
        db.add(node)
        db.flush()

        if not node.is_ending and (hasattr(node_data, "options") and node_data.options):
            options_list = []
            for option_data in node_data.options:
                next_node = option_data.nextNode

                if isinstance(next_node, dict):
                    next_node = StoryNodeLLM.model_validate(next_node)

                child_node = cls._process_story_node(db, story_id, next_node, False)

                options_list.append({
                    "text": option_data.text,
                    "node_id": child_node.id
                })

            node.options = options_list

        db.flush()
        return node