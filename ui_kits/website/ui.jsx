/* ============================================================
   YB Marketing UI Kit — Primitives
   Button, Eyebrow, IconChip, Icon, Container
   ============================================================ */

// Lucide icon as a React element. A global effect re-runs createIcons.
function Icon({ name, size = 18, className = '', style = {} }) {
  return <i data-lucide={name} className={className}
            style={{ width: size, height: size, display: 'inline-flex', ...style }} />;
}

function useLucide(dep) {
  React.useEffect(() => {
    if (window.lucide) window.lucide.createIcons();
  });
}

const ybContainer = { width: '100%', maxWidth: 'var(--container)', margin: '0 auto', padding: '0 28px', boxSizing: 'border-box' };
function Container({ children, style = {} }) {
  return <div style={{ ...ybContainer, ...style }}>{children}</div>;
}

function Eyebrow({ children, color = 'var(--yb-blue)', center }) {
  return (
    <div style={{ display: 'inline-flex', alignItems: 'center', gap: 8,
                  justifyContent: center ? 'center' : 'flex-start' }}>
      <span style={{ width: 7, height: 7, borderRadius: '50%', background: color, flex: 'none' }} />
      <span className="yb-eyebrow" style={{ color }}>{children}</span>
    </div>
  );
}

const btnBase = {
  fontFamily: 'var(--font-body)', fontWeight: 700, fontSize: 15, cursor: 'pointer',
  border: 'none', display: 'inline-flex', alignItems: 'center', gap: 8,
  borderRadius: 'var(--r-md)', padding: '13px 22px', transition: 'all var(--dur) var(--ease)',
  lineHeight: 1, textDecoration: 'none', whiteSpace: 'nowrap',
};
const btnVariants = {
  primary: { background: 'var(--yb-blue)', color: '#fff', boxShadow: 'var(--sh-blue)' },
  grad:    { background: 'var(--grad-brand)', color: '#fff', boxShadow: 'var(--sh-blue)' },
  coral:   { background: 'var(--yb-coral)', color: '#fff', boxShadow: 'var(--sh-coral)' },
  navy:    { background: 'var(--yb-navy)', color: '#fff' },
  ghost:   { background: '#fff', color: 'var(--yb-blue)', border: '1.5px solid var(--line-strong)' },
  ghostLight: { background: 'rgba(255,255,255,.12)', color: '#fff', border: '1.5px solid rgba(255,255,255,.3)' },
};
function Button({ children, variant = 'primary', icon, onClick, size, style = {} }) {
  const [hover, setHover] = React.useState(false);
  const v = btnVariants[variant] || btnVariants.primary;
  const big = size === 'lg' ? { padding: '16px 28px', fontSize: 16 } : {};
  const hov = hover ? { transform: 'translateY(-2px)', filter: 'brightness(1.04)' } : {};
  if (variant === 'ghost' && hover) { hov.borderColor = 'var(--yb-blue)'; hov.background = 'var(--wash-blue)'; }
  return (
    <button onClick={onClick}
      onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
      style={{ ...btnBase, ...v, ...big, ...hov, ...style }}>
      {children}{icon && <Icon name={icon} size={17} />}
    </button>
  );
}

function IconChip({ icon, accent = 'var(--yb-blue)', wash = 'var(--wash-blue)', size = 46, grad }) {
  return (
    <div style={{ width: size, height: size, borderRadius: 'var(--r-md)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  background: grad || wash, color: grad ? '#fff' : accent, flex: 'none' }}>
      <Icon name={icon} size={size * 0.5} />
    </div>
  );
}

Object.assign(window, { Icon, useLucide, Container, Eyebrow, Button, IconChip,
  ybContainer });
