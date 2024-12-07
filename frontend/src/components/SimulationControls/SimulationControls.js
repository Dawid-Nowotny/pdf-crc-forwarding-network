import { startWebsockets, stopWebsockets } from '../../services/api';
import './SimulationControls.css';

function SimulationControls() {

  const handleStart = async () => {
    await startWebsockets({ admin_node: 'Node1' });
    window.location.reload();
  };

  const handleStop = async () => {
    await stopWebsockets();
  };

  return (
    <div className="SimulationControls">
      <h2>Simulation Controls</h2>
      <button onClick={handleStart}>Start</button>
      <button onClick={handleStop}>Stop</button>
    </div>
  );
}

export default SimulationControls;
