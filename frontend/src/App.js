import './App.css';
import Header from './components/Header/Header';
import SimulationControls from './components/SimulationControls/SimulationControls';
import FileTransfer from './components/FileTransferForm/FileTransferForm';
import Logs from './components/Logs/Logs';
import Graph from './components/Graph/Graph';

function App() {
  return (
    <div className="App">
      <Header />
      <div class="AppContainer">
        <div class="AppLeft">
          <div class="bar_graph">Simulation Controls</div>
          <Graph />
        </div>
        <div class="AppRight">
          <SimulationControls />
          <FileTransfer />
          <Logs />
        </div>
      </div>
    </div>
  );
}

export default App;
