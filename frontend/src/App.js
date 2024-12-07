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
      <Graph />
      <SimulationControls />
      <FileTransfer />
      <Logs />
    </div>
  );
}

export default App;
