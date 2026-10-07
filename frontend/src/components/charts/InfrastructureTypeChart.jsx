import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

export default function InfrastructureTypeChart({ data = [] }) {
  if (!data.length) return <div className="chart-empty">The dashboard API does not return failure or risk counts by infrastructure type.</div>;
  return (
    <div className="chart-area">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 10, right: 8, left: -18, bottom: 0 }}>
          <CartesianGrid stroke="#edf1f5" vertical={false} />
          <XAxis dataKey="name" tickLine={false} axisLine={false} tick={{ fill: '#7b8798', fontSize: 11 }} />
          <YAxis tickLine={false} axisLine={false} tick={{ fill: '#7b8798', fontSize: 11 }} />
          <Tooltip />
          <Bar dataKey="value" fill="#3979d8" radius={[5, 5, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
