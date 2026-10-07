import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts';

const COLORS = ['#10b981', '#facc15', '#ef4444'];

export default function RiskDistribution({ data = [] }) {
  const available = data.filter((item) => Number(item.value) > 0);
  if (!available.length) return <div className="chart-empty">Risk distribution is not available from this response.</div>;
  return (
    <div className="chart-with-legend">
      <div className="chart-area chart-donut">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie data={available} dataKey="value" nameKey="name" innerRadius={62} outerRadius={90} paddingAngle={4} stroke="none">
              {available.map((item, index) => <Cell key={item.name} fill={COLORS[index % COLORS.length]} />)}
            </Pie>
            <Tooltip formatter={(value) => [value, 'Assets']} />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="chart-legend">
        {available.map((item, index) => (
          <div className="legend-row" key={item.name}><i style={{ backgroundColor: COLORS[index % COLORS.length] }} /><span>{item.name}</span><strong>{item.value.toLocaleString()}</strong></div>
        ))}
      </div>
    </div>
  );
}
