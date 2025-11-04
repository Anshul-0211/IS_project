import React, { useState, useEffect } from 'react';
import { auditAPI } from '../utils/api';
import { Download, Filter, Clock, User, Activity } from 'lucide-react';

const AuditLogs = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterAction, setFilterAction] = useState('all');

  useEffect(() => {
    loadLogs();
  }, []);

  const loadLogs = async () => {
    try {
      const response = await auditAPI.getAll(100, 0);
      setLogs(response.data.logs || []);
    } catch (error) {
      console.error('Failed to load audit logs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    try {
      const response = await auditAPI.export();
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `audit_logs_${new Date().toISOString().split('T')[0]}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Failed to export logs:', error);
    }
  };

  const filteredLogs = logs.filter(log => 
    filterAction === 'all' || log.action === filterAction
  );

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const getActionColor = (action) => {
    const colors = {
      'login': 'bg-green-100 text-green-700',
      'logout': 'bg-gray-100 text-gray-700',
      'view_report': 'bg-blue-100 text-blue-700',
      'decrypt_report': 'bg-purple-100 text-purple-700',
      'add_whitelist': 'bg-green-100 text-green-700',
      'remove_whitelist': 'bg-red-100 text-red-700',
      'export_data': 'bg-yellow-100 text-yellow-700',
    };
    return colors[action] || 'bg-gray-100 text-gray-700';
  };

  const getActionIcon = (action) => {
    if (action.includes('decrypt') || action.includes('view')) return '👁️';
    if (action.includes('add')) return '➕';
    if (action.includes('remove')) return '🗑️';
    if (action.includes('login')) return '🔑';
    if (action.includes('export')) return '📥';
    return '📝';
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
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Audit Logs</h1>
          <p className="text-gray-600 mt-1">Track all administrative actions</p>
        </div>
        <button onClick={handleExport} className="btn-primary flex items-center gap-2">
          <Download className="w-4 h-4" />
          Export Logs
        </button>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="flex items-center gap-4">
          <Filter className="w-5 h-5 text-gray-600" />
          <select
            value={filterAction}
            onChange={(e) => setFilterAction(e.target.value)}
            className="input-field"
          >
            <option value="all">All Actions</option>
            <option value="login">Login</option>
            <option value="logout">Logout</option>
            <option value="view_report">View Report</option>
            <option value="decrypt_report">Decrypt Report</option>
            <option value="add_whitelist">Add Whitelist</option>
            <option value="remove_whitelist">Remove Whitelist</option>
            <option value="export_data">Export Data</option>
          </select>
          <span className="text-sm text-gray-600">
            Showing {filteredLogs.length} of {logs.length} logs
          </span>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card bg-gradient-to-br from-blue-50 to-white border-blue-200">
          <div className="flex items-center gap-3">
            <Activity className="w-8 h-8 text-blue-600" />
            <div>
              <p className="text-sm font-medium text-gray-600">Total Actions</p>
              <p className="text-2xl font-bold text-blue-600">{logs.length}</p>
            </div>
          </div>
        </div>

        <div className="card bg-gradient-to-br from-green-50 to-white border-green-200">
          <div className="flex items-center gap-3">
            <User className="w-8 h-8 text-green-600" />
            <div>
              <p className="text-sm font-medium text-gray-600">Active Users</p>
              <p className="text-2xl font-bold text-green-600">
                {new Set(logs.map(l => l.username)).size}
              </p>
            </div>
          </div>
        </div>

        <div className="card bg-gradient-to-br from-purple-50 to-white border-purple-200">
          <div className="flex items-center gap-3">
            <Clock className="w-8 h-8 text-purple-600" />
            <div>
              <p className="text-sm font-medium text-gray-600">Today's Activity</p>
              <p className="text-2xl font-bold text-purple-600">
                {logs.filter(l => {
                  const logDate = new Date(l.timestamp).toDateString();
                  const today = new Date().toDateString();
                  return logDate === today;
                }).length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Logs Timeline */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Activity Timeline</h3>
        
        <div className="space-y-4">
          {filteredLogs.length === 0 ? (
            <div className="text-center py-12">
              <Activity className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600">No audit logs found</p>
            </div>
          ) : (
            filteredLogs.map((log, index) => (
              <div key={index} className="flex items-start gap-4 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                <div className="text-2xl">{getActionIcon(log.action)}</div>
                
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-1">
                    <span className={`text-xs font-semibold px-3 py-1 rounded-full ${getActionColor(log.action)}`}>
                      {log.action.replace(/_/g, ' ').toUpperCase()}
                    </span>
                    <span className="text-xs text-gray-500 flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {formatDate(log.timestamp)}
                    </span>
                  </div>
                  
                  <p className="text-sm text-gray-900 font-medium mb-1">
                    <span className="font-semibold text-primary-600">{log.username}</span>
                    {' '}{log.description || `performed ${log.action}`}
                  </p>
                  
                  {log.details && (
                    <p className="text-xs text-gray-600 font-mono bg-white px-2 py-1 rounded mt-2 inline-block">
                      {log.details}
                    </p>
                  )}
                  
                  {log.ip_address && (
                    <p className="text-xs text-gray-500 mt-1">
                      IP: {log.ip_address}
                    </p>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default AuditLogs;
