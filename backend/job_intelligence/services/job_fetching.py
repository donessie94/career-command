"""Utilities for fetching job posting pages."""

import requests


class JobFetchError(Exception):
    """Raised when a job posting URL cannot be fetched."""


def fetch_job_html(url: str) -> str:
    """Fetch raw HTML from a job posting URL."""
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (compatible; CareerCommand/0.1; "
                    "job-posting-preview)"
                )
            },
            timeout=15,
        )

        response.raise_for_status()

    except requests.exceptions.Timeout as exc:
        raise JobFetchError(
            "The page took too long to respond."
        ) from exc

    except requests.exceptions.HTTPError as exc:
        status_code = exc.response.status_code

        if status_code == 403:
            message = (
                "This site blocked automatic fetching. "
                "Please paste the job description manually."
            )
        elif status_code == 404:
            message = (
                "This job posting page was not found. "
                "Please check the URL or paste the job description manually."
            )
        elif status_code == 429:
            message = (
                "This site rate-limited the request. "
                "Please try again later or paste the job description manually."
            )
        else:
            message = (
                f"Could not fetch this page. HTTP status: {status_code}. "
                "Please paste the job description manually."
            )

        raise JobFetchError(message) from exc

    except requests.exceptions.RequestException as exc:
        raise JobFetchError(
            "Could not fetch this URL. Please paste the job description manually."
        ) from exc

    return response.text