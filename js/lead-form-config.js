/**
 * YB Marketing lead form → GoHighLevel webhook config.
 *
 * Same inbound webhook as BlueSoft; leads are distinguished by site, source,
 * page_url, and page_path in the JSON payload.
 */
window.YB_LEAD_FORM = window.YB_LEAD_FORM || {
  webhookUrl:
    'https://services.leadconnectorhq.com/hooks/0Pc2NnJAQkzYB3hhPi1b/webhook-trigger/1865a2f2-d6f5-48ec-a4a7-4d68fb92f329',
  site: 'YB Marketing',
  siteDomain: 'yakimabranding.com',
};
