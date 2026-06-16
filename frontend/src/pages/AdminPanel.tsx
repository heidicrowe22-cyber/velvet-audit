import React from 'react';
import { 
  Users, 
  Search, 
  Activity, 
  DollarSign, 
  Wrench,
  Filter,
  CheckCircle,
  Clock,
  AlertCircle
} from 'lucide-react';

const AdminPanel = () => {
  const implementations = [
    { id: 'impl_1', customer: 'Sarah Johnson', website: 'mysalon.com', task: 'Add Lead Gen Form', price: 29, status: 'Pending', assignedTo: 'Unassigned' },
    { id: 'impl_2', customer: 'Mike Miller', website: 'miller-roofing.com', task: 'Mobile Optimization', price: 149, status: 'In Progress', assignedTo: 'John Doe' },
    { id: 'impl_3', customer: 'Mike Miller', website: 'miller-roofing.com', task: 'Alt Text Fixes', price: 29, status: 'Done', assignedTo: 'Jane Smith' },
  ];

  return (
    <div className="min-h-screen bg-ghost p-8">
      <header className="mb-12">
        <h1 className="font-display text-4xl text-velvet-primary mb-2">Admin Command Center</h1>
        <p className="text-slate-deep/60">Manage operations, track revenue, and monitor implementations.</p>
      </header>

      {/* Admin Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
        {[
          { icon: <Users className="w-5 h-5" />, label: 'Active Customers', value: '1,284', trend: '+12% this month', color: 'text-velvet-primary' },
          { icon: <Activity className="w-5 h-5" />, label: 'Audits Run', value: '5,492', trend: '+24% this month', color: 'text-velvet-secondary' },
          { icon: <DollarSign className="w-5 h-5" />, label: 'Monthly Revenue', value: '$42,500', trend: '+18% this month', color: 'text-success' },
          { icon: <Wrench className="w-5 h-5" />, label: 'Pending Fixes', value: '42', trend: '-5% this month', color: 'text-gold' },
        ].map((stat, i) => (
          <div key={i} className="card">
            <div className={`p-2 bg-ghost rounded-lg ${stat.color} w-fit mb-4`}>
              {stat.icon}
            </div>
            <p className="text-[10px] font-heading font-bold uppercase tracking-widest text-slate-deep/40 mb-1">{stat.label}</p>
            <p className="text-3xl font-display text-slate-deep mb-2">{stat.value}</p>
            <p className="text-xs text-success font-bold">{stat.trend}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Implementation Queue */}
        <div className="lg:col-span-2 card p-0 overflow-hidden">
          <div className="p-6 border-b border-ghost flex justify-between items-center">
            <h2 className="text-xl font-display text-velvet-primary">Implementation Queue</h2>
            <div className="flex gap-2">
               <button className="flex items-center gap-2 px-3 py-1 bg-ghost rounded text-xs font-bold text-slate-deep/60">
                 <Filter className="w-3 h-3" /> Filter
               </button>
               <button className="flex items-center gap-2 px-3 py-1 bg-ghost rounded text-xs font-bold text-slate-deep/60">
                 <Search className="w-3 h-3" /> Search
               </button>
            </div>
          </div>
          <table className="w-full text-left">
            <thead className="bg-ghost/50 text-[10px] font-heading font-bold uppercase tracking-widest text-slate-deep/40">
              <tr>
                <th className="px-6 py-4">Customer / Website</th>
                <th className="px-6 py-4">Task</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4">Assignee</th>
                <th className="px-6 py-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-ghost text-sm">
              {implementations.map((impl) => (
                <tr key={impl.id} className="hover:bg-ghost transition-colors">
                  <td className="px-6 py-4">
                    <p className="font-bold">{impl.customer}</p>
                    <p className="text-xs text-slate-deep/60">{impl.website}</p>
                  </td>
                  <td className="px-6 py-4">
                    <p className="font-medium">{impl.task}</p>
                    <p className="text-xs text-gold font-bold">${impl.price}</p>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                       {impl.status === 'Done' ? <CheckCircle className="w-4 h-4 text-success" /> : 
                        impl.status === 'In Progress' ? <Clock className="w-4 h-4 text-velvet-secondary" /> : 
                        <AlertCircle className="w-4 h-4 text-alert" />}
                       <span className="font-bold">{impl.status}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-slate-deep/60">{impl.assignedTo}</td>
                  <td className="px-6 py-4 text-right">
                    <button className="text-velvet-primary font-bold">Manage</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* System Health / Logs */}
        <div className="card">
          <h2 className="text-xl font-display text-velvet-primary mb-6">Recent Activity</h2>
          <div className="space-y-6">
            {[
              { time: '2m ago', action: 'Audit completed', target: 'flowers-by-mary.com', status: 'Success' },
              { time: '15m ago', action: 'New order', target: 'realty-group.net', status: '$299' },
              { time: '1h ago', action: 'Fix deployed', target: 'roof-experts.com', status: 'Live' },
              { time: '3h ago', action: 'Audit failed', target: 'complex-spa-app.io', status: 'Timeout' },
            ].map((log, i) => (
              <div key={i} className="flex gap-4 items-start pb-4 border-b border-ghost last:border-0">
                <div className={`mt-1 w-2 h-2 rounded-full ${log.status === 'Timeout' ? 'bg-alert' : 'bg-success'}`}></div>
                <div>
                  <p className="text-sm font-bold text-slate-deep">{log.action}</p>
                  <p className="text-xs text-slate-deep/60">{log.target}</p>
                  <div className="flex justify-between items-center mt-1">
                    <span className="text-[10px] uppercase font-bold text-slate-deep/40">{log.time}</span>
                    <span className={`text-[10px] font-bold ${log.status === 'Timeout' ? 'text-alert' : 'text-success'}`}>{log.status}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
          <button className="w-full mt-6 py-3 border-2 border-ghost rounded-lg text-sm font-bold text-slate-deep/40 hover:bg-ghost transition-colors">
            View Full System Logs
          </button>
        </div>
      </div>
    </div>
  );
};

export default AdminPanel;
