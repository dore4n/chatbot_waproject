from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import add_messages, StateGraph, START, END
from typing import Sequence, TypedDict
from langchain_core.messages import BaseMessage

class GraphState(TypedDict):
    messages: Sequence[BaseMessage]

def create_graph(research_agent):
    graph_builder = StateGraph(GraphState)
    graph_builder.add_node("research_node", research_agent)
    graph_builder.add_edge(START, "research_node")
    
    def chart_to_research_condition(state: GraphState) -> str:
        chart_content = state["messages"][-1].content
        if "QUESTION_TO_RESEARCHER" in chart_content:
            return "research_more"
        else:
            return "path_end"
    
    graph_builder.add_conditional_edges(
        "research_node", 
        chart_to_research_condition, 
        {"research_more": "research_node", "path_end": END}
    )
    
    return graph_builder.compile()
