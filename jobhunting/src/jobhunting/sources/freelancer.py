"""Freelancer.com — 自由职业项目（接单）

官方公开 API，无需登录（文档: developers.freelancer.com）：
  GET https://www.freelancer.com/api/projects/0.1/projects/active/
      ?query=<keyword>&limit=N&compact=true
返回 result.projects[]，每项含：
  id / title / seo_url / preview_description / type(fixed|hourly)
  budget{minimum,maximum} / submitdate(unix 秒)
项目页 URL: https://www.freelancer.com/projects/<seo_url>
"""
from __future__ import annotations

import time
from typing import Any

import httpx

from .base import JobSource
from ..log import setup_logging

logger = setup_logging()


class FreelancerSource(JobSource):
    """Freelancer.com 在竞项目（官方 API）"""

    name = "freelancer"
    source_type = "api"
    BASE_URL = "https://www.freelancer.com/api/projects/0.1/projects/active/"

    def fetch(self) -> list[dict[str, Any]]:
        keywords = self.config.get("keywords", [])
        excludes = [e.lower() for e in self.config.get("exclude_keywords", [])]
        per_query = int(self.config.get("per_query", 20))
        max_results = int(self.config.get("max_results", 60))
        all_jobs: dict[str, dict[str, Any]] = {}
        for kw in keywords:
            try:
                resp = httpx.get(
                    self.BASE_URL,
                    params={"query": kw, "limit": per_query, "compact": "true"},
                    timeout=20.0,
                    headers={"User-Agent": "jobhunting-agent/0.1"},
                )
                resp.raise_for_status()
                projects = (resp.json().get("result") or {}).get("projects") or []
                for p in projects:
                    pid = str(p.get("id", ""))
                    blob = f"{p.get('title', '')} {p.get('preview_description', '')}".lower()
                    if not pid or any(x in blob for x in excludes):
                        continue
                    all_jobs.setdefault(pid, p)
            except Exception as exc:  # noqa: BLE001
                logger.warning("[freelancer] 关键词 %r 抓取失败: %s", kw, exc)
        jobs = list(all_jobs.values())
        return jobs[:max_results] if max_results else jobs

    def normalize(self, raw: dict[str, Any]) -> dict[str, Any]:
        ptype = raw.get("type", "fixed")
        budget = raw.get("budget") or {}
        lo, hi = budget.get("minimum"), budget.get("maximum")
        if lo is not None and hi is not None:
            unit = "/hr" if ptype == "hourly" else ""
            salary = f"${lo:g} - ${hi:g}{unit}"
        else:
            salary = ""
        posted = raw.get("submitdate")
        return {
            "id": f"fl-{raw.get('id', '')}",
            "title": raw.get("title", ""),
            "company": "Freelancer.com 客户",
            "url": f"https://www.freelancer.com/projects/{raw.get('seo_url', '')}",
            "description": raw.get("preview_description", ""),
            "tags": [ptype, "gig"],
            "location": "Remote",
            "salary": salary,
            "job_type": "contract",
            "posted_at": time.strftime("%Y-%m-%d", time.gmtime(posted)) if posted else "",
        }
