const hasValue = (value) => value !== null && value !== undefined && value !== '';

export const formatNumber = (value, digits = 0) => (
  hasValue(value) && Number.isFinite(Number(value))
    ? Number(value).toLocaleString(undefined, { maximumFractionDigits: digits })
    : 'Not available'
);

export const formatPercent = (value) => {
  if (!hasValue(value) || !Number.isFinite(Number(value))) return 'Not available';
  const number = Number(value);
  return `${(number <= 1 ? number * 100 : number).toFixed(1)}%`;
};

export const formatMetric = (value, digits = 3) => (
  hasValue(value) && Number.isFinite(Number(value)) ? Number(value).toFixed(digits) : 'Not available'
);

export const humanize = (value) => (
  String(value ?? 'Not available')
    .replaceAll('_', ' ')
    .replace(/\b\w/g, (letter) => letter.toUpperCase())
);

export const riskClass = (value) => {
  const risk = String(value ?? '').toLowerCase();
  if (risk.includes('high') || risk.includes('critical')) return 'high';
  if (risk.includes('medium') || risk.includes('moderate')) return 'medium';
  if (risk.includes('low') || risk.includes('healthy')) return 'low';
  return 'unknown';
};
