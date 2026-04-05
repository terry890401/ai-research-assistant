from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_web(query: str) -> str:
    results = tavily.search(query=query, max_results=3)
    
    # 把搜尋結果整理成文字
    output = []
    for r in results["results"]:
        output.append(f"標題：{r['title']}\n內容：{r['content']}\n來源：{r['url']}")
    
    return "\n\n".join(output)