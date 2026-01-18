from fastapi import APIRouter

router = APIRouter()

@router.get("/.well-known/appspecific/com.chrome.devtools.json", include_in_schema=False)
async def chrome_devtools_probe():
    # Return empty JSON with 200 to satisfy Chrome DevTools probe
    return {}
