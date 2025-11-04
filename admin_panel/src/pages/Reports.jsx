import React, { useState, useEffect } from 'react';
import { reportsAPI } from '../utils/api';
import { Search, Download, Lock, Unlock, ExternalLink, Calendar, Shield, AlertTriangle } from 'lucide-react';

const Reports = () => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [decryptedData, setDecryptedData] = useState({});
  const [decrypting, setDecrypting] = useState({});

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    try {
      const response = await reportsAPI.getAll(50, 0);
      setReports(response.data.reports || []);
    } catch (error) {
      console.error('Failed to load reports:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDecrypt = async (reportId) => {
    setDecrypting({ ...decrypting, [reportId]: true });
    try {
      const response = await reportsAPI.decrypt(reportId);
      setDecryptedData({ 
        ...decryptedData, 
        [reportId]: response.data 
      });
    } catch (error) {
      console.error('Failed to decrypt report:', error);
      alert('Failed to decrypt report: ' + (error.response?.data?.error || 'Unknown error'));
    } finally {
      setDecrypting({ ...decrypting, [reportId]: false });
    }
  };

  const handleExport = async () => {
    try {
      const response = await reportsAPI.export();
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `phishing_reports_${new Date().toISOString().split('T')[0]}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Failed to export reports:', error);
    }
  };

  const filteredReports = reports.filter(report => {
    if (!searchQuery) return true;
    const decrypted = decryptedData[report.id];
    return decrypted?.url?.toLowerCase().includes(searchQuery.toLowerCase());
  });

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
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
          <h1 className="text-3xl font-bold text-gray-900">Encrypted Reports</h1>
          <p className="text-gray-600 mt-1">View and decrypt phishing threat data</p>
        </div>
        <button onClick={handleExport} className="btn-primary flex items-center gap-2">
          <Download className="w-4 h-4" />
          Export Data
        </button>
      </div>

      {/* Search Bar */}
      <div className="card">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search by URL (decrypt first to search)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="input-field pl-10"
          />
        </div>
      </div>

      {/* Reports List */}
      <div className="space-y-4">
        {filteredReports.length === 0 ? (
          <div className="card text-center py-12">
            <AlertTriangle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No reports found</p>
          </div>
        ) : (
          filteredReports.map((report) => {
            const decrypted = decryptedData[report.id];
            const isDecrypted = !!decrypted;

            return (
              <div key={report.id} className="card hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between gap-4">
                  {/* Left: Report Info */}
                  <div className="flex-1">
                    <div className="flex items-start gap-3 mb-3">
                      <div className={`p-2 rounded-lg ${isDecrypted ? 'bg-green-100' : 'bg-gray-100'}`}>
                        {isDecrypted ? (
                          <Unlock className="w-5 h-5 text-green-600" />
                        ) : (
                          <Lock className="w-5 h-5 text-gray-600" />
                        )}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-xs font-mono bg-gray-100 px-2 py-1 rounded">
                            ID: {report.id}
                          </span>
                          <span className="text-xs text-gray-500 flex items-center gap-1">
                            <Calendar className="w-3 h-3" />
                            {formatDate(report.timestamp)}
                          </span>
                        </div>
                        
                        {isDecrypted ? (
                          <div className="space-y-2">
                            <div className="flex items-center gap-2">
                              <ExternalLink className="w-4 h-4 text-danger-600" />
                              <a 
                                href={decrypted.url} 
                                target="_blank" 
                                rel="noopener noreferrer"
                                className="text-danger-600 hover:text-danger-700 font-medium break-all"
                              >
                                {decrypted.url}
                              </a>
                            </div>
                            
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mt-3">
                              <div className="bg-danger-50 p-3 rounded-lg">
                                <p className="text-xs text-gray-600 mb-1">Threat Probability</p>
                                <p className="text-lg font-bold text-danger-600">
                                  {(decrypted.metadata?.probability * 100).toFixed(1)}%
                                </p>
                              </div>
                              
                              <div className="bg-blue-50 p-3 rounded-lg">
                                <p className="text-xs text-gray-600 mb-1">Detection Source</p>
                                <p className="text-sm font-semibold text-blue-600">
                                  {decrypted.metadata?.source || 'ML Model'}
                                </p>
                              </div>
                              
                              <div className="bg-purple-50 p-3 rounded-lg">
                                <p className="text-xs text-gray-600 mb-1">VirusTotal Reports</p>
                                <p className="text-lg font-bold text-purple-600">
                                  {decrypted.metadata?.virustotal_reports || 0}
                                </p>
                              </div>
                            </div>

                            {/* Blockchain Info */}
                            <div className="bg-gray-50 p-3 rounded-lg mt-3">
                              <div className="flex items-center gap-2 mb-2">
                                <Shield className="w-4 h-4 text-primary-600" />
                                <p className="text-xs font-semibold text-gray-700">Blockchain Data</p>
                              </div>
                              <div className="grid grid-cols-2 gap-2 text-xs">
                                <div>
                                  <span className="text-gray-600">Block Hash:</span>
                                  <p className="font-mono text-gray-900 truncate">
                                    {report.block_hash?.substring(0, 16)}...
                                  </p>
                                </div>
                                <div>
                                  <span className="text-gray-600">Previous Hash:</span>
                                  <p className="font-mono text-gray-900 truncate">
                                    {report.previous_hash?.substring(0, 16)}...
                                  </p>
                                </div>
                              </div>
                              <div className="mt-2">
                                <span className={`inline-flex items-center gap-1 text-xs px-2 py-1 rounded ${
                                  decrypted.signature_valid 
                                    ? 'bg-green-100 text-green-700' 
                                    : 'bg-red-100 text-red-700'
                                }`}>
                                  {decrypted.signature_valid ? '✓ Signature Valid' : '✗ Signature Invalid'}
                                </span>
                              </div>
                            </div>
                          </div>
                        ) : (
                          <div className="bg-gray-100 p-4 rounded-lg">
                            <p className="text-sm text-gray-600 flex items-center gap-2">
                              <Lock className="w-4 h-4" />
                              Encrypted data - Click decrypt to view details
                            </p>
                            <p className="text-xs text-gray-500 mt-2 font-mono">
                              Encrypted URL: {report.encrypted_url?.substring(0, 40)}...
                            </p>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Right: Actions */}
                  <div>
                    {!isDecrypted ? (
                      <button
                        onClick={() => handleDecrypt(report.id)}
                        disabled={decrypting[report.id]}
                        className="btn-primary flex items-center gap-2 whitespace-nowrap"
                      >
                        {decrypting[report.id] ? (
                          <>
                            <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                            </svg>
                            Decrypting...
                          </>
                        ) : (
                          <>
                            <Unlock className="w-4 h-4" />
                            Decrypt
                          </>
                        )}
                      </button>
                    ) : (
                      <span className="inline-flex items-center gap-2 text-sm text-green-600 font-medium">
                        <Shield className="w-4 h-4" />
                        Decrypted
                      </span>
                    )}
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Pagination Info */}
      {reports.length > 0 && (
        <div className="text-center text-sm text-gray-600">
          Showing {filteredReports.length} of {reports.length} reports
        </div>
      )}
    </div>
  );
};

export default Reports;
