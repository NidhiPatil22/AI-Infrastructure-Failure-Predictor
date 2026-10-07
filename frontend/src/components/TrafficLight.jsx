export default function TrafficLight({
  orientation = 'vertical',
  active = 'all',
  size = 'md',
  withPole = false,
  withMount = false,
  className = '',
}) {
  const isHorizontal = orientation === 'horizontal';

  // For horizontal: Green, Yellow, Red (matching Image 1)
  // For vertical: Red, Yellow, Green (matching Images 2 & 3)
  const lights = isHorizontal
    ? [
        { id: 'green', color: '#10b981', glow: 'rgba(16, 185, 129, 0.9)' },
        { id: 'yellow', color: '#facc15', glow: 'rgba(250, 204, 21, 0.9)' },
        { id: 'red', color: '#ef4444', glow: 'rgba(239, 68, 68, 0.9)' },
      ]
    : [
        { id: 'red', color: '#ef4444', glow: 'rgba(239, 68, 68, 0.9)' },
        { id: 'yellow', color: '#facc15', glow: 'rgba(250, 204, 21, 0.9)' },
        { id: 'green', color: '#10b981', glow: 'rgba(16, 185, 129, 0.9)' },
      ];

  return (
    <div className={`traffic-light-wrapper ${orientation} size-${size} ${className}`}>
      {withMount && <div className="tl-horizontal-arm" aria-hidden="true" />}
      <div className="tl-casing" aria-label={`Traffic Signal (${orientation})`}>
        {lights.map(({ id, color, glow }) => {
          const isLit = active === 'all' || active === id;
          return (
            <div
              key={id}
              className={`tl-lens-socket ${id} ${isLit ? 'is-illuminated' : 'is-dim'}`}
            >
              <div
                className="tl-lens"
                style={{
                  backgroundColor: isLit ? color : '#1e2631',
                  boxShadow: isLit
                    ? `0 0 14px 3px ${glow}, inset 0 2px 4px rgba(255,255,255,0.4)`
                    : 'inset 0 2px 4px rgba(0,0,0,0.8)',
                }}
              >
                <div className="tl-lens-reflection" />
              </div>
            </div>
          );
        })}
      </div>
      {withPole && !isHorizontal && <div className="tl-pole" aria-hidden="true" />}
    </div>
  );
}
