import React, { useState, useEffect } from 'react';
import logService from '../../services/LogService';
import './Logs.css';

const Logs = () => {
  const [logs, setLogs] = useState([]);
  const [expandedLogs, setExpandedLogs] = useState({});
  const [message, setMessage] = useState('');
  const [type, setType] = useState(''); 
  const [showMessage, setShowMessage] = useState(false);

  const handleAddMessage = (message, type) => {
    setMessage(message);
    setType(type);
    setShowMessage(true);
  };

  useEffect(() => {
    if (showMessage) {
      const timer = setTimeout(() => {
        setShowMessage(false);
      }, 5000); 
      return () => clearTimeout(timer);
    }
  }, [showMessage]);


  useEffect(() => {
    const handleNewLogs = (newLogs) => {
      setLogs([...newLogs]);

      const errorLog = newLogs.find(
        (log) => log.status === 'ERROR' || log.status === 'CONNECTION_FAILED'
      );
      if (errorLog) {
        let errorMessage = errorLog.details?.message || 'An error occurred.';
        handleAddMessage(errorMessage, 'error');
      }

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
      {showMessage && (
        <div class="MessageBarContainer"><div class={type === 'success' ? 'MessageBar' : 'MessageBarError'}>{message}</div></div>
      )}
      <div class="bar">Logs</div>
      <div className="log-container">
        {logs.map((log, index) => (
          <div key={index} className="log-entry">
           <div className="expand-container">
              <span>
                <strong>Received: </strong>
                {"{"} 
                {log.node ? "node" : "target node"}: "{log.node || log.details?.target_node}", status: "{log.status}"
                {"}"}
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
