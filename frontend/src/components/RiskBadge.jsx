import { humanize, riskClass } from '../utils/formatters.js';

export default function RiskBadge({ risk }) {
  return <span className={`risk-badge risk-${riskClass(risk)}`}>{humanize(risk)}</span>;
}
