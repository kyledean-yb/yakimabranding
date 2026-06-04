/* ============================================================
   YB Marketing UI Kit — Hero
   ============================================================ */

function Hero({ onGetStarted }) {
  useLucide();
  return (
    <section id="top" style={{ position: 'relative', overflow: 'hidden', background: 'var(--bg)' }}>
      <div style={{ position: 'absolute', inset: 0, backgroundImage: 'var(--grad-mesh)', pointerEvents: 'none' }} />
      <Container style={{ position: 'relative', display: 'grid', gridTemplateColumns: '1.05fr .95fr',
        gap: 56, alignItems: 'center', padding: '74px 28px 88px' }} >
        <div className="yb-hero-copy">
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: 9, background: '#fff',
            border: '1px solid var(--line)', borderRadius: 'var(--r-pill)', padding: '7px 15px 7px 8px',
            boxShadow: 'var(--sh-sm)', marginBottom: 24 }}>
            <span style={{ background: 'var(--grad-sunset)', color: '#fff', fontSize: 11, fontWeight: 800,
              padding: '3px 9px', borderRadius: 'var(--r-pill)', letterSpacing: '.04em', whiteSpace: 'nowrap' }}>AWARD-WINNING</span>
            <span style={{ fontSize: 13, fontWeight: 600, color: 'var(--fg2)', whiteSpace: 'nowrap' }}>5 U.S. offices</span>
          </div>
          <h1 className="yb-display" style={{ margin: '0 0 20px', fontSize: 'clamp(2.6rem,4.6vw,4.1rem)' }}>
            Full-Spectrum Branding & <span className="yb-grad-text">Digital Marketing</span>
          </h1>
          <p className="yb-lead" style={{ margin: '0 0 32px', maxWidth: 540 }}>
            We craft exceptional brand experiences that captivate audiences, drive engagement, and
            accelerate business growth through innovative digital marketing strategies.
          </p>
          <div style={{ display: 'flex', gap: 14, flexWrap: 'wrap', alignItems: 'center' }}>
            <Button variant="grad" size="lg" icon="arrow-right" onClick={onGetStarted}>Get Started Today</Button>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
              <div style={{ display: 'flex' }}>
                {['#7B5BE6','#2BC4F0','#FF6B57','#25C28A'].map((c,i)=>(
                  <span key={i} style={{ width: 34, height: 34, borderRadius: '50%', background: c,
                    border: '2px solid #fff', marginLeft: i ? -10 : 0 }} />
                ))}
              </div>
              <div style={{ fontSize: 13 }}>
                <div style={{ fontWeight: 800, color: 'var(--ink)' }}>250+ clients</div>
                <div style={{ color: 'var(--fg3)' }}>trust YB Marketing</div>
              </div>
            </div>
          </div>
        </div>

        {/* hero visual */}
        <div style={{ position: 'relative' }} className="yb-hero-visual">
          <div style={{ position: 'relative', borderRadius: 'var(--r-xl)', overflow: 'hidden',
            boxShadow: 'var(--sh-lg)', aspectRatio: '4/3.4', background: 'var(--grad-navy)' }}>
            <div style={{ position: 'absolute', inset: 0, backgroundImage: 'var(--grad-mesh)', opacity: .9 }} />
            <div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column',
              alignItems: 'center', justifyContent: 'center', color: 'rgba(255,255,255,.5)', gap: 10 }}>
              <Icon name="image" size={40} />
              <span style={{ fontSize: 13, fontWeight: 600 }}>Hero image placeholder</span>
            </div>
          </div>
          {/* floating stat card */}
          <div style={{ position: 'absolute', bottom: -22, left: -22, background: '#fff', borderRadius: 'var(--r-lg)',
            boxShadow: 'var(--sh-lg)', padding: '16px 20px', display: 'flex', alignItems: 'center', gap: 13 }}>
            <IconChip icon="trending-up" grad="var(--grad-brand)" size={44} />
            <div><div style={{ fontFamily: 'var(--font-display)', fontWeight: 800, fontSize: 22, color: 'var(--ink)', lineHeight: 1 }}>+182%</div>
              <div style={{ fontSize: 12, color: 'var(--fg3)', fontWeight: 600 }}>Avg. lead growth</div></div>
          </div>
          {/* floating review chip */}
          <div style={{ position: 'absolute', top: -18, right: -14, background: '#fff', borderRadius: 'var(--r-md)',
            boxShadow: 'var(--sh-md)', padding: '10px 14px', display: 'flex', alignItems: 'center', gap: 8 }}>
            <div style={{ display: 'flex', gap: 1, color: 'var(--yb-amber)' }}>
              {[0,1,2,3,4].map(i => <Icon key={i} name="star" size={14} style={{ fill: 'var(--yb-amber)' }} />)}
            </div>
            <span style={{ fontSize: 12, fontWeight: 800, color: 'var(--ink)' }}>5.0 on Clutch</span>
          </div>
        </div>
      </Container>
    </section>
  );
}

Object.assign(window, { Hero });
