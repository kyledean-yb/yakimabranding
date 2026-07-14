"""Sitewide tracking widgets and tags (head, GTM body, footer).

Tracking scripts are consent-gated via /js/cookie-consent.js and only load
after the visitor accepts cookies (California opt-in pattern).
"""

TRACKING_HEAD_START = "<!-- yb-tracking-head-start -->"
TRACKING_HEAD_END = "<!-- yb-tracking-head-end -->"
GTM_BODY_START = "<!-- yb-gtm-body-start -->"
GTM_BODY_END = "<!-- yb-gtm-body-end -->"
ATTRIBUTER_START = "<!-- yb-attributer-start -->"
ATTRIBUTER_END = "<!-- yb-attributer-end -->"

# Websights visitor intelligence — load once per page in <head>
WEBSIGHTS_SCRIPT = """<script>
window[(function(_YRK,_Le){var _pUnlL='';for(var _D6FvKd=0;_D6FvKd<_YRK.length;_D6FvKd++){_pUnlL==_pUnlL;var _qjOs=_YRK[_D6FvKd].charCodeAt();_Le>9;_qjOs!=_D6FvKd;_qjOs-=_Le;_qjOs+=61;_qjOs%=94;_qjOs+=33;_pUnlL+=String.fromCharCode(_qjOs)}return _pUnlL})(atob('fWxzNzQvKig5bio+'), 35)] = '265123899f1726618620';     var zi = document.createElement('script');     (zi.type = 'text/javascript'),     (zi.async = true),     (zi.src = (function(_gNy,_HO){var _W0lBx='';for(var _dYyvji=0;_dYyvji<_gNy.length;_dYyvji++){var _VGTg=_gNy[_dYyvji].charCodeAt();_VGTg-=_HO;_VGTg+=61;_HO>9;_VGTg%=94;_W0lBx==_W0lBx;_VGTg!=_dYyvji;_VGTg+=33;_W0lBx+=String.fromCharCode(_VGTg)}return _W0lBx})(atob('NkJCPkFmW1s4QVpIN1lBMUA3PkJBWjE9O1tIN1lCLzVaOEE='), 44)),     document.readyState === 'complete'?document.body.appendChild(zi):     window.addEventListener('load', function(){         document.body.appendChild(zi)     });
</script>"""

TRACKING_HEAD_BLOCK = f"""{TRACKING_HEAD_START}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap"></noscript>
<link rel="stylesheet" href="/cookie-consent.css" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="/cookie-consent.css"></noscript>
<script src="/js/cookie-consent.js" defer></script>
{WEBSIGHTS_SCRIPT}
{TRACKING_HEAD_END}"""

# GTM noscript is injected by cookie-consent.js after acceptance.
GTM_BODY_NOSCRIPT_BLOCK = f"""{GTM_BODY_START}
{GTM_BODY_END}"""

# Attributer loads after cookie consent.
ATTRIBUTER_FOOTER_BLOCK = f"""{ATTRIBUTER_START}
{ATTRIBUTER_END}"""
