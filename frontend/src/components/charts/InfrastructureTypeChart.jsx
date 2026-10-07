import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

export default function InfrastructureTypeChart({ data = [] }) {
  if (!data.length) return <div className="chart-empty">The dashboard API does not return failure or risk counts by infrastructure type.</div>;
  return (
    <div className="chart-area">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 10, right: 8, left: -18, bottom: 0 }}>
          <CartesianGrid stroke="#22344a" vertical={false} />
          <XAxis dataKey="name" tickLine={false} axisLine={false} tick={{ fill: '#94a3b8', fontSize: 11 }} />
          <YAxis tickLine={false} axisLine={false} tick={{ fill: '#94a3b8', fontSize: 11 }} />
          <Tooltip contentStyle={{ backgroundColor: '#0f1722', borderColor: '#22344a', borderRadius: '8px', color: '#fff' }} />
          <Bar dataKey="value" fill="#fecb00" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
