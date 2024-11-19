import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function AdminDashboard() {
  const navigate = useNavigate();
  const [assets, setAssets] = useState([]);
  const [requests, setRequests] = useState([]);
  const [selectedSection, setSelectedSection] = useState('viewAssets');
  const [newAsset, setNewAsset] = useState({
    asset_name: '',
    description: '',
    category_id: '',
    condition: '',
    status: 'Available',
    department_id: '',
  });
  const [editingAsset, setEditingAsset] = useState(null);
  const [sortKey, setSortKey] = useState('');
  const [filterCategory, setFilterCategory] = useState('');
  const [filterCondition, setFilterCondition] = useState('');

  useEffect(() => {
    if (selectedSection === 'viewAssets' || selectedSection === 'manageAssets') {
      fetchAssets();
    }
    if (selectedSection === 'viewRequests') {
      fetchRequests();
    }
  }, [selectedSection]);

  const fetchAssets = async () => {
    try {
      const response = await axios.get('http://localhost:3000/Assets');
      setAssets(response.data);
    } catch (error) {
      console.error("Error fetching assets:", error);
    }
  };

  const fetchRequests = async () => {
    try {
      const response = await axios.get('http://localhost:3000/Requests');
      setRequests(response.data);
    } catch (error) {
      console.error("Error fetching requests:", error);
    }
  };

  const handleSectionChange = (section) => {
    setSelectedSection(section);
  };

  const handleLogout = () => {
    navigate('/');
  };

  const handleAddAsset = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:3000/Assets', newAsset);
      fetchAssets();
      setNewAsset({ asset_name: '', description: '', category_id: '', condition: '', status: 'Available', department_id: '' });
    } catch (error) {
      console.error("Error adding asset:", error);
    }
  };

  const handleEditAsset = (asset) => {
    setEditingAsset(asset);
  };

  const handleUpdateAsset = async (e) => {
    e.preventDefault();
    try {
      await axios.put(`http://localhost:3000/Assets/${editingAsset.id}`, editingAsset);
      fetchAssets();
      setEditingAsset(null);
    } catch (error) {
      console.error("Error updating asset:", error);
    }
  };

  const handleDeleteAsset = async (id) => {
    try {
      await axios.delete(`http://localhost:3000/Assets/${id}`);
      fetchAssets();
    } catch (error) {
      console.error("Error deleting asset:", error);
    }
  };

  const handleApprove = async (id) => {
    try {
      await axios.patch(`http://localhost:3000/Requests/${id}`, { status_id: 2 }); // 2 for Approved
      fetchRequests();
    } catch (error) {
      console.error("Error approving request:", error);
    }
  };

  const handleReject = async (id) => {
    try {
      await axios.patch(`http://localhost:3000/Requests/${id}`, { status_id: 3 }); // 3 for Rejected
      fetchRequests();
    } catch (error) {
      console.error("Error rejecting request:", error);
    }
  };

  const handleSort = (e) => {
    setSortKey(e.target.value);
  };

  const handleFilterCategory = (e) => {
    setFilterCategory(e.target.value);
  };

  const handleFilterCondition = (e) => {
    setFilterCondition(e.target.value);
  };

  const filteredAssets = assets.filter(asset => {
    const categoryMatch = filterCategory ? asset.category_id === filterCategory : true;
    const conditionMatch = filterCondition ? asset.condition === filterCondition : true;
    return categoryMatch && conditionMatch;
  });

  const sortedAssets = filteredAssets.sort((a, b) => {
    if (sortKey) {
      return a[sortKey] < b[sortKey] ? -1 : 1;
    }
    return 0;
  });

  return (
    <div style={styles.adminDashboard}>
      <div style={styles.sidebar}>
        <h2 style={styles.sidebarTitle}>Admin Dashboard</h2>
        <ul style={styles.navList}>
          <li style={styles.navItem} onClick={() => handleSectionChange('viewAssets')}>View All Assets</li>
          <li style={styles.navItem} onClick={() => handleSectionChange('viewRequests')}>View Requests</li>
          <li style={styles.navItem} onClick={() => handleSectionChange('manageAssets')}>Manage Assets</li>
        </ul>
        <button onClick={handleLogout} style={styles.logoutButton}>Logout</button>
      </div>

      <div style={styles.content}>
        <h1 style={styles.contentTitle}>Admin Dashboard</h1>

        {selectedSection === 'viewAssets' && (
          <div style={styles.section}>
            <h2 style={styles.sectionTitle}>All Assets</h2>

            <div style={styles.filterContainer}>
              <select onChange={handleSort} value={sortKey} style={styles.select}>
                <option value="">Sort by</option>
                <option value="asset_name">Name</option>
                <option value="condition">Condition</option>
                <option value="status">Status</option>
              </select>

              <select onChange={handleFilterCategory} value={filterCategory} style={styles.select}>
                <option value="">Filter by Category</option>
                <option value="1">Electronics</option>
                <option value="2">Furniture</option>
              </select>

              <select onChange={handleFilterCondition} value={filterCondition} style={styles.select}>
                <option value="">Filter by Condition</option>
                <option value="New">New</option>
                <option value="Used">Used</option>
                <option value="Damaged">Damaged</option>
              </select>
            </div>

            <div style={styles.assetGrid}>
              {sortedAssets.length > 0 ? (
                sortedAssets.map(asset => (
                  <div key={asset.id} style={styles.assetCard}>
                    <img src={asset.image_url} alt={asset.asset_name} style={styles.assetImage} />
                    <h4>{asset.asset_name}</h4>
                    <p>{asset.description}</p>
                    <span>Status: {asset.status}</span>
                  </div>
                ))
              ) : (
                <p>No assets available to display.</p>
              )}
            </div>
          </div>
        )}

        {selectedSection === 'viewRequests' && (
          <div style={styles.section}>
            <h2 style={styles.sectionTitle}>User Requests</h2>
            <table style={styles.table}>
              <thead>
                <tr>
                  <th style={styles.tableHeader}>Request Type</th>
                  <th style={styles.tableHeader}>Quantity</th>
                  <th style={styles.tableHeader}>Urgency</th>
                  <th style={styles.tableHeader}>Reason</th>
                  <th style={styles.tableHeader}>Status</th>
                  <th style={styles.tableHeader}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {requests.map((request) => (
                  <tr key={request.id}>
                    <td style={styles.tableCell}>{request.request_type}</td>
                    <td style={styles.tableCell}>{request.quantity}</td>
                    <td style={styles.tableCell}>{request.urgency}</td>
                    <td style={styles.tableCell}>{request.reason}</td>
                    <td style={styles.tableCell}>{request.status_id === 1 ? "Pending" : request.status_id === 2 ? "Approved" : "Rejected"}</td>
                    <td style={styles.tableCell}>
                      {request.status_id === 1 && (
                        <>
                          <button onClick={() => handleApprove(request.id)} style={styles.approveButton}>Approve</button>
                          <button onClick={() => handleReject(request.id)} style={styles.rejectButton}>Reject</button>
                        </>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  adminDashboard: {
    display: 'flex',
    minHeight: '100vh',
    fontFamily: 'Arial, sans-serif',
    backgroundColor: '#f4f6f8',
  },
  sidebar: {
    width: '250px',
    backgroundColor: '#2c3e50',
    color: 'white',
    padding: '20px',
    display: 'flex',
    flexDirection: 'column',
  },
  sidebarTitle: {
    fontSize: '22px',
    fontWeight: 'bold',
    marginBottom: '20px',
    color: '#ecf0f1',
  },
  navList: {
    listStyleType: 'none',
    padding: 0,
    marginBottom: 'auto',
  },
  navItem: {
    fontSize: '18px',
    cursor: 'pointer',
    padding: '10px 0',
    borderBottom: '1px solid #ecf0f1',
    transition: 'background-color 0.3s',
  },
  logoutButton: {
    backgroundColor: '#e74c3c',
    border: 'none',
    padding: '10px',
    fontSize: '16px',
    color: 'white',
    cursor: 'pointer',
    marginTop: '20px',
  },
  content: {
    flex: 1,
    padding: '20px',
    backgroundColor: 'white',
  },
  contentTitle: {
    fontSize: '30px',
    fontWeight: 'bold',
    marginBottom: '20px',
  },
  section: {
    marginBottom: '20px',
  },
  sectionTitle: {
    fontSize: '24px',
    fontWeight: 'bold',
    marginBottom: '15px',
  },
  filterContainer: {
    display: 'flex',
    gap: '15px',
    marginBottom: '20px',
  },
  select: {
    padding: '10px',
    fontSize: '16px',
    border: '1px solid #ccc',
    borderRadius: '5px',
    width: '200px',
  },
  assetGrid: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '20px',
  },
  assetCard: {
    backgroundColor: '#fff',
    padding: '15px',
    border: '1px solid #ddd',
    borderRadius: '8px',
    width: '200px',
    textAlign: 'center',
    boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
  },
  assetImage: {
    maxWidth: '100%',
    borderRadius: '8px',
    marginBottom: '10px',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
  },
  tableHeader: {
    textAlign: 'left',
    padding: '10px',
    backgroundColor: '#34495e',
    color: 'white',
  },
  tableCell: {
    padding: '10px',
    borderBottom: '1px solid #ddd',
  },
  approveButton: {
    backgroundColor: '#2ecc71',
    border: 'none',
    color: 'white',
    padding: '8px 12px',
    marginRight: '10px',
    cursor: 'pointer',
  },
  rejectButton: {
    backgroundColor: '#e74c3c',
    border: 'none',
    color: 'white',
    padding: '8px 12px',
    cursor: 'pointer',
  },
};

export default AdminDashboard;
