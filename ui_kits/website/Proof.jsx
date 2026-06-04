/* ============================================================
   YB Marketing UI Kit — Why Choose / Stats / Reviews
   ============================================================ */

function StatCounter({ end, suffix = '', label }) {
  const [val, setVal] = React.useState(0);
  const ref = React.useRef(null);
  React.useEffect(() => {
    const el = ref.current; if (!el) return;
    const io = new IntersectionObserver(([e]) => {
      if (e.isIntersecting) {
        io.disconnect();
        const dur = 1400, t0 = performance.now();
        const tick = (t) => {
          const p = Math.min(1, (t - t0) / dur);
          const eased = 1 - Math.pow(1 - p, 3);
          setVal(Math.round(end * eased));
          if (p < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
      }
    }, { threshold: .4 });
    io.observe(el); return () => io.disconnect();
  }, [end]);
  return (
    <div ref={ref} style={{ textAlign: 'center' }}>
      <div style={{ fontFamily: 'var(--font-display)', fontWeight: 800, fontSize: 'clamp(2.4rem,4vw,3.4rem)',
        lineHeight: 1, background: 'var(--grad-brand)', WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent' }}>
        {val}{suffix}</div>
      <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--fg2-on-dark)', marginTop: 10, letterSpacing: '.03em' }}>{label}</div>
    </div>
  );
}

const WHY = [
  { icon: 'users', accent: 'var(--yb-blue)', wash: 'var(--wash-blue)', title: 'Dedicated Team', body: 'Establish & execute strategies. All in house.' },
  { icon: 'line-chart', accent: 'var(--yb-mint)', wash: 'var(--wash-mint)', title: 'Proven Results', body: 'Optimized strategies. Measurable growth.' },
  { icon: 'puzzle', accent: 'var(--yb-violet)', wash: 'var(--wash-violet)', title: 'Custom Solutions', body: 'Tailored strategies. Competitive advantage.' },
];

function WhyChoose() {
  useLucide();
  return (
    <section id="about" style={{ background: 'var(--bg)', padding: '90px 0 0' }}>
      <Container>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 56, alignItems: 'center' }} className="yb-why-grid">
          <div>
            <Eyebrow color="var(--yb-violet)">Why Choose Us</Eyebrow>
            <h2 className="yb-h2" style={{ margin: '14px 0 16px' }}>YB Marketing Drives <span className="yb-grad-text">Real Results</span></h2>
            <p className="yb-lead" style={{ margin: '0 0 28px' }}>
              Partner with a team that combines creative brilliance with strategic thinking to deliver
              exceptional brand experiences that resonate and convert.</p>
            <div style={{ display: 'grid', gap: 14 }}>
              {WHY.map(w => (
                <div key={w.title} style={{ display: 'flex', gap: 15, alignItems: 'flex-start',
                  background: 'var(--bg-soft)', border: '1px solid var(--line)', borderRadius: 'var(--r-md)', padding: 16 }}>
                  <IconChip icon={w.icon} accent={w.accent} wash={w.wash} size={44} />
                  <div><div style={{ fontWeight: 700, fontFamily: 'var(--font-display)', fontSize: 16, color: 'var(--ink)' }}>{w.title}</div>
                    <div style={{ fontSize: 14, color: 'var(--fg2)', marginTop: 3 }}>{w.body}</div></div>
                </div>
              ))}
            </div>
          </div>
          <div style={{ position: 'relative', borderRadius: 'var(--r-xl)', overflow: 'hidden',
            aspectRatio: '4/4.4', background: 'var(--bg-mute)', boxShadow: 'var(--sh-md)' }}>
            <div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column',
              alignItems: 'center', justifyContent: 'center', color: 'var(--fg3)', gap: 10 }}>
              <Icon name="users" size={40} /><span style={{ fontSize: 13, fontWeight: 600 }}>Team photo placeholder</span>
            </div>
          </div>
        </div>
      </Container>

      {/* stats band */}
      <div style={{ marginTop: 80, background: 'var(--grad-navy)', position: 'relative', overflow: 'hidden' }}>
        <div style={{ position: 'absolute', inset: 0, backgroundImage: 'var(--grad-mesh)', opacity: .7 }} />
        <Container style={{ position: 'relative', display: 'grid', gridTemplateColumns: 'repeat(4,1fr)',
          gap: 24, padding: '54px 28px' }} className="yb-stats-grid">
          <StatCounter end={12} label="Years in Business" />
          <StatCounter end={40} suffix="+" label="Industries" />
          <StatCounter end={250} suffix="+" label="Active Clients" />
          <StatCounter end={75} suffix="+" label="Years of Experience" />
        </Container>
      </div>
    </section>
  );
}

