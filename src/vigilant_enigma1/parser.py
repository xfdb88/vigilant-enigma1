import re, json
from typing import Dict, Tuple, List, Optional, Any
from bs4 import BeautifulSoup

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-ZaZ0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:\+?\d[\d\s\-]{7,}\d)")
LINK_RE = re.compile(r"https?://[^\s\"')]+", re.I)

def extract_structured_json(html: str) -> Optional[dict]:
    """
    优先从 <script type="application/ld+json"> 提取结构化 JSON；
    次选尝试解析内嵌数据块（页面 props/sharedData 等）。
    """
    soup = BeautifulSoup(html, "lxml")
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            txt = s.get_text(strip=True); 
            if not txt: continue
            obj = json.loads(txt)
            # 兼容数组形式
            if isinstance(obj, list):
                for it in obj:
                    if isinstance(it, dict) and it.get("@type") in {"Person","Organization"}: return it
            elif isinstance(obj, dict) and obj.get("@type") in {"Person","Organization"}: return obj
        except Exception: continue
    # 简单兜底：匹配 props/sharedData 片段尝试反序列化
    for pat in (r"window\._sharedData\s*=\s*(\{.*?\});", r"window\.__additionalDataLoaded\([^,]+,\s*(\{.*?\})\);", r"\"props\":\s*\{.*?\}"):
        m = re.search(pat, html, re.S)
        if not m: continue
        try:
            chunk = m.group(1) if m.groups() else m.group(0)
            # 尝试修剪到最外层 {}
            head, tail = chunk.find("{"), chunk.rfind("}")
            if head!=-1 and tail!=-1 and head<tail: chunk = chunk[head:tail+1]
            data = json.loads(chunk); 
            if isinstance(data, dict): return data
        except Exception: continue
    return None

def parse_profile(html: str, profile_username: str) -> Tuple[Dict[str, Any], str]:
    """
    解析 Instagram 公共页 HTML，提取：
    username、display_name、bio、email、phone、links、gender、age、region、warning_code、error
    返回 (row, warning_code)
    """
    soup = BeautifulSoup(html, "lxml"); warning: List[str] = []
    # username
    username = profile_username
    # display_name
    display_name = ""
    h1 = soup.find("h1"); 
    if h1: display_name = h1.get_text(strip=True) or display_name
    if not display_name:
        og = soup.find("meta", property="og:title")
        if og and og.get("content"): display_name = og["content"].split("•")[0].strip()
    # bio：挑可见较长段落作为候选
    bio = ""
    candidates = [p.get_text(" ", strip=True) for p in soup.select("header ~ div p, header p, section p")]
    if candidates: bio = max(candidates, key=len)[:500]
    if not bio:
        # 兜底：全局 p 文本中取最长的一段（适配极简页面）
        all_ps = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
        if all_ps: bio = max(all_ps, key=len)[:500]
    # 外链：去掉站内与 instagram 链接
    links: List[str] = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/") or "instagram.com" in href: continue
        links.append(href)
    links += LINK_RE.findall(bio or ""); links = sorted(set(links))
    # email、phone 从 bio 启发式提取
    email_match = EMAIL_RE.search(bio or ""); email = email_match.group(0) if email_match else ""
    phone_match = PHONE_RE.search(bio or ""); phone = phone_match.group(0) if phone_match else ""
    # 性别/年龄/地区：低置信度启发式
    gender = ""
    if re.search(r"\b(she|her|he|him|they|them)\b", (bio or "").lower()): gender="unspecified-pronouns"; warning.append("low_conf_gender")
    age = ""
    m_age = re.search(r"\b(1[6-9]|[2-9]\d)\b\s*(?:y/o|years?\s*old)", (bio or "").lower())
    if m_age: age = m_age.group(1); warning.append("low_conf_age")
    region = ""
    m_region = re.search(r"(USA|UK|Canada|Australia|China|India|Singapore|Hong Kong|NYC|LA|London|Beijing|Shanghai)", bio or "", re.I)
    if m_region: region = m_region.group(1)
    # 结构化 JSON 辅助填充
    js = extract_structured_json(html)
    if isinstance(js, dict):
        display_name = display_name or js.get("name","") or ""
        if not links:
            u = js.get("url")
            if isinstance(u, str): links=[u]
    warning_code = ";".join(sorted(set(warning))) if warning else ""
    row: Dict[str, Any] = {"username":username,"display_name":display_name,"bio":bio,"email":email,"phone":phone,"links":",".join(links),"gender":gender,"age":age,"region":region,"warning_code":warning_code,"error":""}
    return row, warning_code
