import os, re, uuid
from typing import Optional, List, Dict, Any
from urllib.parse import urlparse, urljoin, parse_qs

import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="만덕 Shopping AI Studio v2 API", version="3.1-coupang-fallback")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Project(BaseModel):
    id: Optional[str] = ""
    name: Optional[str] = ""
    url: Optional[str] = ""
    productName: Optional[str] = ""
    price: Optional[str] = ""
    target: Optional[str] = ""
    pros: Optional[str] = ""
    reviews: Optional[str] = ""
    style: Optional[str] = "조회수형"
    duration: Optional[str] = "30초"
    script: Optional[str] = ""
    scenes: Optional[List[Dict[str, Any]]] = []
    titles: Optional[List[str]] = []
    hashtags: Optional[List[str]] = []

def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()

def lines(text: str) -> List[str]:
    return [x.strip() for x in (text or "").replace(",", "\n").split("\n") if x.strip()]

def job(t, title, payload):
    return {"id": str(uuid.uuid4()), "type": t, "title": title, "status": "queued", "payload": payload}

def meta(soup, *names):
    for name in names:
        tag = soup.find("meta", attrs={"property": name}) or soup.find("meta", attrs={"name": name})
        if tag and tag.get("content"):
            return clean(tag.get("content"))
    return ""

def price_from_text(text):
    patterns = [
        r"([0-9]{1,3}(?:,[0-9]{3})+)\s*원",
        r"₩\s*([0-9]{1,3}(?:,[0-9]{3})+)",
    ]
    for pattern in patterns:
        m = re.search(pattern, text)
        if m:
            return f"{m.group(1)}원"
    return ""

def guess_name(title):
    title = clean(title)
    for sep in [" - 쿠팡!", " | 쿠팡", " : 네이버", " - 네이버", " | 스마트스토어", " | Apple", " - 11번가"]:
        if sep in title:
            title = title.split(sep)[0]
    return title[:90]

def is_coupang_url(url: str) -> bool:
    host = urlparse(url).netloc.lower()
    return "coupang.com" in host or "link.coupang.com" in host

def coupang_fallback(url: str, reason: str = "") -> Dict[str, Any]:
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)

    product_id = ""
    m = re.search(r"/vp/products/(\d+)", parsed.path)
    if m:
        product_id = m.group(1)

    item_id = (qs.get("itemId") or [""])[0]
    vendor_item_id = (qs.get("vendorItemId") or [""])[0]

    hints = []
    if product_id:
        hints.append(f"상품번호: {product_id}")
    if item_id:
        hints.append(f"옵션번호: {item_id}")
    if vendor_item_id:
        hints.append(f"판매자옵션번호: {vendor_item_id}")

    return {
        "ok": True,
        "mode": "manual_fallback",
        "isCoupang": True,
        "message": "쿠팡은 자동 수집이 차단될 수 있어 수동 보정 모드로 전환했어요.",
        "reason": reason or "쿠팡 페이지 접근 제한 또는 메타정보 부족",
        "productName": "",
        "price": "",
        "pros": "\n".join([
            "쿠팡 상품 URL이 감지되었습니다.",
            "쿠팡은 자동 분석이 막힐 수 있어 상품명/가격을 직접 입력하면 바로 AI 제작을 계속할 수 있습니다.",
            *hints
        ]),
        "reviews": "",
        "imageUrl": "",
        "domain": parsed.netloc,
        "finalUrl": url,
        "manualRequired": True,
        "coupangMeta": {
            "productId": product_id,
            "itemId": item_id,
            "vendorItemId": vendor_item_id,
        }
    }

async def fetch_html(url):
    if not url.startswith(("http://", "https://")):
        return {"ok": False, "message": "http 또는 https URL만 가능합니다."}

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }

    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True, headers=headers) as client:
            r = await client.get(url)
            if r.status_code >= 400:
                return {"ok": False, "message": f"HTTP {r.status_code} 오류"}
            content_type = r.headers.get("content-type", "")
            if "text/html" not in content_type and "application/xhtml" not in content_type:
                return {"ok": False, "message": f"HTML 페이지가 아닙니다: {content_type}"}
            return {"ok": True, "html": r.text, "finalUrl": str(r.url)}
    except Exception as e:
        return {"ok": False, "message": f"URL 요청 실패: {e}"}

