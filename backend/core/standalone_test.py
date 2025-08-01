# standalone_test.py
# FINAL CORRECTED VERSION - Place this in your project root folder.

import os
import uuid
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# --- Dependencies that would normally be in other files ---
from pydantic import BaseModel, Field
from sqlalchemy import (create_engine, Column, Integer, String, Boolean, JSON, ForeignKey)
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.orm import Session
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

# Load environment variables from a .env file in the same directory
load_dotenv()

# 1. Pydantic Models
class StoryOptionLLM(BaseModel):
    text: str = Field(description="the text of the option shown to the user")
    nextNode: Dict[str, Any] = Field(description="the next node content and its options")

class StoryNodeLLM(BaseModel):
    content: str = Field(description="The main content of the story node")
    isEnding: bool = Field(description="Whether this node is an ending node")
    isWinningEnding: bool = Field(description="Whether this node is a winning ending node")
    options: Optional[List[StoryOptionLLM]] = Field(default=None, description="The options for this node")

class StoryLLMResponse(BaseModel):
    title: str = Field(description="The title of the story")
    rootNode: StoryNodeLLM = Field(description="The root node of the story")

# 2. SQLAlchemy Models
Base = declarative_base()
class Story(Base):
    __tablename__ = "stories"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    session_id = Column(String, unique=True, index=True)
    nodes = relationship("StoryNode", back_populates="story")

class StoryNode(Base):
    __tablename__ = "story_nodes"
    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id"))
    content = Column(String)
    is_root = Column(Boolean, default=False)
    is_ending = Column(Boolean, default=False)
    is_winning_ending = Column(Boolean, default=False)
    options = Column(JSON)
    story = relationship("Story", back_populates="nodes")

# 3. The Corrected Prompt
STORY_PROMPT = """
You are a master storyteller...
<...The entire long prompt with the escaped {{...}} example JSON goes here...>
HERE IS AN EXAMPLE OF THE EXACT JSON STRUCTURE YOU MUST FOLLOW (note the double curly braces to escape them):
{{
  "title": "The Quest for the Sunstone",
  "rootNode": {{
    "content": "You stand at the edge of the Whispering Woods. An ancient map points towards the Sunstone, hidden deep within. To your left is a dark, thorny path. To your right is a gently flowing river.",
    "isEnding": false,
    "isWinningEnding": false,
    "options": [
      {{
        "text": "Take the thorny path.",
        "nextNode": {{
          "content": "You push through the thorns and discover a hidden clearing with a sleeping giant. You can try to sneak past or turn back.",
          "isEnding": false,
          "isWinningEnding": false,
          "options": [
            {{
              "text": "Sneak past the giant.",
              "nextNode": {{
                "content": "You successfully sneak past and find the Sunstone! You have won!",
                "isEnding": true,
                "isWinningEnding": true,
                "options": null
              }}
            }}
          ]
        }}
      }},
      {{
        "text": "Follow the river.",
        "nextNode": {{
          "content": "You follow the river, but it leads to a dead-end waterfall. You have failed.",
          "isEnding": true,
          "isWinningEnding": false,
          "options": null
        }}
      }}
    ]
  }}
}}
Now, generate a new, unique story based on the user's theme, following this exact JSON structure.
Do not add any extra text or explanations outside of the single JSON object.
"""

# --- The StoryGenerator Class ---
class StoryGenerator:
    @classmethod
    def _get_llm(cls):
        google_api_key = os.getenv("GEMINI_API_KEY")
        if not google_api_key:
            raise ValueError("GEMINI_API_KEY not found. Please create a .env file.")
        return ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=google_api_key, temperature=0.7)

    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy") -> Story:
        llm = cls._get_llm()
        story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)
        prompt = ChatPromptTemplate.from_messages([
            ("system", STORY_PROMPT),
            ("human", f"Create the story with this theme: {theme}")
        ]).partial(format_instructions=story_parser.get_format_instructions())
        chain = prompt | llm
        raw_response = chain.invoke({})
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
        node = StoryNode(story_id=story_id, content=node_data.content, is_root=is_root, is_ending=node_data.isEnding, is_winning_ending=node_data.isWinningEnding, options=[])
        db.add(node)
        db.flush()
        if not node.is_ending and node_data.options:
            options_list = []
            for option_data in node_data.options:
                next_node_data = StoryNodeLLM.model_validate(option_data.nextNode)
                child_node = cls._process_story_node(db, story_id, next_node_data, False)
                options_list.append({"text": option_data.text, "node_id": child_node.id})
            node.options = options_list
        db.flush()
        return node

# --- Test Execution ---
def run_standalone_test():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        session_id = str(uuid.uuid4())
        theme = "a journey to the center of a mysterious, sentient planet"
        print("="*50 + "\n🚀 Starting story generation with theme: '{}'".format(theme))
        print("🤖 Calling Gemini 1.5 Flash... (this might take a few seconds)\n" + "="*50)
        generated_story = StoryGenerator.generate_story(db=db, session_id=session_id, theme=theme)
        print("\n🎉 Story generation successful!\n" + "-"*50)
        print(f"Title: {generated_story.title}")
        root_node = db.query(StoryNode).filter(StoryNode.story_id == generated_story.id, StoryNode.is_root == True).first()
        if root_node:
            print(f"\nStory Start: {root_node.content}")
            print("\nOptions:")
            if root_node.options:
                for option in root_node.options:
                    print(f"- {option['text']}")
            else:
                print("This is an ending node.")
        print("-" * 50)
    finally:
        db.close()

if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY not found. Please create a .env file in this directory.")
    else:
        run_standalone_test()