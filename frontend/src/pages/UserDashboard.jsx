import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function UserDashboard() {
  const [assetType, setAssetType] = useState('');
  const [requestType, setRequestType] = useState('');
  const [requestedBy, setRequestedBy] = useState('');
  const [quantity, setQuantity] = useState('');
  const [urgency, setUrgency] = useState('');
  const [reason, setReason] = useState('');
  const [status, setStatus] = useState('Pending');
  const [createdAt, setCreatedAt] = useState('');
  const [requests, setRequests] = useState([]);
  const [assets, setAssets] = useState([]);
  const [activeSection, setActiveSection] = useState('viewRequests');
  const navigate = useNavigate();

  useEffect(() => {
    const currentTimestamp = new Date().toISOString();
    setCreatedAt(currentTimestamp);

    const fetchData = async () => {
      try {
        const [assetsResponse, requestsResponse] = await Promise.all([
          axios.get('http://localhost:3000/Assets'),
          axios.get('http://localhost:3000/Requests'),
        ]);

        setAssets(assetsResponse.data);
        setRequests(requestsResponse.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newRequest = {
      id: requests.length + 1,
      request_type: requestType,
      quantity,
      urgency,
      reason,
      status,
      created_at: createdAt,
    };

    try {
      await axios.post('http://localhost:3000/Requests', newRequest);
      setRequests([...requests, newRequest]);
      handleCancel();
      setActiveSection('viewRequests'); // Redirect to view requests after submission
    } catch (error) {
      console.error("Error submitting request:", error);
    }
  };

  const handleCancel = () => {
    setAssetType('');
    setRequestType('');
    setRequestedBy('');
    setQuantity('');
    setUrgency('');
    setReason('');
  };

  const handleLogout = () => {
    navigate('/');
  };

  return (
    <div style={styles.container}>
      <div style={styles.sidebar}>
        <h2 style={styles.sidebarTitle}>User Dashboard</h2>
        <ul style={styles.navList}>
          <li style={styles.navItem} onClick={() => setActiveSection('viewRequests')}>
            View My Requests
          </li>
          <li style={styles.navItem} onClick={() => setActiveSection('viewAssets')}>
            View All Assets
          </li>
          <li style={styles.navItem} onClick={() => setActiveSection('makeRequest')}>
            Make a New Request
          </li>
          <button onClick={handleLogout} style={styles.logoutButton}>Logout</button>
        </ul>
      </div>

      <div style={styles.content}>
        <h1>User Dashboard</h1>
        
        {activeSection === 'viewRequests' ? (
          <div style={styles.tableContainer}>
            <h2>My Requests</h2>
            <table style={styles.table}>
              <thead>
                <tr>
                  <th style={styles.tableHeader}>Type</th>
                  <th style={styles.tableHeader}>Quantity</th>
                  <th style={styles.tableHeader}>Urgency</th>
                  <th style={styles.tableHeader}>Reason</th>
                  <th style={styles.tableHeader}>Status</th>
                  <th style={styles.tableHeader}>Date</th>
                </tr>
              </thead>
              <tbody>
                {requests.map((request) => (
                  <tr key={request.id}>
                    <td style={styles.tableCell}>{request.request_type}</td>
                    <td style={styles.tableCell}>{request.quantity}</td>
                    <td style={styles.tableCell}>{request.urgency}</td>
                    <td style={styles.tableCell}>{request.reason}</td>
                    <td style={styles.tableCell}>{request.status}</td>
                    <td style={styles.tableCell}>{new Date(request.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : activeSection === 'viewAssets' ? (
          <div style={styles.assetContainer}>
            <h2>All Assets</h2>
            {assets.length > 0 ? (
              <ul style={styles.assetList}>
                {assets.map(asset => (
                  <li key={asset.id} style={styles.assetItem}>
                    <img src={asset.image_url} alt={asset.asset_name} style={styles.assetImage} />
                    <h4>{asset.asset_name}</h4>
                    <p>{asset.description}</p>
                    <span>Status: {asset.status}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p>No assets available.</p>
            )}
          </div>
        ) : (
          <form onSubmit={handleSubmit} style={styles.form}>
            <h2>Create Request</h2>
            
            <label style={styles.label}>Asset Type</label>
            <select
              value={assetType}
              onChange={(e) => setAssetType(e.target.value)}
              style={styles.input}
            >
              <option value="">Select Asset Type</option>
              <option value="Laptop">Laptop</option>
              <option value="Chair">Chair</option>
              <option value="Table">Table</option>
              <option value="Projector">Projector</option>
            </select>

            <label style={styles.label}>Request Type</label>
            <select
              value={requestType}
              onChange={(e) => setRequestType(e.target.value)}
              style={styles.input}
            >
              <option value="">Select Request Type</option>
              <option value="New Asset">New Asset</option>
              <option value="Repair">Repair</option>
            </select>

            <label style={styles.label}>Requested By (Department)</label>
            <select
              value={requestedBy}
              onChange={(e) => setRequestedBy(e.target.value)}
              style={styles.input}
            >
              <option value="">Select Department</option>
              <option value="IT">IT</option>
              <option value="HR">HR</option>
              <option value="Finance">Finance</option>
              <option value="Marketing">Marketing</option>
            </select>

            <label style={styles.label}>Quantity</label>
            <input
              type="number"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
              style={styles.input}
            />

            <label style={styles.label}>Urgency</label>
            <select
              value={urgency}
              onChange={(e) => setUrgency(e.target.value)}
              style={styles.input}
            >
              <option value="">Select Urgency</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>

            <label style={styles.label}>Reason</label>
            <input
              type="text"
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              style={styles.input}
            />

            <label style={styles.label}>Status</label>
            <input
              type="text"
              value={status}
              readOnly
              style={styles.input}
            />

            <label style={styles.label}>Created/Updated at</label>
            <input
              type="text"
              value={createdAt}
              readOnly
              style={styles.input}
            />

            <div style={styles.buttonContainer}>
              <button type="button" onClick={handleCancel} style={styles.cancelButton}>
                Cancel
              </button>
              <button type="submit" style={styles.submitButton}>
                Submit
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    height: '100vh',
  },
  sidebar: {
    width: '250px',
    backgroundColor: '#2C3E50',
    padding: '20px',
    color: '#ECF0F1',
    display: 'flex',
    flexDirection: 'column',
  },
  sidebarTitle: {
    fontSize: '24px',
    marginBottom: '20px',
  },
  navList: {
    listStyle: 'none',
    padding: 0,
  },
  navItem: {
    cursor: 'pointer',
    padding: '10px 0',
    fontSize: '18px',
    color: '#bdc3c7',
    transition: 'color 0.2s',
  },
  logoutButton: {
    marginTop: '20px',
    padding: '10px',
    backgroundColor: '#e74c3c',
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  },
  content: {
    flexGrow: 1,
    padding: '20px',
  },
  assetContainer: {
    backgroundColor: '#2C3E50',
    padding: '20px',
    borderRadius: '10px',
    color: '#ECF0F1',
  },
  assetList: {
    listStyle: 'none',
    display: 'flex',
    flexWrap: 'wrap',
    gap: '10px',
    padding: 0,
  },
  assetItem: {
    width: '150px',
    padding: '10px',
    backgroundColor: '#fff',
    color: '#333',
    borderRadius: '5px',
    textAlign: 'center',
  },
  assetImage: {
    width: '100%',
    height: '100px',
    objectFit: 'cover',
  },
  form: {
    backgroundColor: '#2C3E50',
    padding: '20px',
    borderRadius: '10px',
    color: '#ECF0F1',
  },
  tableContainer: {
    backgroundColor: '#2C3E50',
    padding: '20px',
    borderRadius: '10px',
    color: '#ECF0F1',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
  },
  tableHeader: {
    backgroundColor: '#34495e',
    color: '#ECF0F1',
    padding: '10px',
  },
  tableCell: {
    padding: '10px',
    border: '1px solid #34495e',
  },
  label: {
    display: 'block',
    marginBottom: '5px',
    fontWeight: 'bold',
  },
  input: {
    width: '100%',
    padding: '10px',
    borderRadius: '5px',
    marginBottom: '15px',
    border: '1px solid #ccc',
  },
  buttonContainer: {
    display: 'flex',
    justifyContent: 'space-between',
  },
  cancelButton: {
    padding: '10px 20px',
    backgroundColor: '#e74c3c',
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  },
  submitButton: {
    padding: '10px 20px',
    backgroundColor: '#2ecc71',
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  },
};

export default UserDashboard;
