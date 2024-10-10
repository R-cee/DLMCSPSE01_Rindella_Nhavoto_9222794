import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './VettingForm.css';
import Header from './HostHeader';

const VettingForm = ({ isAdmin = false }) => {
  const { user_id } = useParams();
  const navigate = useNavigate();
  const [hostType, setHostType] = useState('Individual');
  const [userRole, setUserRole] = useState('');
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    phone_number: '',
    address: '',
    document_id: null,
    business_certificate: null,
  });
  const [rejectReason, setRejectReason] = useState('');
  const [showRejectReason, setShowRejectReason] = useState(false);

  useEffect(() => {
    if (isAdmin && user_id) {
      const fetchProfile = async () => {
        try {
          const token = localStorage.getItem('jwt_token');
          const response = await fetch(`/admin/vetting/${user_id}`, {
            headers: {
              'Authorization': `Bearer ${token}`,
            },
          });
          const role = localStorage.getItem('role');
          if (role) {
            setUserRole(role);
          };
          const profile = await response.json();
          setHostType(profile.host_type);
          setFormData({
            first_name: profile.first_name || '',
            last_name: profile.last_name || '',
            phone_number: profile.phone_number || '',
            address: profile.address || '',
            document_id: profile.document_id || null,
            business_certificate: profile.business_certificate || null,
          });
        } catch (error) {
          console.error('Error fetching profile data:', error);
        }
      };

      fetchProfile();
    }
  }, [isAdmin, user_id]);

  const handleFileChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.files[0],
    });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isAdmin) {
      return; 
    }
    const data = new FormData();
    for (const key in formData) {
      data.append(key, formData[key]);
    }
    data.append('host_type', hostType);

    try {
      const token = localStorage.getItem('jwt_token'); 
      const response = await fetch('/vetting', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: data,
      });
      if (response.ok) {
        alert('Vetting information submitted successfully');
        navigate('/host-dashboard');
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.error || 'Submission failed'}`);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleUpdateStatus = async (status) => {
    const data = { status };
    if (status === 'Rejected') {
      data.reason = rejectReason;
    }

    try {
      const token = localStorage.getItem('jwt_token'); 
      const response = await fetch(`/admin/vetting/update/${user_id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(data),
      });
      if (response.ok) {
        alert(`Profile ${status.toLowerCase()} successfully`);
        navigate('/admin-dashboard');
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.error || `${status} failed`}`);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="vetting-form-container">
      <Header />
      <form onSubmit={handleSubmit}>
        <label>
          Host Type:
          <select value={hostType} onChange={(e) => setHostType(e.target.value)} disabled={isAdmin}>
            <option value="Individual">Individual</option>
            <option value="Business">Business</option>
            <option value="Organization">Organization</option>
          </select>
        </label>

        <label>
          First Name:
          <input
            type="text"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            required
            disabled={isAdmin}
          />
        </label>

        <label>
          Last Name:
          <input
            type="text"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
            required
            disabled={isAdmin}
          />
        </label>

        <label>
          Phone Number:
          <input
            type="text"
            name="phone_number"
            value={formData.phone_number}
            onChange={handleChange}
            required
            disabled={isAdmin}
          />
        </label>

        <label>
          Address:
          <input
            type="text"
            name="address"
            value={formData.address}
            onChange={handleChange}
            required
            disabled={isAdmin}
          />
        </label>

        <label>
          Government ID:
          <input
            type="file"
            name="document_id"
            onChange={handleFileChange}
            required={!isAdmin}
            disabled={isAdmin}
          />
        </label>
        {formData.document_id && (
          <div className="document-preview">
            <img src={`/uploads/ids/${formData.document_id}`} alt="Government ID" />
          </div>
        )}

        {hostType !== 'Individual' && (
          <label>
            Business Certificate:
            <input
              type="file"
              name="business_certificate"
              onChange={handleFileChange}
              disabled={isAdmin}
            />
          </label>
        )}
        {formData.business_certificate && hostType !== 'Individual' && (
          <div className="document-preview">
            <img src={`/uploads/certs/${formData.business_certificate}`} alt="Business Certificate" />
          </div>
        )}

        {!isAdmin && <button type="submit">Submit</button>}

        {isAdmin && (
          <div className="admin-actions">
            <button type="button" onClick={() => handleUpdateStatus('Approved')}>Approve</button>
            <button
              type="button"
              onClick={() => setShowRejectReason(true)}
            >
              Reject
            </button>
            {showRejectReason && (
              <div className="reject-reason">
                <textarea
                  placeholder="State the reason for rejection..."
                  value={rejectReason}
                  onChange={(e) => setRejectReason(e.target.value)}
                />
                <button type="button" onClick={() => handleUpdateStatus('Rejected')}>Submit Rejection</button>
              </div>
            )}
          </div>
        )}
      </form>
    </div>
  );
};

export default VettingForm;
