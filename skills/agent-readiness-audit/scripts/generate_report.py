#!/usr/bin/env python3
"""Generate the audit JSON report from environment variables."""
import json, os, sys

def env_int(name, default=0):
    val = (os.environ.get(name, "") or "").strip()
    # Remove any newlines or non-numeric chars
    val = ''.join(c for c in val if c.isdigit())
    return int(val) if val else default

def env_bool(name):
    val = (os.environ.get(name, "") or "").strip()
    return val not in ("", "0", "false", "False")

report = {
    "audit": {
        "domain": os.environ.get("DOMAIN_CLEAN", ""),
        "url": os.environ.get("BASE_URL", ""),
        "timestamp": os.environ.get("TIMESTAMP", ""),
        "overall_score": env_int("OVERALL")
    },
    "scores": {
        "agent_files": {"score": env_int("AGENT_FILES_SCORE"), "max": 10},
        "schema_markup": {"score": env_int("SCHEMA_SCORE"), "max": 10},
        "meta_tags": {"score": env_int("META_SCORE") * 2, "max": 10},
        "content_clarity": {"score": env_int("CONTENT_SCORE"), "max": 10},
        "product_data": {"score": env_int("PRODUCT_SCORE"), "max": 10},
        "competitive": {"score": env_int("COMP_SCORE"), "max": 10},
        "trust_signals": {"score": env_int("TRUST_SCORE"), "max": 10}
    },
    "details": {
        "agent_files": {
            "llms_txt": os.environ.get("LLMS_CODE", ""),
            "products_json": os.environ.get("PJ_CODE", ""),
            "robots_txt": os.environ.get("ROBOTS_CODE", ""),
            "sitemap_xml": os.environ.get("SITEMAP_CODE", "")
        },
        "schema": {
            "jsonld_blocks": env_int("SCHEMA_COUNT"),
            "has_product": env_bool("HAS_PRODUCT"),
            "has_faq": env_bool("HAS_FAQ"),
            "has_local_business": env_bool("HAS_LOCAL"),
            "has_breadcrumb": env_bool("HAS_BREADCRUMB"),
            "has_review": env_bool("HAS_REVIEW")
        },
        "meta": {
            "title": (os.environ.get("TITLE_TAG", "") or "")[:200],
            "description_present": os.environ.get("META_DESC", "") not in ("", "Missing"),
            "og_title_present": os.environ.get("OG_TITLE", "") not in ("", "Missing"),
            "og_image_present": os.environ.get("OG_IMAGE", "") not in ("", "Missing"),
            "canonical_present": os.environ.get("CANONICAL", "") not in ("", "Missing")
        },
        "content": {
            "word_count": env_int("WORD_COUNT"),
            "pricing_visible": env_bool("HAS_PRICING"),
            "phone_visible": env_bool("HAS_PHONE"),
            "location_visible": env_bool("HAS_ADDRESS")
        },
        "product_sample": {
            "has_product_schema": env_bool("PRODUCT_SCHEMA"),
            "has_price": env_bool("HAS_PRICE_SCHEMA"),
            "has_sku": env_bool("HAS_SKU"),
            "has_availability": env_bool("HAS_AVAIL"),
            "has_shipping": env_bool("HAS_SHIPPING"),
            "has_return_policy": env_bool("HAS_RETURN")
        },
        "competitors": json.loads(os.environ.get("COMPETITOR_JSON", "[]")),
        "trust": {
            "review_schema": env_bool("HAS_REVIEWS"),
            "ssl": env_bool("HAS_SSL"),
            "phone_visible": env_bool("HAS_PHONE"),
            "policy_pages": env_bool("HAS_POLICY")
        },
        "raw": {
            "llms_content": (os.environ.get("LLMS_CONTENT", "") or "")[:500],
            "robots_content": (os.environ.get("ROBOTS_CONTENT", "") or "")[:500]
        }
    }
}

json.dump(report, sys.stdout, indent=2)
