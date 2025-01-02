import React, { useState, useEffect } from 'react';
import { Network, User, AlertTriangle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card.jsx';  // Note the .jsx extension and ./

const PatternDashboard = () => {
  const [patterns, setPatterns] = useState({
    company_network_patterns: [],
    user_repeat_patterns: []
  });

  useEffect(() => {
    const fetchPatterns = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/patterns');
        const data = await response.json();
        setPatterns(data);
      } catch (error) {
        console.error('Error fetching patterns:', error);
      }
    };

    fetchPatterns();
    const interval = setInterval(fetchPatterns, 5 * 60 * 1000); // Refresh every 5 minutes
    return () => clearInterval(interval);
  }, []);

  const NetworkPatternCard = ({ pattern }) => (
    <Card className="mb-4">
      <CardContent className="p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <Network className="h-6 w-6 text-red-500" />
            <div>
              <h3 className="font-semibold text-lg">{pattern.company}</h3>
              <p className="text-sm text-gray-500">Network Issues Detected</p>
            </div>
          </div>
          <span className={`px-3 py-1 rounded-full text-sm ${
            pattern.alert_level === 'high' 
              ? 'bg-red-100 text-red-800' 
              : 'bg-yellow-100 text-yellow-800'
          }`}>
            {pattern.alert_level.toUpperCase()}
          </span>
        </div>
        <div className="space-y-2">
          <p><strong>{pattern.ticket_count}</strong> network-related tickets in the last 3 days</p>
          <p className="text-sm text-gray-600">
            First reported: {new Date(pattern.first_occurrence).toLocaleString()}
          </p>
          <p className="text-sm text-gray-600">
            Most recent: {new Date(pattern.last_occurrence).toLocaleString()}
          </p>
          <div className="mt-4">
            <h4 className="font-medium mb-2">Recent Tickets:</h4>
            <div className="space-y-2">
              {pattern.tickets.slice(0, 3).map((ticket, i) => (
                <div key={i} className="text-sm text-gray-600 pl-4 border-l-2 border-gray-200">
                  {ticket.summary}
                </div>
              ))}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );

  const UserPatternCard = ({ pattern }) => (
    <Card className="mb-4">
      <CardContent className="p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <User className="h-6 w-6 text-blue-500" />
            <div>
              <h3 className="font-semibold text-lg">{pattern.user}</h3>
              <p className="text-sm text-gray-500">Repeated {pattern.issue_type} Issues</p>
            </div>
          </div>
          <span className={`px-3 py-1 rounded-full text-sm ${
            pattern.ticket_count >= 3 
              ? 'bg-red-100 text-red-800' 
              : 'bg-yellow-100 text-yellow-800'
          }`}>
            {pattern.ticket_count} Tickets
          </span>
        </div>
        <div className="space-y-2">
          <p>
            Submitted <strong>{pattern.ticket_count}</strong> tickets about{' '}
            <strong>{pattern.issue_type}</strong> in the last 3 days
          </p>
          <p className="text-sm text-gray-600">
            First ticket: {new Date(pattern.first_occurrence).toLocaleString()}
          </p>
          <p className="text-sm text-gray-600">
            Latest ticket: {new Date(pattern.last_occurrence).toLocaleString()}
          </p>
          <div className="mt-4">
            <h4 className="font-medium mb-2">Ticket History:</h4>
            <div className="space-y-2">
              {pattern.tickets.map((ticket, i) => (
                <div key={i} className="text-sm text-gray-600 pl-4 border-l-2 border-gray-200">
                  {ticket.summary}
                </div>
              ))}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );

  return (
    <div className="p-8 max-w-7xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold">Pattern Detection Dashboard</h1>
        <div className="text-sm text-gray-500">
          Updated: {new Date().toLocaleString()}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Company Network Issues */}
        <div>
          <div className="flex items-center space-x-2 mb-6">
            <Network className="h-5 w-5" />
            <h2 className="text-xl font-semibold">Company Network Issues</h2>
          </div>
          {patterns.company_network_patterns.length > 0 ? (
            patterns.company_network_patterns.map((pattern, i) => (
              <NetworkPatternCard key={i} pattern={pattern} />
            ))
          ) : (
            <Card>
              <CardContent className="p-6 text-center text-gray-500">
                No network issues detected
              </CardContent>
            </Card>
          )}
        </div>

        {/* User Repeat Issues */}
        <div>
          <div className="flex items-center space-x-2 mb-6">
            <User className="h-5 w-5" />
            <h2 className="text-xl font-semibold">Repeated User Issues</h2>
          </div>
          {patterns.user_repeat_patterns.length > 0 ? (
            patterns.user_repeat_patterns.map((pattern, i) => (
              <UserPatternCard key={i} pattern={pattern} />
            ))
          ) : (
            <Card>
              <CardContent className="p-6 text-center text-gray-500">
                No user patterns detected
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default PatternDashboard;