from enum import Enum

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from agents.tools.get_current_weather import get_current_weather
from agents.workflows import metaprompts


class Node(str, Enum):
    def __str__(self):
        return str(self.value)
    ASSISTANT = "assistant"
    TOOLS = "tools"


class ToolsMarkdownWorkflow():
    def __init__(self, llm):
        self.tools = [get_current_weather]
        self.llm_with_tools = llm.bind_tools(self.tools)
        self.graph = self.build_graph().compile()

    def build_graph(self) -> StateGraph:
        """Short Term Memory (~ReAct Framework)
        1. The model should remember the last 4 messages. State is only persisted in memory
            and will be lost when the socket connection is recreated.
        2. The model responds to the user in Markdown format.
        """
        builder = StateGraph(MessagesState)
        builder.add_node(
            Node.ASSISTANT, lambda state: self.__request_with_short_memory(state))
        builder.add_node(Node.TOOLS, ToolNode(self.tools))
        builder.add_edge(START, Node.ASSISTANT)
        builder.add_conditional_edges(Node.ASSISTANT, tools_condition)
        builder.add_edge(Node.TOOLS, Node.ASSISTANT)
        return builder

    def __request_with_short_memory(self, state: MessagesState) -> dict:
        """
        Generate answer including the last four messages as context
        """
        last_four_messages = state["messages"][-4:]
        system_message = SystemMessage(
            metaprompts.CONVERSATION_MARKDOWN_ASSISTANT)
        return {"messages": [self.llm_with_tools.invoke([system_message] + last_four_messages)]}


# Enable to display graph in langgraph studio
# dev_model = ChatOpenAI(model="gpt-4o")
# graph = ToolsMarkdownWorkflow(dev_model).graph