def parse_html(html, final_url):
    soup = BeautifulSoup(html, "lxml")
    title = clean(soup.title.get_text(" ")) if soup.title else ""
    og_title = meta(soup, "og:title", "twitter:title")
    desc = meta(soup, "og:description", "description", "twitter:description")
    image = meta(soup, "og:image", "twitter:image")
    text = clean(soup.get_text(" "))

    product_name = guess_name(og_title or title)
    price = price_from_text(text)

    # 쿠팡 차단/빈 정보 감지
    if is_coupang_url(final_url):
        lower_text = text.lower()
        blocked_words = ["robot", "captcha", "access denied", "자동입력", "비정상적인"]
        if not product_name or any(w in lower_text for w in blocked_words):
            return coupang_fallback(final_url, "쿠팡 페이지가 봇 차단 또는 빈 페이지를 반환했습니다.")

    return {
        "ok": True,
        "mode": "auto",
        "message": "URL 분석 완료",
        "productName": product_name,
        "price": price,
        "pros": "\n".join([x for x in [desc[:180], "페이지 메타정보 기반으로 분석했습니다."] if x]),
        "imageUrl": urljoin(final_url, image) if image else "",
        "domain": urlparse(final_url).netloc,
        "finalUrl": final_url,
        "manualRequired": False,
    }

def build_package(p: Project):
    product = p.productName or "이 상품"
    target = p.target or "이 상품이 필요한 사람"
    price = p.price or "가격 확인 필요"
    pros = lines(p.pros)
    reviews = lines(p.reviews)
    p1 = pros[0] if len(pros) > 0 else "사용이 간편합니다"
    p2 = pros[1] if len(pros) > 1 else "가격 대비 만족도가 좋습니다"
    p3 = pros[2] if len(pros) > 2 else "일상에서 바로 체감됩니다"
    r1 = reviews[0] if reviews else "실사용 만족도가 높다는 후기가 많습니다"

    hook = {
        "광고형": f"요즘 {target} 사이에서 반응 좋은 제품입니다.",
        "정보형": f"{target}이라면 구매 전 이 포인트는 꼭 확인하세요.",
        "리뷰형": f"후기에서 자주 보이는 {product}의 진짜 포인트입니다.",
    }.get(p.style, f"딱 {target}이라면 이거 그냥 지나치면 손해입니다.")

    script = f"""{hook}

오늘 소개할 제품은 "{product}"입니다.

첫 번째, {p1}.
두 번째, {p2}.
세 번째, {p3}.

실제 후기에서는 "{r1}" 같은 반응이 보입니다.

가격/혜택은 {price}.
필요했다면 저장해두고 비교해보세요.

이런 상품 더 보고 싶으면 팔로우하세요."""

    base_scenes = [
        ("0~2초","강한 훅",f"{target}이라면 꼭 보세요","fast zoom-in, premium product reveal"),
        ("2~5초","문제 공감","이런 불편함 있었죠?","show pain point, lifestyle shot"),
        ("5~8초","상품 등장",product,"hero product shot, slow push-in"),
        ("8~13초","장점 1",p1,"demonstrate main benefit clearly"),
        ("13~18초","장점 2",p2,"quick before-after commercial cut"),
        ("18~23초","후기 신뢰",r1,"review cards floating, trust motion"),
        ("23~27초","가격/혜택",price,"deal highlight, shopping UI motion"),
        ("27~30초","CTA","저장하고 나중에 비교하세요","clean ending, save and follow motion"),
    ]

    scenes = []
    for i, (time, title, caption, motion) in enumerate(base_scenes, 1):
        scenes.append({
            "id": i,
            "time": time,
            "title": title,
            "caption": caption,
            "imagePrompt": f"{product}, {title}, {caption}, realistic, cinematic, detailed, vertical 9:16, no text",
            "videoPrompt": motion,
        })

    titles = [
        f"{target}이 좋아할 만한 {product}",
        f"{product}, 이 포인트는 꼭 확인하세요",
        f"요즘 반응 좋은 {product} 추천",
        f"{product} 사기 전 보면 좋은 영상",
        f"저장해둘 만한 {product}",
    ]

    hashtags = [
        "#상품추천", "#쇼핑추천", "#가성비템", "#인스타릴스", "#유튜브쇼츠",
        "#AI쇼츠", "#제품추천", "#리뷰템", "#생활템", f"#{product.replace(' ', '')}"
    ]

    analysis = {
        "features": [
            f"{product}은 {target}에게 문제 해결형으로 보여주기 좋습니다.",
            f"가격/혜택 포인트: {price}",
            f"핵심 장점 1: {p1}",
            f"핵심 장점 2: {p2}",
            f"핵심 장점 3: {p3}",
            "첫 2초에는 문제 해결 문구가 가장 좋습니다.",
            "중반에는 실사용 장면과 후기 신뢰를 넣는 것이 좋습니다.",
            "마지막에는 저장/비교 CTA가 적합합니다.",
            "썸네일은 질문형/궁금증형 문구가 좋습니다.",
            "영상은 빠른 컷 전환과 제품 클로즈업이 어울립니다.",
        ],
        "target": target,
        "sellingPoints": [p1, p2, p3, "후기 신뢰", "가격/혜택"],
        "hooks": [
            f"{target}이라면 이거 그냥 지나치면 손해",
            "이거 하나로 은근 귀찮은 문제가 해결됩니다",
            "사기 전에 이 포인트만 확인하세요",
            "후기에서 자주 보이는 장점은 이겁니다",
            "저장해두고 나중에 비교하세요",
        ],
    }

    return {
        "productName": product,
        "analysis": analysis,
        "script": script,
        "scenes": scenes,
        "captions": "\n".join([f"{s['time']} {s['caption']}" for s in scenes]),
        "titles": titles,
        "hashtags": hashtags,
        "thumbnailTexts": ["이거 왜 이제 알았지?", "사기 전 꼭 보세요", "후기 많은 이유", "저장하고 비교하세요"],
        "imagePrompts": [s["imagePrompt"] for s in scenes],
        "videoPrompts": [s["videoPrompt"] for s in scenes],
        "ttsGuide": f"{p.duration or '30초'} 분량, 빠른 템포, 또렷한 발음",
    }

