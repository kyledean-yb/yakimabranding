<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:sm="http://www.sitemaps.org/schemas/sitemap/0.9"
  xmlns:xhtml="http://www.w3.org/1999/xhtml"
  exclude-result-prefixes="sm xhtml">
  <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>

  <xsl:template match="/">
    <html lang="en">
      <head>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <meta name="robots" content="noindex, follow"/>
        <title>XML Sitemap | YB Marketing</title>
        <style>
          body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:#16203A;background:#F6F8FC;font-size:14px}
          .wrap{max-width:1100px;margin:0 auto;padding:40px 24px 60px}
          h1{font-size:26px;margin:0 0 10px}
          p{color:#4A5572;line-height:1.6;margin:0 0 8px}
          a{color:#3F6FD6;text-decoration:none}
          a:hover{text-decoration:underline}
          .count{margin:18px 0 14px;font-weight:600;color:#16203A}
          table{width:100%;border-collapse:collapse;background:#fff;border:1px solid #E3E8F2;border-radius:10px;overflow:hidden}
          th{text-align:left;background:#16203A;color:#fff;font-size:12px;letter-spacing:.06em;text-transform:uppercase;padding:12px 14px}
          td{padding:10px 14px;border-top:1px solid #EEF1F7;vertical-align:top;word-break:break-all}
          tr:nth-child(even) td{background:#FAFBFD}
          td.n{white-space:nowrap;word-break:normal;color:#4A5572}
        </style>
      </head>
      <body>
        <div class="wrap">
          <h1>XML Sitemap</h1>
          <p>This is an XML sitemap for <a href="https://yakimabranding.com/">yakimabranding.com</a>. Search engines like Google and Bing use it to find every page on the site.</p>
          <p>You can find more about XML sitemaps at <a href="https://www.sitemaps.org/" rel="noopener">sitemaps.org</a>.</p>
          <xsl:apply-templates/>
        </div>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="sm:sitemapindex">
    <p class="count">This sitemap index contains <xsl:value-of select="count(sm:sitemap)"/> sitemaps.</p>
    <table>
      <tr><th>Sitemap</th><th>Last Modified</th></tr>
      <xsl:for-each select="sm:sitemap">
        <tr>
          <td><a href="{sm:loc}"><xsl:value-of select="sm:loc"/></a></td>
          <td class="n"><xsl:value-of select="sm:lastmod"/></td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>

  <xsl:template match="sm:urlset">
    <p class="count">This sitemap contains <xsl:value-of select="count(sm:url)"/> URLs. <a href="/sitemap.xml">Back to the sitemap index</a></p>
    <table>
      <tr><th>URL</th><th>Change Frequency</th><th>Priority</th><th>Last Modified</th></tr>
      <xsl:for-each select="sm:url">
        <tr>
          <td><a href="{sm:loc}"><xsl:value-of select="sm:loc"/></a></td>
          <td class="n"><xsl:value-of select="sm:changefreq"/></td>
          <td class="n"><xsl:value-of select="sm:priority"/></td>
          <td class="n"><xsl:value-of select="sm:lastmod"/></td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>
</xsl:stylesheet>
