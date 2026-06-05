/* ============================================================
   YB Marketing UI Kit — Contact / Footer / Contact Modal
   ============================================================ */

function Contact({ onGetStarted }) {
  useLucide();
  const methods = [
    { icon: 'calendar', accent: 'var(--yb-blue)', wash: 'var(--wash-blue)', title: 'Schedule a Consultation',
      body: 'Book a free 30-minute strategy session', cta: 'Book Meeting', note: 'Free consultation' },
    { icon: 'mail', accent: 'var(--yb-pink)', wash: 'var(--wash-pink)', title: 'Send us an Email',
      body: 'sales@yakimabranding.com', cta: 'Email Us', note: 'Response within 2 business hours' },
    { icon: 'phone', accent: 'var(--yb-mint)', wash: 'var(--wash-mint)', title: 'Call Our Experts',
      body: '510-687-9737', cta: 'Call Now', note: 'Mon–Fri 9AM–6PM PST' },
  ];
  return (
    <section id="contact" style={{ background: 'var(--bg-soft)', padding: '90px 0' }}>
      <Container>
        <div style={{ textAlign: 'center', maxWidth: 640, margin: '0 auto 46px' }}>
          <Eyebrow center>Get Started</Eyebrow>
          <h2 className="yb-h2" style={{ margin: '14px 0 12px' }}>Work With a Team Built to <span className="yb-grad-text">Drive You Results</span></h2>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 22 }} className="yb-svc-grid">
          {methods.map(m => (
            <div key={m.title} style={{ background: '#fff', border: '1px solid var(--line)', borderRadius: 'var(--r-lg)',
              padding: 28, textAlign: 'center', boxShadow: 'var(--sh-sm)', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <IconChip icon={m.icon} accent={m.accent} wash={m.wash} size={56} />
              <h3 className="yb-h3" style={{ fontSize: 19, margin: '16px 0 6px' }}>{m.title}</h3>
              <p style={{ margin: '0 0 18px', fontSize: 14.5, fontWeight: 600, color: 'var(--fg1)' }}>{m.body}</p>
              <Button variant="ghost" onClick={onGetStarted} style={{ marginTop: 'auto' }}>{m.cta}</Button>
              <div style={{ fontSize: 12, color: 'var(--fg3)', marginTop: 12 }}>{m.note}</div>
            </div>
          ))}
        </div>
      </Container>
    </section>
  );
}

function Footer() {
  useLucide();
  const offices = [['Colorado','Denver, CO'],['Arizona','Scottsdale, AZ'],['California','San Francisco, CA'],['Illinois','Chicago, IL'],['Washington','Yakima, WA']];
  const cols = [
    ['Navigation', ['Home','About','Services','Blog','Reviews','Contact']],
    ['Services', ['Brand Identity','SEO Optimization','Google Ads','Social Media','Web Design','Content Marketing']],
  ];
  return (
    <footer style={{ background: 'var(--grad-navy)', color: '#fff', position: 'relative', overflow: 'hidden' }}>
      <div style={{ position: 'absolute', inset: 0, backgroundImage: 'var(--grad-mesh)', opacity: .5 }} />
      <Container style={{ position: 'relative', padding: '64px 28px 28px' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1.6fr 1fr 1fr 1.4fr', gap: 40 }} className="yb-footer-grid">
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 11, marginBottom: 16 }}>
              <img src="../../assets/yb-logo-white.png" alt="YB" style={{ width: 40, height: 40, filter: 'drop-shadow(0 0 1px rgba(255,255,255,.5))' }} />
              <span style={{ fontFamily: 'var(--font-display)', fontWeight: 800, fontSize: 20 }}>YB <span style={{ color: 'var(--yb-cyan)' }}>Marketing</span></span>
            </div>
            <p style={{ color: 'var(--fg2-on-dark)', fontSize: 14, maxWidth: 280, margin: '0 0 18px' }}>
              Award-winning digital marketing agency helping businesses grow through strategic branding, SEO, and comprehensive digital solutions.</p>
            <div style={{ display: 'flex', gap: 10 }}>
              {['facebook','instagram','linkedin'].map(s => (
                <a key={s} href="#" onClick={e=>e.preventDefault()} style={{ width: 38, height: 38, borderRadius: 'var(--r-sm)',
                  background: 'rgba(255,255,255,.1)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff' }}>
                  <Icon name={s} size={17} /></a>
              ))}
            </div>
          </div>
          {cols.map(([h, items]) => (
            <div key={h}>
              <h4 style={{ fontFamily: 'var(--font-display)', fontSize: 14, fontWeight: 700, margin: '0 0 14px', letterSpacing: '.04em' }}>{h}</h4>
              <ul style={{ listStyle: 'none', margin: 0, padding: 0, display: 'grid', gap: 10 }}>
                {items.map(i => <li key={i}><a href="#" onClick={e=>e.preventDefault()} style={{ color: 'var(--fg2-on-dark)', textDecoration: 'none', fontSize: 14 }}>{i}</a></li>)}
              </ul>
            </div>
          ))}
          <div>
            <h4 style={{ fontFamily: 'var(--font-display)', fontSize: 14, fontWeight: 700, margin: '0 0 14px', letterSpacing: '.04em' }}>Our Offices</h4>
            <ul style={{ listStyle: 'none', margin: 0, padding: 0, display: 'grid', gap: 11 }}>
              {offices.map(([s, c]) => (
                <li key={s} style={{ display: 'flex', alignItems: 'center', gap: 9, fontSize: 13.5 }}>
                  <Icon name="map-pin" size={15} style={{ color: 'var(--yb-cyan)' }} />
                  <span><b style={{ color: '#fff' }}>{s}</b> <span style={{ color: 'var(--fg2-on-dark)' }}>· {c}</span></span></li>
              ))}
            </ul>
          </div>
        </div>
        <div style={{ borderTop: '1px solid rgba(255,255,255,.12)', marginTop: 40, paddingTop: 22,
          display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: 12,
          color: 'var(--fg2-on-dark)', fontSize: 13 }}>
          <span>© 2026 YB Marketing. All rights reserved.</span>
          <span style={{ display: 'flex', gap: 20 }}><a href="/privacy-policy.html" style={{ color: 'var(--fg2-on-dark)', textDecoration: 'none' }}>Privacy Policy</a>
            <a href="/sitemap.html" style={{ color: 'var(--fg2-on-dark)', textDecoration: 'none' }}>Sitemap</a></span>
        </div>
      </Container>
    </footer>
  );
}