@app.get("/")
def root():
    return {"name": "만덕 Shopping AI Studio API", "version": "3.1-coupang-fallback", "status": "running"}

@app.get("/api/health")
def health():
    return {
        "ok": True,
        "openai": bool(os.getenv("OPENAI_API_KEY")),
        "image": bool(os.getenv("IMAGE_API_KEY")),
        "video": bool(os.getenv("VIDEO_API_KEY")),
        "tts": bool(os.getenv("TTS_API_KEY")),
    }

@app.post("/api/product/analyze-url")
async def analyze_url(p: Project):
    url = (p.url or "").strip()
    if not url:
        return {"ok": False, "message": "URL을 먼저 입력해주세요."}

    # 쿠팡은 실패해도 수동 보정 모드로 계속 진행
    coupang = is_coupang_url(url)
    data = await fetch_html(url)

    if not data["ok"]:
        if coupang:
            return coupang_fallback(url, data.get("message", "쿠팡 접근 실패"))
        return data

    parsed = parse_html(data["html"], data["finalUrl"])

    # 쿠팡인데 분석값이 너무 약하면 수동보정
    if coupang and not parsed.get("productName"):
        return coupang_fallback(url, "쿠팡 상품명을 자동 추출하지 못했습니다.")

    return parsed

@app.post("/api/ai/generate-package")
def generate_package(p: Project):
    return build_package(p)

@app.post("/api/team/run")
def run_team(p: Project):
    pack = build_package(p)
    team = [
        {"role":"팀장 AI","status":"완료","result":"전체 제작 방향을 쇼핑 릴스형으로 설정했습니다."},
        {"role":"상품조사 AI","status":"완료","result":f"{pack['productName']} 상품 정보를 분석했습니다."},
        {"role":"대본 AI","status":"완료","result":"30초 쇼츠 대본과 훅을 생성했습니다."},
        {"role":"이미지 AI","status":"완료","result":"장면별 이미지 프롬프트 8개를 준비했습니다."},
        {"role":"영상 AI","status":"완료","result":"장면별 영상 모션 프롬프트 8개를 준비했습니다."},
        {"role":"음성 AI","status":"완료","result":"TTS 가이드와 나레이션 대본을 준비했습니다."},
        {"role":"업로드 AI","status":"완료","result":"유튜브/인스타/틱톡 업로드 문구를 준비했습니다."},
    ]
    return {"ok": True, "team": team}

@app.post("/api/jobs/create-all")
def create_jobs(p: Project):
    pack = build_package(p)
    jobs = []
    for i, s in enumerate(pack["scenes"], 1):
        jobs.append(job("image", f"이미지 {i}", {"prompt": s["imagePrompt"]}))
        jobs.append(job("video", f"영상 {i}", {"prompt": s["videoPrompt"]}))
    jobs.append(job("tts", "나레이션", {"script": pack["script"]}))
    jobs.append(job("mp4", "최종 MP4 렌더링", {"ratio": "9:16", "scenes": pack["scenes"]}))
    return {"ok": True, "jobs": jobs}

@app.post("/api/export/upload-plan")
def upload_plan(p: Project):
    pack = build_package(p)
    return {
        "ok": True,
        "plan": {
            "youtube": {"title": pack["titles"][0], "description": pack["script"][:300] + "\n\n" + " ".join(pack["hashtags"])},
            "instagram": {"caption": pack["titles"][1] + "\n\n" + " ".join(pack["hashtags"])},
            "tiktok": {"caption": pack["titles"][2] + "\n" + " ".join(pack["hashtags"][:6])},
        }
    }
