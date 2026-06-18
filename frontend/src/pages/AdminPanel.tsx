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
    { id: 'impl_1', customer: 'sarah johnson', website: 'mysalon.com', task: 'add lead gen form', price: 29, status: 'Pending', assignedTo: 'Unassigned' },
    { id: 'impl_2', customer: 'mike miller', website: 'miller-roofing.com', task: 'mobile optimization', price: 149, status: 'In Progress', assignedTo: 'John Doe' },
    { id: 'impl_3', customer: 'mike miller', website: 'miller-roofing.com', task: 'alt text fixes', price: 29, status: 'Done', assignedTo: 'Jane Smith' },
  ];

  return (
    <div className="min-h-screen bg-background p-12 md:p-16 lg:p-24 font-sans">
      <header className="mb-20">
        <h1 className="text-4xl md:text-5xl mb-4 font-normal">admin <em className="italic">command center.</em></h1>
        <p className="text-text-muted font-light">manage operations, track revenue, and monitor implementations.</p>
      </header>

      <div className="hairline mb-20"></div>

      {/* Admin Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-16 mb-32">
        {[
          { icon: <Users className="w-4 h-4" />, label: 'active customers', value: '1,284', trend: '+12% this month' },
          { icon: <Activity className="w-4 h-4" />, label: 'audits run', value: '5,492', trend: '+24% this month' },
          { icon: <DollarSign className="w-4 h-4" />, label: 'monthly revenue', value: '$42,500', trend: '+18% this month' },
          { icon: <Wrench className="w-4 h-4" />, label: 'pending fixes', value: '42', trend: '-5% this month' },
        ].map((stat, i) => (
          <div key={i} className="space-y-6">
            <span className="section-label flex items-center gap-2">{stat.icon} {stat.label}</span>
            <div className="flex items-baseline gap-4">
              <span className="text-5xl font-display text-text-primary">{stat.value}</span>
            </div>
            <div className="h-px w-10 bg-gold/40"></div>
            <p className="text-success text-[0.6rem] uppercase tracking-widest font-bold">{stat.trend}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-24">
        {/* Implementation Queue */}
        <div className="lg:col-span-2 space-y-12">
          <div className="flex justify-between items-center border-b border-border pb-6">
            <h2 className="text-3xl font-normal">implementation <em className="italic">queue.</em></h2>
            <div className="flex gap-6">
               <button className="nav-link flex items-center gap-2">
                 <Filter className="w-3 h-3" /> filter
               </button>
               <button className="nav-link flex items-center gap-2">
                 <Search className="w-3 h-3" /> search
               </button>
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-border">
                  <th className="section-label pb-6">customer / website</th>
                  <th className="section-label pb-6">task</th>
                  <th className="section-label pb-6">status</th>
                  <th className="section-label pb-6">assignee</th>
                  <th className="section-label pb-6 text-right">manage</th>
                </tr>
              </thead>
              <tbody className="font-light">
                {implementations.map((impl) => (
                  <tr key={impl.id} className="border-b border-border/40">
                    <td className="py-8">
                      <p className="font-normal text-text-primary lowercase">{impl.customer}</p>
                      <p className="text-xs text-text-muted">{impl.website}</p>
                    </td>
                    <td className="py-8">
                      <p className="lowercase">{impl.task}</p>
                      <p className="text-xs text-gold font-bold">${impl.price}</p>
                    </td>
                    <td className="py-8">
                      <div className="flex items-center gap-2">
                         {impl.status === 'Done' ? <CheckCircle className="w-3 h-3 text-success" /> : 
                          impl.status === 'In Progress' ? <Clock className="w-3 h-3 text-gold" /> : 
                          <AlertCircle className="w-3 h-3 text-alert" />}
                         <span className="text-[0.65rem] uppercase tracking-widest font-medium">{impl.status}</span>
                      </div>
                    </td>
                    <td className="py-8 text-text-muted text-sm">{impl.assignedTo}</td>
                    <td className="py-8 text-right">
                      <button className="text-blush hover:underline text-sm uppercase tracking-widest">manage</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* System Health / Logs */}
        <div className="space-y-12">
          <h2 className="text-3xl font-normal border-b border-border pb-6">recent <em className="italic">activity.</em></h2>
          <div className="space-y-10">
            {[
              { time: '2m ago', action: 'audit completed', target: 'flowers-by-mary.com', status: 'Success' },
              { time: '15m ago', action: 'new order', target: 'realty-group.net', status: '$299' },
              { time: '1h ago', action: 'fix deployed', target: 'roof-experts.com', status: 'Live' },
              { time: '3h ago', action: 'audit failed', target: 'complex-spa-app.io', status: 'Timeout' },
            ].map((log, i) => (
              <div key={i} className="flex gap-6 items-start">
                <div className={`mt-2 w-1.5 h-1.5 rounded-full flex-shrink-0 ${log.status === 'Timeout' ? 'bg-alert' : 'bg-success'}`}></div>
                <div className="space-y-1">
                  <p className="text-sm font-normal text-text-primary lowercase">{log.action}</p>
                  <p className="text-xs text-text-muted font-light">{log.target}</p>
                  <div className="flex justify-between items-center pt-2">
                    <span className="text-[0.6rem] uppercase tracking-widest text-text-muted/60">{log.time}</span>
                    <span className={`text-[0.6rem] uppercase tracking-widest font-bold ${log.status === 'Timeout' ? 'text-alert' : 'text-success'}`}>{log.status}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
          <button className="w-full mt-12 btn-secondary py-3">
            view system logs
          </button>
        </div>
      </div>
    </div>
  );
};

export default AdminPanel;