function ContactModal({ open, onClose }) {
  const [sent, setSent] = React.useState(false);
  useLucide();
  React.useEffect(() => { if (open) setSent(false); }, [open]);
  if (!open) return null;
  const field = { width: '100%', boxSizing: 'border-box', fontFamily: 'var(--font-body)', fontSize: 15,
    padding: '12px 14px', border: '1.5px solid var(--line-strong)', borderRadius: 'var(--r-md)', background: '#fff', color: 'var(--ink)', marginTop: 6 };
  const lab = { fontSize: 12.5, fontWeight: 700, color: 'var(--fg2)' };
  return (
    <div onClick={onClose} style={{ position: 'fixed', inset: 0, zIndex: 100, background: 'rgba(22,32,58,.55)',
      backdropFilter: 'blur(4px)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 20 }}>
      <div onClick={e => e.stopPropagation()} style={{ background: '#fff', borderRadius: 'var(--r-xl)', width: 'min(460px,100%)',
        boxShadow: 'var(--sh-lg)', overflow: 'hidden', maxHeight: '92vh', overflowY: 'auto' }}>
        <div style={{ background: 'var(--grad-navy)', position: 'relative', padding: '26px 28px', color: '#fff' }}>
          <div style={{ position: 'absolute', inset: 0, backgroundImage: 'var(--grad-mesh)', opacity: .7 }} />
          <button onClick={onClose} style={{ position: 'absolute', top: 16, right: 16, background: 'rgba(255,255,255,.15)',
            border: 'none', borderRadius: '50%', width: 32, height: 32, color: '#fff', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Icon name="x" size={18} /></button>
          <div style={{ position: 'relative' }}>
            <Eyebrow color="var(--yb-cyan)">Free Marketing Analysis</Eyebrow>
            <h3 style={{ fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: 24, margin: '10px 0 0' }}>Let's Get Started</h3>
          </div>
        </div>
        {sent ? (
          <div style={{ padding: '48px 28px', textAlign: 'center' }}>
            <div style={{ width: 64, height: 64, borderRadius: '50%', background: 'var(--wash-mint)', color: 'var(--yb-mint)',
              display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 18px' }}><Icon name="check" size={32} /></div>
            <h3 className="yb-h3" style={{ margin: '0 0 8px' }}>Thanks — we'll be in touch!</h3>
            <p style={{ margin: '0 0 22px', fontSize: 14.5 }}>One of our experts will reach out within 2 business hours.</p>
            <Button variant="grad" onClick={onClose}>Close</Button>
          </div>
        ) : (
          <form onSubmit={e => { e.preventDefault(); setSent(true); }} style={{ padding: '24px 28px 30px', display: 'grid', gap: 14 }}>
            <div><label style={lab}>Name *</label><input style={field} required placeholder="Your name" /></div>
            <div><label style={lab}>Email *</label><input style={field} type="email" required placeholder="you@company.com" /></div>
            <div><label style={lab}>Company Name or URL *</label><input style={field} required placeholder="yourcompany.com" /></div>
            <div><label style={lab}>How can we help?</label><textarea style={{ ...field, resize: 'vertical', minHeight: 80 }} placeholder="Tell us about your project…" /></div>
            <Button variant="grad" icon="arrow-right" style={{ justifyContent: 'center', width: '100%' }}>Send Message</Button>
          </form>
        )}
      </div>
    </div>
  );
}

Object.assign(window, { Contact, Footer, ContactModal });