const REVIEWS = [
  { q: 'The deliverables exceeded our expectations.', n: 'Kate McKenna', r: 'Executive Director', c: 'Ballpark GID · Denver, CO', src: 'Clutch', tags: ['Branding','SEO','Social'] },
  { q: "Their communication style and depth of knowledge is unmatched.", n: 'Jade Cutler', r: 'Social & E-Commerce Mgr', c: 'The Focus Group · Denver, CO', src: 'Clutch', tags: ['SEO','Google Ads'] },
  { q: "They're the first agency that acts as a partner and invests in our value as a company.", n: 'Ken Rayment', r: 'Committee Chair', c: 'NOCO Partnership · Loveland, CO', src: 'Clutch', tags: ['Video'] },
  { q: 'Professional, creative, accommodating and very patient! We are very happy with our website.', n: 'Heather Hellums', r: 'Google Review', c: 'Yakima, WA', src: 'Google', tags: ['Web Design'] },
  { q: 'We view them as an extension of our own team.', n: 'Eric Ward', r: 'Assistant Director', c: 'Pickens Tech · Aurora, CO', src: 'Clutch', tags: ['Advertising','Email'] },
  { q: 'The business has been leaping up the Google results page with organic searches.', n: 'Apex Dentures', r: 'Google Review', c: 'WA', src: 'Google', tags: ['SEO'] },
];

function ReviewCard({ rv }) {
  const [hover, setHover] = React.useState(false);
  const initials = rv.n.split(' ').map(w => w[0]).slice(0,2).join('');
  const grads = ['var(--grad-brand)','var(--grad-violet)','var(--grad-sunset)'];
  const g = grads[(rv.n.charCodeAt(0)) % grads.length];
  return (
    <div onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
      style={{ background: '#fff', border: '1px solid var(--line)', borderRadius: 'var(--r-lg)', padding: 24,
        boxShadow: hover ? 'var(--sh-md)' : 'var(--sh-sm)', transform: hover ? 'translateY(-4px)' : 'none',
        transition: 'all var(--dur) var(--ease-out)', breakInside: 'avoid', marginBottom: 22 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
        <div style={{ display: 'flex', gap: 2, color: 'var(--yb-amber)' }}>
          {[0,1,2,3,4].map(i => <Icon key={i} name="star" size={16} style={{ fill: 'var(--yb-amber)' }} />)}
        </div>
        <span style={{ fontSize: 11, fontWeight: 700, color: rv.src === 'Clutch' ? 'var(--yb-coral)' : 'var(--yb-blue)',
          display: 'inline-flex', alignItems: 'center', gap: 4 }}>
          <Icon name="badge-check" size={13} />{rv.src}</span>
      </div>
      <p style={{ margin: '0 0 18px', fontSize: 15.5, fontWeight: 600, color: 'var(--ink)', lineHeight: 1.5 }}>"{rv.q}"</p>
      <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 16 }}>
        {rv.tags.map(t => <span key={t} style={{ fontSize: 11, fontWeight: 700, color: 'var(--fg2)',
          background: 'var(--bg-mute)', borderRadius: 'var(--r-pill)', padding: '4px 10px' }}>{t}</span>)}
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 11, borderTop: '1px solid var(--line)', paddingTop: 14 }}>
        <div style={{ width: 40, height: 40, borderRadius: '50%', background: g, color: '#fff', display: 'flex',
          alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontFamily: 'var(--font-display)', fontSize: 14 }}>{initials}</div>
        <div><div style={{ fontWeight: 700, fontSize: 14, color: 'var(--ink)' }}>{rv.n}</div>
          <div style={{ fontSize: 12, color: 'var(--fg3)' }}>{rv.r} · {rv.c}</div></div>
      </div>
    </div>
  );
}

function Reviews() {
  useLucide();
  return (
    <section id="reviews" style={{ background: 'var(--bg-soft)', padding: '90px 0' }}>
      <Container>
        <div style={{ textAlign: 'center', maxWidth: 640, margin: '0 auto 46px' }}>
          <Eyebrow center color="var(--yb-coral)">Client Love</Eyebrow>
          <h2 className="yb-h2" style={{ margin: '14px 0 12px' }}>Don't Just Take Our Word For It</h2>
          <p className="yb-lead" style={{ margin: 0 }}>Verified reviews from the businesses we've helped grow.</p>
        </div>
        <div style={{ columnCount: 3, columnGap: 22 }} className="yb-reviews-grid">
          {REVIEWS.map((rv, i) => <ReviewCard key={i} rv={rv} />)}
        </div>
      </Container>
    </section>
  );
}

Object.assign(window, { StatCounter, WhyChoose, Reviews, ReviewCard, REVIEWS });
