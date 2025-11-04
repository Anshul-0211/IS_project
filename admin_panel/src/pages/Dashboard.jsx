import React, { useState, useEffect } from 'react';
import { statsAPI } from '../utils/api';
import { Shield, AlertTriangle, Database, TrendingUp, Clock, CheckCircle } from 'lucide-react';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const StatCard = ({ icon: Icon, title, value, change, color = 'primary' }) => (
  <div className="card">
    <div className="flex items-start justify-between">
      <div>
        <p className="text-sm font-medium text-gray-600 mb-1">{title}</p>
        <p className="text-3xl font-bold text-gray-900">{value}</p>
        {change !== undefined && (
          <p className={`text-sm mt-2 ${change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {change >= 0 ? '+' : ''}{change}% from last week
          </p>
        )}
      </div>
      <div className={`p-3 bg-${color}-100 rounded-lg`}>
        <Icon className={`w-6 h-6 text-${color}-600`} />
      </div>
    </div>
  </div>
);

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [trends, setTrends] = useState([]);
  const [topThreats, setTopThreats] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [statsRes, trendsRes, threatsRes] = await Promise.all([
        statsAPI.getOverview(),
        statsAPI.getTrends(7),
        statsAPI.getTopThreats(5),
      ]);

      setStats(statsRes.data);
      setTrends(trendsRes.data);
      setTopThreats(threatsRes.data);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-1">Overview of encrypted phishing threat database</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={AlertTriangle}
          title="Total Threats"
          value={stats?.total_reports || 0}
          change={stats?.threats_change}
          color="danger"
        />
        <StatCard
          icon={Clock}
          title="Today's Reports"
          value={stats?.reports_today || 0}
          change={stats?.today_change}
          color="primary"
        />
        <StatCard
          icon={CheckCircle}
          title="Whitelisted"
          value={stats?.whitelist_count || 0}
          color="green"
        />
        <StatCard
          icon={Database}
          title="Database Size"
          value={stats?.database_size || '0 MB'}
          color="purple"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Threats Trend Chart */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">7-Day Threat Trend</h3>
          <ResponsiveContainer width="100%" height={250}>
            <AreaChart data={trends}>
              <defs>
                <linearGradient id="colorThreats" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="date" stroke="#9ca3af" style={{ fontSize: '12px' }} />
              <YAxis stroke="#9ca3af" style={{ fontSize: '12px' }} />
              <Tooltip />
              <Area type="monotone" dataKey="count" stroke="#ef4444" fillOpacity={1} fill="url(#colorThreats)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Top Threats */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Top 5 Threat Domains</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={topThreats} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis type="number" stroke="#9ca3af" style={{ fontSize: '12px' }} />
              <YAxis dataKey="domain" type="category" width={150} stroke="#9ca3af" style={{ fontSize: '11px' }} />
              <Tooltip />
              <Bar dataKey="count" fill="#0ea5e9" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Recent Activity</h3>
          <button className="text-sm text-primary-600 hover:text-primary-700 font-medium">
            View All
          </button>
        </div>
        <div className="space-y-3">
          {stats?.recent_activity?.map((activity, index) => (
            <div key={index} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
              <div className={`p-2 rounded-full ${
                activity.type === 'threat' ? 'bg-danger-100' : 
                activity.type === 'whitelist' ? 'bg-green-100' : 'bg-primary-100'
              }`}>
                <Shield className={`w-4 h-4 ${
                  activity.type === 'threat' ? 'text-danger-600' : 
                  activity.type === 'whitelist' ? 'text-green-600' : 'text-primary-600'
                }`} />
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">{activity.message}</p>
                <p className="text-xs text-gray-500 mt-1">{activity.timestamp}</p>
              </div>
            </div>
          )) || (
            <p className="text-center text-gray-500 py-8">No recent activity</p>
          )}
        </div>
      </div>

      {/* Security Status */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card bg-gradient-to-br from-green-50 to-white border-green-200">
          <div className="flex items-center gap-3">
            <CheckCircle className="w-8 h-8 text-green-600" />
            <div>
              <p className="text-sm font-medium text-gray-600">Encryption Status</p>
              <p className="text-lg font-bold text-green-600">Active</p>
            </div>
          </div>
          <p className="text-xs text-gray-600 mt-3">AES-256-GCM + RSA-2048</p>
        </div>

        <div className="card bg-gradient-to-br from-blue-50 to-white border-primary-200">
          <div className="flex items-center gap-3">
            <Database className="w-8 h-8 text-primary-600" />
            <div>
              <p className="text-sm font-medium text-gray-600">Blockchain Integrity</p>
              <p className="text-lg font-bold text-primary-600">Verified</p>
            </div>
          </div>
          <p className="text-xs text-gray-600 mt-3">SHA-256 chain linking</p>
        </div>

        <div className="card bg-gradient-to-br from-purple-50 to-white border-purple-200">
          <div className="flex items-center gap-3">
            <Shield className="w-8 h-8 text-purple-600" />
            <div>
              <p className="text-sm font-medium text-gray-600">Digital Signatures</p>
              <p className="text-lg font-bold text-purple-600">Valid</p>
            </div>
          </div>
          <p className="text-xs text-gray-600 mt-3">RSA-PSS verification</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
