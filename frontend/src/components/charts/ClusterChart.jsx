import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { humanize } from '../../utils/formatters.js';

export default function ClusterChart({ clusters = [] }) {
  const data = clusters.map((cluster) => ({
    name: cluster.description || `Cluster ${cluster.cluster_id}`,
    size: Number(cluster.size) || 0,
  }));
  if (!data.length) return <div className="chart-empty">Clustering details are not available in the backend response.</div>;
  return (
    <div className="chart-area">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 10, right: 8, left: -18, bottom: 0 }}>
          <CartesianGrid stroke="#22344a" vertical={false} />
          <XAxis dataKey="name" tickFormatter={(value) => humanize(value).replace(' Infrastructure', '')} tickLine={false} axisLine={false} tick={{ fill: '#94a3b8', fontSize: 10 }} />
          <YAxis tickLine={false} axisLine={false} tick={{ fill: '#94a3b8', fontSize: 11 }} />
          <Tooltip contentStyle={{ backgroundColor: '#0f1722', borderColor: '#22344a', borderRadius: '8px', color: '#fff' }} />
          <Bar dataKey="size" name="Assets" fill="#fecb00" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
