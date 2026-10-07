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
          <CartesianGrid stroke="#edf1f5" vertical={false} />
          <XAxis dataKey="name" tickFormatter={(value) => humanize(value).replace(' Infrastructure', '')} tickLine={false} axisLine={false} tick={{ fill: '#7b8798', fontSize: 10 }} />
          <YAxis tickLine={false} axisLine={false} tick={{ fill: '#7b8798', fontSize: 11 }} />
          <Tooltip />
          <Bar dataKey="size" name="Assets" fill="#7459c7" radius={[5, 5, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
