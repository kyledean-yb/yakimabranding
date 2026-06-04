/* ============================================================
   YB Marketing UI Kit — Services section + ServiceCard
   ============================================================ */

function ServiceCard({ s, onLearn }) {
  const [hover, setHover] = React.useState(false);
  return (
    <div onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
      style={{ background: '#fff', border: '1px solid var(--line)', borderTop: `4px solid ${s.accent}`,
        borderRadius: 'var(--r-lg)', padding: 26, boxShadow: hover ? 'var(--sh-md)' : 'var(--sh-sm)',
        transform: hover ? 'translateY(-6px)' : 'none', transition: 'all var(--dur) var(--ease-out)',
        display: 'flex', flexDirection: 'column', cursor: 'pointer' }} onClick={onLearn}>
      <IconChip icon={s.icon} accent={s.accent} wash={s.wash} size={52} />
      <h3 className="yb-h3" style={{ fontSize: 21, margin: '16px 0 8px' }}>{s.label}</h3>
      <p style={{ margin: '0 0 16px', fontSize: 14.5 }}>{s.blurb}</p>
      <ul style={{ listStyle: 'none', margin: '0 0 18px', padding: 0, display: 'grid', gap: 9 }}>
        {s.feats.map(f => (
          <li key={f} style={{ display: 'flex', alignItems: 'center', gap: 9, fontSize: 13.5, fontWeight: 600, color: 'var(--fg2)' }}>
            <span style={{ width: 18, height: 18, borderRadius: '50%', background: s.wash, color: s.accent,
              display: 'flex', alignItems: 'center', justifyContent: 'center', flex: 'none' }}>
              <Icon name="check" size={12} />
            </span>{f}
          </li>
        ))}
      </ul>
      <span style={{ marginTop: 'auto', display: 'inline-flex', alignItems: 'center', gap: 6,
        color: s.accent, fontWeight: 700, fontSize: 14 }}>
        Learn More <Icon name="arrow-right" size={15} style={{ transform: hover ? 'translateX(4px)' : 'none', transition: 'transform var(--dur) var(--ease)' }} />
      </span>
    </div>
  );
}

function Services({ onGetStarted }) {
  useLucide();
  return (
    <section id="services" style={{ background: 'var(--bg-soft)', padding: '90px 0' }}>
      <Container>
        <div style={{ textAlign: 'center', maxWidth: 680, margin: '0 auto 48px' }}>
          <Eyebrow center>What YB Offers</Eyebrow>
          <h2 className="yb-h2" style={{ margin: '14px 0 14px' }}>Solutions That Deliver</h2>
          <p className="yb-lead" style={{ margin: 0 }}>
            We turn smart plans into bold execution—building brands and campaigns that get seen everywhere.
          </p>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 22 }} className="yb-svc-grid">
          {YB_SERVICES.map(s => <ServiceCard key={s.key} s={s} onLearn={onGetStarted} />)}
        </div>

        {/* CTA strip */}
        <div style={{ marginTop: 28, borderRadius: 'var(--r-xl)', overflow: 'hidden', position: 'relative',
          background: 'var(--grad-navy)', padding: '40px 44px', display: 'flex', alignItems: 'center',
          justifyContent: 'space-between', gap: 24, flexWrap: 'wrap' }}>
          <div style={{ position: 'absolute', inset: 0, backgroundImage: 'var(--grad-mesh)', opacity: .8 }} />
          <div style={{ position: 'relative' }}>
            <h3 style={{ fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: 26, color: '#fff', margin: '0 0 6px' }}>
              Ready to elevate your brand?</h3>
            <p style={{ margin: 0, color: 'var(--fg2-on-dark)', fontSize: 15, maxWidth: 540 }}>
              Let's discuss how our comprehensive solutions can transform your business and accelerate your growth.</p>
          </div>
          <Button variant="grad" size="lg" icon="arrow-right" onClick={onGetStarted} style={{ position: 'relative' }}>
            Start Your Project</Button>
        </div>
      </Container>
    </section>
  );
}

Object.assign(window, { ServiceCard, Services });
