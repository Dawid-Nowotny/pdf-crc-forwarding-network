import { useState } from 'react';
import { sendFile } from '../../services/api';
import './FileTransferForm.css';
import logService from '../../services/LogService';

function FileTransferForm() {
  const [file, setFile] = useState(null);
  const [admin_node, setAdminNode] = useState('Node1');
  const [target_node, setTargetNode] = useState('Node5');
  const [polynomial, setPolynomial] = useState('11111111');
  
  const handleSubmit = async (e) => {
    logService.clearLogs();
    logService.setShouldColorGraph(false);
    e.preventDefault();

    if (!file || !admin_node || !target_node || !polynomial) {
      alert('Please fill in all fields');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('admin_node', admin_node);
    formData.append('target_node', target_node);
    formData.append('polynomial', polynomial);

    try {
      await sendFile(formData);
      setTimeout(() => {
        logService.setShouldColorGraph(true);
      }, 100);
      alert('File sent successfully!');
    } catch (error) {
      console.error(error);
      alert('An error occurred while sending the file.');
    }
  };

  return (
    <div className="FileTransfer">
      <div className="bar">Send a PDF</div>
      <div className="content">
        <form className="form-container" onSubmit={handleSubmit}>
          <div>
            <label htmlFor="fileInput">PDF File</label>
            <input
              id="fileInput"
              style={{ padding: '7px' }}
              type="file"
              accept="application/pdf"
              onChange={(e) => setFile(e.target.files[0])}
            />
          </div>

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

          <div>
            <label htmlFor="targetNode">Target Node</label>
            <select
              id="targetNode"
              value={target_node}
              onChange={(e) => setTargetNode(e.target.value)}
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

          <div>
            <label htmlFor="polynomial">Polynomial (8-bit number)</label>
            <input
              id="polynomial"
              type="text"
              placeholder="Polynomial (8-bit number)"
              value={polynomial}
              onChange={(e) => setPolynomial(e.target.value)}
            />
          </div>

          <button type="submit">Send</button>
        </form>
      </div>
    </div>
  );
}

export default FileTransferForm;
