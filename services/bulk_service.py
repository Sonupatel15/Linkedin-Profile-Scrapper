from services.profile_service import get_or_refresh_profile

def fetch_profiles_from_urls(url_list, freshness_days):
    results = []
    for url in url_list:
        try:
            profile = get_or_refresh_profile(url, freshness_days=freshness_days)
            results.append({
                "url": url,
                "profile": profile,
                "error": None
            })
        except Exception as e:
            results.append({
                "url": url,
                "profile": None,
                "error": str(e)
            })
    return results
