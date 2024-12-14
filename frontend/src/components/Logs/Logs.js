import React, { useState, useEffect } from 'react';
import logService from '../../services/LogService';
import './Logs.css';

const Logs = () => {
  const [logs, setLogs] = useState([]);
  const [expandedLogs, setExpandedLogs] = useState({});

  useEffect(() => {
    const handleNewLogs = (newLogs) => {
      setLogs([...newLogs]);
    };

    logService.subscribe(handleNewLogs);

    logService.openConnection();

    return () => {
      logService.unsubscribe(handleNewLogs);
      logService.closeConnection();
    };
  }, []);

  const toggleExpandLog = (index) => {
    setExpandedLogs((prevExpandedLogs) => ({
      ...prevExpandedLogs,
      [index]: !prevExpandedLogs[index],
    }));
  };

  return (
    <div className="Logs">
      <h2>Logs</h2>
      <div className="log-container">
        {logs.map((log, index) => (
          <div key={index} className="log-entry">
            <div>
              <span>
                <strong>Received:</strong> {"{"}node: "{log.node}", status: "{log.status}"{"}"}
              </span>
              <button
                onClick={() => toggleExpandLog(index)}
                className="expand-button"
              >
                {expandedLogs[index] ? 'Collapse' : 'Expand'}
              </button>
            </div>

            {expandedLogs[index] && (
              <pre className="expanded-log">
                {JSON.stringify(log, null, 2)}
              </pre>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Logs;
