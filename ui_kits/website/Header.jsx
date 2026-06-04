/* ============================================================
   YB Marketing UI Kit — Header (sticky nav)
   ============================================================ */

const YB_SERVICES = [
  { key: 'branding', label: 'Brand Identity', icon: 'palette',  accent: 'var(--yb-violet)', wash: 'var(--wash-violet)',
    blurb: 'Comprehensive brand identity systems that capture your essence.',
    feats: ['Brand Strategy', 'Brand Logo', 'Design System', 'Web Design'] },
  { key: 'seo', label: 'SEO & AI Search', icon: 'search', accent: 'var(--yb-cyan)', wash: 'var(--wash-cyan)',
    blurb: 'Put your brand at the top of search results and inside AI-powered results.',
    feats: ['Keyword Strategy', 'Technical SEO', 'Local & AI Visibility', 'Analytics'] },
  { key: 'google-ads', label: 'Google Ads / PPC', icon: 'target', accent: 'var(--yb-coral)', wash: 'var(--wash-coral)',
    blurb: 'Drive immediate traffic and measurable ROI with targeted ad campaigns.',
    feats: ['Google Ads', 'Landing Pages', 'Conversion Tracking', 'Bid Management'] },
  { key: 'social', label: 'Social Media', icon: 'share-2', accent: 'var(--yb-amber)', wash: 'var(--wash-amber)',
    blurb: 'Grow your brand presence and engage your audience where they are.',
    feats: ['Social Strategy', 'Content & Scheduling', 'Paid Social', 'Community'] },
  { key: 'web-design', label: 'Web Design & Dev', icon: 'layout', accent: 'var(--yb-mint)', wash: 'var(--wash-mint)',
    blurb: 'Turn your website into your most powerful marketing tool.',
    feats: ['Custom Design', 'Mobile & ADA', 'Performance', 'CMS Integration'] },
  { key: 'content', label: 'Content & Email', icon: 'pen-line', accent: 'var(--yb-pink)', wash: 'var(--wash-pink)',
    blurb: 'Nurture leads and build loyalty with compelling content.',
    feats: ['Copywriting', 'Email Strategy', 'Drip Sequences', 'Newsletters'] },
];

function Logo({ dark }) {
  return (
    <a href="#top" onClick={(e)=>{e.preventDefault(); window.scrollTo({top:0,behavior:'smooth'});}}
       style={{ display: 'flex', alignItems: 'center', gap: 11, textDecoration: 'none' }}>
      <img src="../../assets/yb-logo-color.png" alt="YB Marketing" style={{ width: 42, height: 42 }} />
      <span style={{ fontFamily: 'var(--font-display)', fontWeight: 800, fontSize: 21,
                     letterSpacing: '-.02em', lineHeight: 1, color: dark ? '#fff' : 'var(--ink)' }}>
        YB <span style={{ color: dark ? 'var(--yb-cyan)' : 'var(--yb-blue)' }}>Marketing</span>
      </span>
    </a>
  );
}

function Header({ onGetStarted, onNav }) {
  const [scrolled, setScrolled] = React.useState(false);
  const [menuOpen, setMenuOpen] = React.useState(false);
  const [svcOpen, setSvcOpen] = React.useState(false);
  useLucide();
  React.useEffect(() => {
    const fn = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', fn); return () => window.removeEventListener('scroll', fn);
  }, []);
  const links = [['Home','top'], ['About','about'], ['Services','services'], ['Blog','blog'], ['Contact','contact']];
  const go = (id) => { setMenuOpen(false); onNav && onNav(id); };

  return (
    <header style={{ position: 'sticky', top: 0, zIndex: 50,
      background: scrolled ? 'rgba(255,255,255,.82)' : 'rgba(255,255,255,.6)',
      backdropFilter: 'blur(14px)', WebkitBackdropFilter: 'blur(14px)',
      borderBottom: scrolled ? '1px solid var(--line)' : '1px solid transparent',
      transition: 'all var(--dur) var(--ease)' }}>
      {/* announcement bar */}
      <div style={{ background: 'var(--grad-navy)', color: '#fff', textAlign: 'center',
        fontSize: 12.5, fontWeight: 600, padding: '7px 16px', letterSpacing: '.01em' }}>
        encite International is now YB Marketing. <span style={{ color: 'var(--yb-cyan)' }}>Learn more →</span>
      </div>
      <Container style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: 70 }}>
        <Logo />
        <nav style={{ display: 'flex', alignItems: 'center', gap: 4 }} className="yb-nav-desktop">
          {links.map(([label, id]) => (
            <div key={id} style={{ position: 'relative' }}
                 onMouseEnter={() => id==='services' && setSvcOpen(true)}
                 onMouseLeave={() => id==='services' && setSvcOpen(false)}>
              <button onClick={() => go(id)} style={{ background: 'none', border: 'none', cursor: 'pointer',
                fontFamily: 'var(--font-body)', fontWeight: 600, fontSize: 15, color: 'var(--fg1)',
                padding: '8px 14px', borderRadius: 'var(--r-sm)', display: 'inline-flex', alignItems: 'center', gap: 5 }}>
                {label}{id==='services' && <Icon name="chevron-down" size={15} />}
              </button>
              {id === 'services' && svcOpen && (
                <div style={{ position: 'absolute', top: '100%', left: '50%', transform: 'translateX(-50%)',
                  background: '#fff', borderRadius: 'var(--r-lg)', boxShadow: 'var(--sh-lg)', border: '1px solid var(--line)',
                  padding: 12, width: 460, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 4, marginTop: 6 }}>
                  {YB_SERVICES.map(s => (
                    <button key={s.key} onClick={() => go('services')}
                      style={{ display: 'flex', alignItems: 'center', gap: 11, padding: '10px 12px', borderRadius: 'var(--r-md)',
                        border: 'none', background: 'none', cursor: 'pointer', textAlign: 'left' }}
                      onMouseEnter={e => e.currentTarget.style.background = 'var(--bg-soft)'}
                      onMouseLeave={e => e.currentTarget.style.background = 'none'}>
                      <IconChip icon={s.icon} accent={s.accent} wash={s.wash} size={38} />
                      <span style={{ fontWeight: 700, fontSize: 14, color: 'var(--ink)' }}>{s.label}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>
          ))}
        </nav>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <Button variant="grad" onClick={onGetStarted} style={{ padding: '11px 20px' }} className="yb-nav-desktop">
            Get Started
          </Button>
          <button className="yb-nav-mobile" onClick={() => setMenuOpen(o => !o)}
            style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 6, display: 'none' }}>
            <Icon name={menuOpen ? 'x' : 'menu'} size={26} />
          </button>
        </div>
      </Container>
      {menuOpen && (
        <div className="yb-nav-mobile" style={{ borderTop: '1px solid var(--line)', background: '#fff', padding: '12px 28px 20px' }}>
          {links.map(([label, id]) => (
            <button key={id} onClick={() => go(id)} style={{ display: 'block', width: '100%', textAlign: 'left',
              background: 'none', border: 'none', borderBottom: '1px solid var(--line)', padding: '14px 0',
              fontFamily: 'var(--font-body)', fontWeight: 600, fontSize: 17, color: 'var(--ink)', cursor: 'pointer' }}>
              {label}
            </button>
          ))}
          <Button variant="grad" onClick={() => { setMenuOpen(false); onGetStarted(); }} style={{ width: '100%', justifyContent: 'center', marginTop: 16 }}>
            Get Started
          </Button>
        </div>
      )}
    </header>
  );
}

Object.assign(window, { Header, Logo, YB_SERVICES });
