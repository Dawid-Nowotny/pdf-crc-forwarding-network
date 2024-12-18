import { useState } from 'react';
import { startWebsockets, stopWebsockets, closeWebsocket } from '../../services/api';
import './SimulationControls.css';

function SimulationControls() {
  const [admin_node, setAdminNode] = useState('Node1'); 
  const [close_node, setCloseNode] = useState('Node1'); 

  const handleStart = async () => {
    await startWebsockets({ admin_node: admin_node });
    window.location.reload(); 
  };

  const handleStop = async () => {
    await stopWebsockets();
  };

  const handleClose = async () => {
    await closeWebsocket(close_node);
    window.location.reload(); 
  };

  return (
    <div class="SimulationControls">
      <div class="bar">Simulation Controls</div>
      <div class="content">
        <div class="form-container">
          <div>
            <label htmlFor="adminNode">Admin Node</label>
            <select
              id="adminNode"
              value={admin_node}
              onChange={(e) => setAdminNode(e.target.value)} 
            >
              <option value="Node1">Node1</option>
              <option value="Node2">Node2</option>
              <option value="Node3">Node3</option>
              <option value="Node4">Node4</option>
              <option value="Node5">Node5</option>
              <option value="Node6">Node6</option>
              <option value="Node7">Node7</option>
              <option value="Node8">Node8</option>
              <option value="Node9">Node9</option>
              <option value="Node10">Node10</option>
            </select>
          </div>

          <div class="buttoncontainer">
            <button class="button2" onClick={handleStart}>Start</button>
            <button class="button2" onClick={handleStop}>Stop</button>
          </div>
        </div>
        <div class="form-container" style={{ marginTop: '30px' }}>
          <div>
            <label htmlFor="closeNode">Node to close</label>
            <select
              id="closeNode"
              value={close_node}
              onChange={(e) => setCloseNode(e.target.value)} 
            >
              <option value="Node1">Node1</option>
              <option value="Node2">Node2</option>
              <option value="Node3">Node3</option>
              <option value="Node4">Node4</option>
              <option value="Node5">Node5</option>
              <option value="Node6">Node6</option>
              <option value="Node7">Node7</option>
              <option value="Node8">Node8</option>
              <option value="Node9">Node9</option>
              <option value="Node10">Node10</option>
            </select>
          </div>
          <button class="button" onClick={handleClose}>Close</button>
        </div>
      </div>
    </div>
  );
}

export default SimulationControls;