/* ============================================================
   YB Marketing UI Kit — Blog / Insights
   ============================================================ */

const POSTS = [
  { cat: 'Content Marketing', accent: 'var(--yb-pink)', wash: 'var(--wash-pink)', read: '6 min',
    title: 'What Is Content Marketing and Why Does It Matter?',
    excerpt: 'The creation of helpful content that attracts, educates, and converts potential customers.' },
  { cat: 'Branding', accent: 'var(--yb-violet)', wash: 'var(--wash-violet)', read: '6 min',
    title: 'What Is Brand Identity and Why Does It Matter?',
    excerpt: 'The visual and messaging system that makes your business recognizable.' },
  { cat: 'SEO', accent: 'var(--yb-cyan)', wash: 'var(--wash-cyan)', read: '7 min',
    title: 'How SEO Helps Small Businesses Get Found',
    excerpt: 'Improve how your website appears in Google Search, Maps, and AI-powered results.' },
  { cat: 'Google Ads', accent: 'var(--yb-coral)', wash: 'var(--wash-coral)', read: '7 min',
    title: 'Google Ads for Small Businesses: Spend Smarter',
    excerpt: 'Generate leads quickly with focused keywords, location targeting, and conversion tracking.' },
];

function BlogCard({ p, featured }) {
  const [hover, setHover] = React.useState(false);
  return (
    <article onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
      style={{ background: '#fff', border: '1px solid var(--line)', borderRadius: 'var(--r-lg)', overflow: 'hidden',
        boxShadow: hover ? 'var(--sh-md)' : 'var(--sh-sm)', transform: hover ? 'translateY(-5px)' : 'none',
        transition: 'all var(--dur) var(--ease-out)', cursor: 'pointer', display: 'flex',
        flexDirection: featured ? 'column' : 'column', height: '100%' }}>
      <div style={{ position: 'relative', aspectRatio: featured ? '16/8' : '16/9', background: p.wash,
        display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Icon name="image" size={32} style={{ color: p.accent, opacity: .55 }} />
        <span style={{ position: 'absolute', top: 14, left: 14, background: '#fff', color: p.accent,
          fontSize: 11, fontWeight: 800, padding: '5px 11px', borderRadius: 'var(--r-pill)',
          boxShadow: 'var(--sh-xs)', letterSpacing: '.02em' }}>{p.cat}</span>
      </div>
      <div style={{ padding: featured ? 26 : 20, display: 'flex', flexDirection: 'column', flex: 1 }}>
        <h3 className="yb-h3" style={{ fontSize: featured ? 23 : 17.5, margin: '0 0 9px', lineHeight: 1.25 }}>{p.title}</h3>
        <p style={{ margin: '0 0 16px', fontSize: 14, color: 'var(--fg2)' }}>{p.excerpt}</p>
        <div style={{ marginTop: 'auto', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <span style={{ fontSize: 12.5, color: 'var(--fg3)', fontWeight: 600, display: 'inline-flex', alignItems: 'center', gap: 6 }}>
            <Icon name="clock" size={13} />{p.read} read</span>
          <span style={{ color: p.accent, fontWeight: 700, fontSize: 13.5, display: 'inline-flex', alignItems: 'center', gap: 5 }}>
            Read More <Icon name="arrow-right" size={14} style={{ transform: hover ? 'translateX(3px)' : 'none', transition: 'transform var(--dur) var(--ease)' }} /></span>
        </div>
      </div>
    </article>
  );
}

function Blog() {
  useLucide();
  return (
    <section id="blog" style={{ background: 'var(--bg)', padding: '90px 0' }}>
      <Container>
        <div style={{ display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between',
          gap: 24, marginBottom: 42, flexWrap: 'wrap' }}>
          <div style={{ maxWidth: 560 }}>
            <Eyebrow color="var(--yb-mint)">Insights</Eyebrow>
            <h2 className="yb-h2" style={{ margin: '14px 0 12px' }}>Marketing Insights for Growing Businesses</h2>
            <p className="yb-lead" style={{ margin: 0 }}>Practical strategies for SEO, Google Ads, web design, branding, social, and content.</p>
          </div>
          <Button variant="ghost" icon="arrow-right">View All Insights</Button>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: '1.4fr 1fr 1fr', gap: 22 }} className="yb-blog-grid">
          <div style={{ gridRow: 'span 1' }}><BlogCard p={POSTS[0]} featured /></div>
          <BlogCard p={POSTS[1]} />
          <BlogCard p={POSTS[2]} />
        </div>
      </Container>
    </section>
  );
}

Object.assign(window, { BlogCard, Blog, POSTS });
