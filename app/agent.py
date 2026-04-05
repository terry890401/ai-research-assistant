from tavily import TavilyClient
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated
from pydantic import BaseModel
import operator
from dotenv import load_dotenv
import os
import json

load_dotenv()
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

class ResearchReport(BaseModel):
    title: str
    summary: str
    key_points: list[str]
    conclusion: str

# 定義工具
@tool
def search_web(query: str) -> str:
    """搜尋網路上關於特定主題的資訊"""
    results = tavily.search(query=query, max_results=3)
    output = []
    for r in results["results"]:
        output.append(f"標題：{r['title']}\n內容：{r['content']}\n來源：{r['url']}")
    return "\n\n".join(output)

# LLM 綁定工具
tools = [search_web]
llm_with_tools = llm.bind_tools(tools)

# State 定義
class ResearchState(TypedDict):
    topic: str
    messages: Annotated[list, operator.add]  # 對話歷史，自動累加
    report: dict

# Node 1：Agent 決定要做什麼
def agent_node(state: ResearchState) -> ResearchState:
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# Node 2：執行工具
tool_node = ToolNode(tools)

# Node 3：產生最終報告
def report_node(state: ResearchState) -> ResearchState:
    # 整理所有搜尋結果
    search_content = ""
    for msg in state["messages"]:
        if hasattr(msg, "content") and isinstance(msg.content, str):
            search_content += msg.content + "\n"

    response = llm.invoke(f"""
        根據以下資料，針對「{state['topic']}」產生研究報告。
        只回傳 JSON，不要加 markdown：
        {{
            "title": "報告標題",
            "summary": "摘要（100字內）",
            "key_points": ["重點1", "重點2", "重點3"],
            "conclusion": "結論"
        }}

        資料：{search_content}
    """)
    content = response.content.strip().replace("```json", "").replace("```", "").strip()
    report = ResearchReport(**json.loads(content))
    return {"report": report.model_dump()}

# 判斷下一步：還要繼續用工具，還是產生報告
def should_continue(state: ResearchState) -> str:
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "report"

# 建立 Agent
def build_agent():
    graph = StateGraph(ResearchState)

    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)
    graph.add_node("report", report_node)

    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue, {
        "tools": "tools",
        "report": "report"
    })
    graph.add_edge("tools", "agent")
    graph.add_edge("report", END)

    return graph.compile()

agent = build_agent()

def run_research(topic: str) -> dict:
    from langchain_core.messages import HumanMessage
    initial_message = HumanMessage(content=f"請幫我研究「{topic}」這個主題，搜尋相關資訊後產生報告")
    result = agent.invoke({
        "topic": topic,
        "messages": [initial_message],
        "report": {}
    })
    return result["report"]