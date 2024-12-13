import { useState } from 'react';
import { sendFile } from '../../services/api';
import './FileTransferForm.css';
import logService from '../../services/LogService';

function FileTransferForm() {
  const [file, setFile] = useState(null);
  const [admin_node, setAdminNode] = useState('');
  const [target_node, setTargetNode] = useState('');
  const [polynomial, setPolynomial] = useState('');

  const handleSubmit = async (e) => {
    logService.clearLogs();
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
      alert('File sent successfully!');
    } catch (error) {
      console.error(error);
      alert('An error occurred while sending the file.');
    }
  };

  return (
    <div className="FileTransfer">
      <h2>Send a PDF</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <input
          type="text"
          placeholder="Admin Node"
          value={admin_node}
          onChange={(e) => setAdminNode(e.target.value)}
        />
        <input
          type="text"
          placeholder="Target Node"
          value={target_node}
          onChange={(e) => setTargetNode(e.target.value)}
        />
        <input
          type="text"
          placeholder="Polynomial (8-bit number)"
          value={polynomial}
          onChange={(e) => setPolynomial(e.target.value)}
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default FileTransferForm;
