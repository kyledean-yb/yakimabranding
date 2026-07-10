"""Production SEO controls for generated pages.

Thank-you confirmation pages stay noindex (thin/duplicate content).
All other pages are indexable.
"""

# Empty for public content pages (indexable by default).
STAGING_ROBOTS_META = ""

# Keep confirmation pages out of search results.
THANK_YOU_ROBOTS_META = '<meta name="robots" content="noindex, nofollow">'
