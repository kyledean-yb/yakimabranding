"""Case study copy — sourced from client Word documents."""

CASE_STUDIES = [
    {
        "slug": "fortune-500-multilingual-accessibility",
        "title": "A Fortune 500 Accessibility Audit Identified the Issues. Implementing Them Across Six Languages Was the Real Work.",
        "metaTitle": "Fortune 500 Multilingual Accessibility Remediation — YB Marketing",
        "hubTag": "Accessibility · Enterprise",
        "hubExcerpt": "Three domains, six languages — from audit inventory to shipped WCAG conformance without breaking brand or translations.",
        "metaDescription": "How YB Marketing turned a Fortune 500 accessibility audit into shipped fixes across three domains and six languages — React, brand tokens, and translation pipeline included.",
        "accent": "#2BC4F0",
        "accentWash": "var(--wash-cyan)",
        "hubPills": ["6 languages", "3 domains", "Multi-month"],
        "meta": [
            {"label": "Client", "value": "A Fortune 500 enterprise (anonymised)"},
            {"label": "Scope", "value": "Three domains, multilingual"},
            {
                "label": "Languages in scope",
                "value": "English, German, Simplified Chinese, Traditional Chinese, Japanese, Korean",
                "tags": ["English", "German", "Simplified Chinese", "Traditional Chinese", "Japanese", "Korean"],
            },
            {"label": "Environments", "value": "Development, staging, and production"},
            {"label": "Timeline", "value": "Multi-month engagement"},
            {
                "label": "Result",
                "value": "Conformance achieved across all three domains and six languages with no regression to brand or translations",
                "highlight": True,
            },
        ],
        "summary": [
            "A Fortune 500 enterprise had commissioned a third-party accessibility audit across their global web presence. Three domains, each published in six languages. The audit returned a thorough inventory of issues. It did not return a way to fix them without affecting brand consistency, translation coverage, or the working experience of the live sites.",
            "That gap was where the project lived. The audit said what was wrong. Remediation was the body of work that had to take those findings and ship them into production cleanly, across three domains and six locales, with each fix verified in every language before it went live.",
            "Over a few months we took the audit from report to implementation. Three domains, six languages, conformant at the end of it, with the brand intact.",
        ],
        "sections": [
            {
                "heading": "The Situation",
                "paragraphs": [
                    "The client owned three domains: a primary corporate site and two supporting properties serving distinct business functions. Each was published in six languages. The audit had been performed against all three.",
                    "The findings spanned the surface area you would expect at this scale: contrast failures inside brand-owned colour tokens, interactive components without keyboard or screen reader support, forms with missing programmatic labels and silent error states, carousels that played without controls, video without captions, and a long list of third-party embeds (PDFs, maps, and other inserted content) that arrived on the page without any accessibility scaffolding around them.",
                    "None of the individual issues were exotic. What made the remediation work substantial was the combination they sat inside. A Fortune 500 web presence with brand tokens that could not be casually edited. Three connected domains. Six language versions of every fix. And a meaningful portion of the interactive surface rendered through React components.",
                ],
            },
            {
                "heading": "Why Remediation Was the Hard Part",
                "paragraphs": [
                    "An audit is a static document. Remediation is the part that has to ship. On a multilingual estate with this kind of reach, that distinction matters.",
                ],
                "subsections": [
                    {
                        "heading": "Brand-owned colour and contrast tokens",
                        "paragraphs": [
                            "Several contrast failures sat inside colour tokens that were part of the client's global brand system. We could not unilaterally darken a brand colour. Each contrast adjustment had to be resolved at the usage layer (changing the background a token sat on, increasing font weight, switching to a different approved token, adjusting state colours for links, buttons, and focus) or escalated to the brand owners for an approved tonal variant.",
                            "This part of the work was as much coordination as code. Each proposed change went through brand review before reaching the staging environment.",
                        ],
                    },
                    {
                        "heading": "React-rendered interactive components",
                        "paragraphs": [
                            "The most demanding piece of the remediation was the interactive layer rendered through React. These components had been built for visual behaviour first and accessibility second. Roles were missing or wrong, state changes were not announced, focus was lost on re-render, and keyboard interaction worked partially or not at all depending on which sub-component was active.",
                            "Each component needed a real rebuild of its accessibility model. Roles, names, and states declared correctly. Focus surviving re-renders and routing back to a sensible place when modals, drawers, and overlays closed. State changes that mattered to a screen reader user (selections, expansions, errors, loading) announced through live regions without flooding them. None of this could be applied uniformly across components because each one had its own state model.",
                        ],
                    },
                    {
                        "heading": "Dropdowns, forms, and error states",
                        "paragraphs": [
                            "Forms across all three domains relied on a mix of native and custom dropdown controls. Native selects worked. The custom dropdowns, the styled ones the design system preferred, were the ones flagged by the audit. They needed correct roles, keyboard operation, programmatic state, and accessible names that flowed through the translation pipeline.",
                            "The error-state work was equally material. Failing fields needed programmatic association between the error message and the input, the message itself had to be announced when it appeared, and required-field status had to be exposed correctly rather than left as a visual asterisk. Each fix was translated and verified across all six locales.",
                        ],
                    },
                    {
                        "heading": "Carousels and slideshows",
                        "paragraphs": [
                            "The carousels on the site autoplayed, did not expose a pause control to assistive technology, did not handle keyboard navigation cleanly, and lost focus when slides changed. Each of these is an individual fix in isolation. Together, they meant the carousel components had to be re-architected, not just patched. Pause and play controls exposed properly. Slide changes announced where it mattered. Focus managed when users interacted with controls. Reduced-motion preferences respected.",
                        ],
                    },
                    {
                        "heading": "Embedded content: video, PDFs, and maps",
                        "paragraphs": [
                            "A meaningful portion of the page content was not owned by the client's sites at all. Videos were embedded from external players. PDFs were either linked or embedded inside iframes. Maps were embedded from a third-party provider. The source documents could not be edited as part of the engagement.",
                            "What could be fixed was the embedding itself. Videos were configured to load with captions available and player controls exposed to assistive technology. PDF links and embeds were rewritten so the purpose, file type, and behaviour were clear to a screen reader user before the link was activated, with proper iframe titles where PDFs were displayed inline. Map embeds received accessible names, were taken out of the keyboard tab order where they trapped focus, and were paired with text-based alternatives (address, directions, contact) so the underlying information was reachable without the map widget itself being usable.",
                        ],
                    },
                    {
                        "heading": "Images across six languages",
                        "paragraphs": [
                            "Alt text gaps were spread across the asset library, and they were not symmetrical between language versions. Some images had alt text in English and nothing in the other five locales. Others were decorative on some pages and meaningful on others. Closing this required a per-locale pass, not a single global change.",
                        ],
                    },
                    {
                        "heading": "Six language versions of every fix",
                        "paragraphs": [
                            "Every accessible name, helper text string, error message, and announcement we introduced during the project had to exist in all six languages. Hardcoded English strings were not an option. Each new label and message was routed through the translation pipeline, registered in the site's translation memory, and verified in every locale before the fix was considered shipped.",
                        ],
                    },
                    {
                        "heading": "Working across development, staging, and production",
                        "paragraphs": [
                            "The team had a development environment, a staging environment, and production. Each change moved through that pipeline before reaching live users, which removed the risk of shipping a broken fix into a Fortune 500 web presence directly. What it did not remove was the locale multiplication. A fix that passed verification in English on staging still had to be checked in German, where compound words ran longer and could wrap where they did not in English, and in each of the other four locales. Promotion to production was paced so that no business unit was caught out by a layout shift in their language.",
                        ],
                    },
                ],
            },
            {
                "heading": "The Gap Between the Audit and the Work",
                "paragraphs": [
                    "The audit document listed issues. It did not say, for each issue, which of the three domains it appeared on, which of the six languages it affected, which component generated it, or what the downstream consequences of fixing it would be. Building that mapping was the first piece of real work.",
                    "Some audit findings, written generically, turned out to be a single shared component used in dozens of places. Fixing the component fixed every instance. Other findings, written as a single issue, were actually six instances (one per language) because the translated DOM diverged from the source in ways the audit had not captured. The audit's count of issues and the count of actual fixes did not match in either direction.",
                    "We rebuilt the issue list as a remediation plan organised by template, component, embed type, and locale. Fixes that could be made at the code layer were separated from those that required translation work, brand approval, or third-party embed configuration. That plan was what the rest of the engagement worked from.",
                ],
            },
            {
                "heading": "What We Did",
                "paragraphs": [
                    "The work moved in tracks that ran in parallel where they could and serialised where they could not. Each track was scoped, executed, verified across all six locales on staging, and promoted to production before the next batch began.",
                ],
                "subsections": [
                    {"heading": "Colour and contrast adjustments", "paragraphs": ["Contrast failures were resolved through usage-layer changes wherever possible, and through brand-approved tonal variants where a token itself had to change. Focus, hover, disabled, and error states across links, buttons, and form fields were brought up to conformance, with the brand team signing off on each change before it shipped."]},
                    {"heading": "React component rebuilds", "paragraphs": ["The interactive components rendered through React were the most concentrated body of work. Each component received a proper accessibility model: roles, accessible names, states, keyboard operation, focus management on mount and unmount, and announcements for the state changes that mattered to a screen reader user. Components were tested both in isolation and inside the pages that used them."]},
                    {"heading": "Forms and dropdowns", "paragraphs": ["Forms across all three domains were rebuilt to associate labels programmatically with their inputs, expose required-field status correctly, announce errors when they appeared, and provide error text that screen readers could associate with the failing field. Custom dropdowns received correct roles, keyboard handling, and accessible names. Native dropdowns were left in place where they already worked."]},
                    {"heading": "Carousels and slideshows", "paragraphs": ["Carousel components were re-architected to expose pause and play controls, support keyboard navigation, manage focus when slides changed, and respect reduced-motion preferences. Autoplay behaviour was reviewed against the requirement that users have meaningful control over moving content."]},
                    {"heading": "Video accessibility", "paragraphs": ["Embedded video was configured to load with captions available and player controls exposed to assistive technology. Where videos were used to convey information not available elsewhere on the page, the embedding was paired with a textual fallback."]},
                    {"heading": "PDF, map, and other embed remediation", "paragraphs": ["PDFs were not edited at the source. What changed was the way they were referenced from the sites: link text describing the document and its file type, iframe titles where PDFs were embedded inline, and clear indication of behaviour before the link was activated. Map embeds received accessible names, were prevented from trapping keyboard focus, and were paired with text-based alternatives so the underlying information was reachable without the map widget."]},
                    {"heading": "Image and alt text coverage", "paragraphs": ["The asset library was reviewed per locale. Missing alt text was added in each language, decorative images were marked correctly, and image variants that differed between language versions received translated alt text rather than a default fallback."]},
                    {"heading": "Translation pipeline updates", "paragraphs": ["Every new accessible name, helper text, and announcement introduced during remediation was translated into all six languages and registered in the site's translation memory. Nothing was left as a hardcoded English string. The pipeline was extended so future content and feature work would inherit the same coverage."]},
                    {"heading": "Cross-locale verification", "paragraphs": ["Every change went through a verification pass on staging in all six languages before being promoted to production. Automated tooling caught the structural failures (contrast, missing attributes, broken hierarchies). Manual testing covered the parts that required judgement: keyboard flow through React components, announcements firing at the right moment, error handling in real forms, and embed behaviour for video, PDFs, and maps."]},
                ],
            },
            {
                "heading": "The Outcome",
                "paragraphs": [
                    "All three domains reached conformance across all six languages within the engagement window. The brand system remained intact. The translation pipeline was extended cleanly to cover the new accessibility surface. No business unit experienced a regression in their language during the rollout.",
                    "The internal documentation produced during the project (the remediation plan, the per-locale verification notes, the component-level guidance) was handed back to the client's web and brand teams so future content and feature work would stay inside the conformance envelope rather than drifting back out of it.",
                ],
            },
            {
                "heading": "What This Means for Multilingual Enterprise Sites",
                "paragraphs": [
                    "If you run a multilingual web estate at enterprise scale, the patterns that made this engagement substantial are likely already present in your environment.",
                ],
                "subsections": [
                    {"heading": "The audit is the start of the work", "paragraphs": ["A WCAG audit identifies issues. It does not tell you which component generates them, which language variants are affected, which fixes require brand approval, or which fixes will ripple through translation. Building that map is its own piece of work and is usually where remediation projects stall."]},
                    {"heading": "Multilingual makes every fix wider", "paragraphs": ["A single accessibility fix on a monolingual site is one change. The same fix on a six-language site can be six changes, each with its own translation, layout, and verification requirements. Scoping accessibility work without accounting for locale multiplication is how timelines slip."]},
                    {"heading": "Custom React components carry most of the work", "paragraphs": ["Custom interactive components rendered through React rarely behave correctly for assistive technology without a deliberate rebuild. Surface patches do not solve focus loss on re-render, missing state announcements, or broken keyboard models. The component has to be reworked, which is a different cost profile to fixing static markup."]},
                    {"heading": "Brand sign-off has to be in scope from the start", "paragraphs": ["Contrast failures often live inside brand-owned colour tokens. Remediation that does not include the brand team in the loop either ships changes the brand will later roll back, or stalls indefinitely waiting for approval that was never requested correctly."]},
                    {"heading": "You can fix the embedding when you cannot fix the source", "paragraphs": ["Videos, PDFs, and maps that arrive on the page from third-party sources often cannot be edited at the source. What can be fixed is the way they are embedded: link text, iframe titles, focus behaviour, and text-based alternatives that put the underlying information within reach of someone who cannot use the widget itself."]},
                    {"heading": "Conformance drifts without ongoing ownership", "paragraphs": ["A site reaches conformance and then drifts out of it the next time a new feature ships, a new template is added, or a new piece of content is published without translation coverage on its accessible names. The handover documentation is what determines whether the work holds."]},
                ],
            },
        ],
        "closingCta": 'Sitting on an accessibility audit you have not yet implemented? <a href="/contact">YB Marketing</a> remediates multilingual enterprise sites at scale, takes audit findings from inventory to shipped conformance, and hands back the documentation your team needs to stay there.',
    },
    {
        "slug": "wordpress-portfolio-malware-remediation",
        "title": "A 130-Site WordPress Portfolio Looked Clean. Google Ads Knew Something Was Wrong.",
        "metaTitle": "130-Site WordPress Malware Remediation — YB Marketing",
        "hubTag": "WordPress · Security",
        "hubExcerpt": "A stealth malware campaign hid from every scanner — until Google Ads suspensions exposed what 130 sites had in common.",
        "metaDescription": "How YB Marketing cleaned a 130-site WordPress portfolio infected with ad-click-only malware, got Google Ads reinstated, and achieved zero reinfections in three months.",
        "accent": "#FF6B57",
        "accentWash": "var(--wash-coral)",
        "hubPills": ["130 sites", "15 days", "Google Ads"],
        "meta": [
            {"label": "Client", "value": "A 130-site WordPress portfolio (anonymised)"},
            {"label": "Hosting", "value": "Flywheel"},
            {"label": "Timeline", "value": "15 days to full remediation"},
            {"label": "Ongoing", "value": "Monthly security review + weekly audit for high-profile sites"},
            {
                "label": "Result",
                "value": "130 sites clean, no reinfections after three months, Google Ads accounts reinstated",
                "highlight": True,
            },
        ],
        "summary": [
            "An agency owner who had just taken over a 130-site WordPress portfolio found their Google Ads accounts getting suspended repeatedly, with no obvious cause. Every site looked clean. Every scanner returned clear results. The infection had been running undetected across all 130 properties, silently redirecting paid ad traffic to rogue domains while evading every automated check.",
            "For the new owner, this was not just a security problem. It was a client-retention problem, a paid-media problem, and a trust problem. Each suspension made them look responsible for a situation they had inherited and could not yet explain. We were brought in to find the cause, clean the portfolio, and make sure it stayed clean.",
            "In 15 days, the full portfolio was cleaned, hardened, and documented for Google Ads review. Three months later, all 130 sites remain stable, with no reinfections and no recurring ad suspensions.",
        ],
        "sections": [
            {
                "heading": "The Situation",
                "paragraphs": [
                    "A client brought us in after taking over a 130-site WordPress portfolio from a previous agency. Every site in the portfolio was running Google Ads. Within weeks of the handover, ad accounts began getting flagged and suspended for policy violations, one after another. For an agency owner trying to establish trust with 130 clients from day one, the timing could not have been worse. The sites loaded perfectly. Traffic patterns looked normal. There were no error messages, no visitor complaints, no server alerts. Yet every single property was compromised. The infection had been running completely undetected.",
                ],
            },
            {
                "heading": "Why Nobody Caught It",
                "paragraphs": ["Most malware announces itself. This one was built to do the opposite."],
                "subsections": [
                    {
                        "heading": "The hidden plugin",
                        "paragraphs": [
                            "The infection came in the form of a PHP plugin with a generic, unremarkable name. It installed itself like any other plugin but used a WordPress filter to remove itself from the admin plugins screen. There was nothing to find in the dashboard. The only way to spot it was through FTP or direct server access. Standard plugin audits, the kind most agencies run, came back clean.",
                            "The delivery server only served actual JavaScript to browsers that arrived with active Google Ads session signals. Security scanners got a blank file. Automated crawlers got a blank file. Anyone opening the script URL in a browser tab got a blank file. Every scan said clean because, to every scan, it was. The only people who saw what the malware was actually doing were the ones clicking through from paid ads.",
                        ],
                    },
                    {
                        "heading": "Hidden admin access",
                        "paragraphs": [
                            "Built into the plugin was a hardcoded backdoor. Passing a specific GET parameter in a URL would immediately log the attacker in as the site's first administrator, with no password, no two-factor prompt, nothing. One request. Full access. This meant the attacker could return to any site at any time, regardless of how many times passwords had been reset.",
                        ],
                    },
                    {
                        "heading": "Unauthorised file writes",
                        "paragraphs": [
                            "The plugin registered a REST API endpoint open to anyone on the internet. No authentication was required. Through this endpoint, an attacker could push arbitrary PHP code directly into theme files on the site. The plugin also actively cleared all major caching plugins after each write, so injected code would be live and serving to real visitors within seconds.",
                        ],
                    },
                    {
                        "heading": "Ad-click-only redirects",
                        "paragraphs": [
                            "On every page load, the plugin made a server-side call to an external server, retrieved a base64-encoded URL, decoded it, and injected a script tag at the very top of the page before any other content was sent to the visitor.",
                            "Every visitor loaded this script on every page. The redirect logic inside it only fired for visitors who had just clicked a Google Ad. Direct visitors, organic traffic, anyone browsing normally saw nothing wrong.",
                            "The destination URL was never stored on the site. It was pulled fresh from the attacker's server on each page load. The delivery domain rotated every day or two. So the cycle ran like this: Google flags a URL and suspends the account, the client moves through reinstatement, the account goes back live, the ads run again, Google flags the new domain, the account is suspended again. The infection kept running through every reinstatement because nobody knew to look for it.",
                            "The <code>data-cfasync='false'</code> attribute on the script tag was not accidental. It instructs Cloudflare's Rocket Loader to leave the script alone, which meant the malicious code ran before any Cloudflare processing could touch it.",
                        ],
                    },
                    {
                        "heading": "Built-in reinfection mechanism",
                        "paragraphs": [
                            "We learned early on that simply deleting the plugin was not enough. The malware had already embedded a reinstaller into wp-cron.php that could recreate a fresh copy of itself under a different directory name. It had also embedded AES-256 encrypted PHP payloads inside files in the theme's /patterns/ directory, files that looked like ordinary template files to anyone browsing the folder. Those payloads would only execute if the attacker passed the right decryption key via URL parameters.",
                            "We cleaned one site and deliberately left it without the additional security layer to see what would happen. It was re-infected within 24 hours. That test shaped everything that followed.",
                        ],
                    },
                ],
            },
            {
                "heading": "Where the Infection Came From",
                "paragraphs": [
                    "The evidence pointed to a compromised WordPress management tool used across the portfolio. Because the same tool was connected to all 130 sites, the exposure spread portfolio-wide. Several of the sites had Wordfence installed and active throughout. It did not detect the infection or prevent re-infection.",
                    "The delivery infrastructure revealed an operation with more reach than a single bad actor with a cheap server. The rotating domains hosting the malicious JavaScript files did not belong to the attacker. They were other compromised WordPress sites belonging to unrelated organisations that had no idea their servers were being used. One delivery domain we identified resolved to the same server as a well-known international non-profit. The attacker had added their domain as a virtual host, planted the file, used it for a couple of days, then moved on. By the time any investigation caught up to a particular domain, the file was already gone.",
                ],
            },
            {
                "heading": "What We Did",
                "paragraphs": [
                    "We worked through every site individually, completing the full sequence on each one before moving to the next. Partial work on a site was not an option given what the re-infection test had shown. The sequence on each site was file system remediation, database cleanup, credential rotation, and hardening. 130 sites over 15 days.",
                ],
                "subsections": [
                    {"heading": "File system remediation", "paragraphs": ["WordPress core files were reinstalled from verified checksums on every site. Non-core directories were inspected manually and cleared of unauthorised PHP files, including the encrypted payloads in the theme pattern directories and anything else that had no business being there. File editing through the WordPress admin was disabled at the configuration level to close that route for future writes."]},
                    {"heading": "Database remediation", "paragraphs": ["The injected JavaScript strings were located and removed from the wp_posts and wp_options tables on each site's database. This required care to strip the malicious content without corrupting legitimate data. The conditional redirect hooks came out at the source."]},
                    {"heading": "Credential rotation and hardening", "paragraphs": ["All active sessions were terminated, unauthorised admin accounts removed, and credentials rotated across every property. A consistent security configuration was then applied to each site to close the attack surfaces the malware had used: login protections, file permission changes, attack surface reduction across the WordPress configuration, and invalidation of all existing sessions. The configuration that had been missing from the re-infection test site was in place on all 130 by the end."]},
                ],
            },
            {
                "heading": "The Outcome",
                "paragraphs": [
                    "Three months on, all 130 sites remain clean. No re-infections, no redirects, no rogue admin accounts.",
                    "We provided the technical remediation evidence the client needed to move through the Google Ads reinstatement process. Once the domains were verified clean and the documentation submitted, the accounts came back without the recurring suspensions that had defined the previous weeks.",
                    "There is now an ongoing engagement covering the full portfolio. High-profile sites get a weekly manual audit: file integrity checks, security log review, user account monitoring, and backup validation, with a written report after each session. The wider portfolio gets a monthly review cycle.",
                    "The reason the client wanted ongoing cover is straightforward. The infection ran without a single visible indicator for weeks. The only thing that flagged it was Google pulling the ad accounts. Once you have seen an attack run that quietly for that long, the question of whether your current setup would catch something similar becomes a lot harder to answer confidently.",
                ],
            },
            {
                "heading": "What This Means for Agency-Managed Portfolios",
                "paragraphs": [
                    "If you manage WordPress sites for clients who run paid advertising, the same conditions that allowed this infection are common across agency-managed portfolios.",
                ],
                "subsections": [
                    {"heading": "There is no visible signal", "paragraphs": ["The WordPress admin may look clean. The site may load normally. Scanners may report no issue. Paid traffic can still be compromised. Infections like this typically run for weeks before anything surfaces, and when they do, it is usually a Google Ads suspension that reveals it, not a security alert."]},
                    {"heading": "Your management tool can become a single point of failure", "paragraphs": ["Centralised management is efficient, but if the tool is compromised, exposure can spread across every connected site simultaneously. The assumption that a trusted platform is safe to use is not the same as knowing it is."]},
                    {"heading": "Cleanup without hardening creates a loop", "paragraphs": ["Removing malware is not the same as closing the entry point. In this case, a cleaned site without the added hardening layer was re-infected within 24 hours. The entry points have to be closed, or the cycle starts again."]},
                    {"heading": "Automated tools are not enough", "paragraphs": ["This infection was designed to hide from scanners and the WordPress admin. Finding it required direct file system review, database inspection, and behavioural testing. Active security plugins on multiple sites detected nothing throughout the entire infection period."]},
                ],
            },
        ],
        "closingCta": 'Managing a WordPress portfolio with paid traffic behind it? <a href="/contact">YB Marketing</a> helps agencies uncover hidden malware, recover compromised sites, and harden portfolios before silent infections turn into suspended ads, emergency calls, and client-retention problems.',
    },
]
