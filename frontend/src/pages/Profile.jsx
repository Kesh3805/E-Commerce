import { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import API from '../api/axios';
import { useAuth } from '../context/AuthContext';
import './Profile.css';

export default function Profile() {
  const { user, logout } = useAuth();
  const [tab, setTab] = useState('profile');
  const [profileForm, setProfileForm] = useState({ name: '', phone: '' });
  const [addresses, setAddresses] = useState([]);
  const [showAddrForm, setShowAddrForm] = useState(false);
  const [addrForm, setAddrForm] = useState({
    label: 'Home', full_name: '', phone: '', address_line1: '',
    address_line2: '', city: '', state: '', zip_code: '', country: 'US', is_default: false,
  });
  const [editAddrId, setEditAddrId] = useState(null);

  useEffect(() => {
    if (user) setProfileForm({ name: user.name, phone: user.phone || '' });
    API.get('/addresses').then(r => setAddresses(r.data.addresses)).catch(() => {});
  }, [user]);

  const saveProfile = async (e) => {
    e.preventDefault();
    try {
      await API.put('/auth/profile', profileForm);
      toast.success('Profile updated');
    } catch (err) {
      toast.error(err.response?.data?.error || 'Update failed');
    }
  };

  const saveAddress = async (e) => {
    e.preventDefault();
    try {
      if (editAddrId) {
        const res = await API.put(`/addresses/${editAddrId}`, addrForm);
        setAddresses(prev => prev.map(a => a.id === editAddrId ? res.data.address : a));
        toast.success('Address updated');
      } else {
        const res = await API.post('/addresses', addrForm);
        setAddresses(prev => [...prev, res.data.address]);
        toast.success('Address added');
      }
      setShowAddrForm(false);
      setEditAddrId(null);
      resetAddrForm();
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to save');
    }
  };

  const deleteAddress = async (id) => {
    try {
      await API.delete(`/addresses/${id}`);
      setAddresses(prev => prev.filter(a => a.id !== id));
      toast.info('Address deleted');
    } catch {
      toast.error('Failed to delete');
    }
  };

  const setDefault = async (id) => {
    try {
      await API.put(`/addresses/${id}/default`);
      setAddresses(prev => prev.map(a => ({ ...a, is_default: a.id === id })));
      toast.success('Default address updated');
    } catch {
      toast.error('Failed to update');
    }
  };

  const editAddress = (addr) => {
    setAddrForm(addr);
    setEditAddrId(addr.id);
    setShowAddrForm(true);
  };

  const resetAddrForm = () => {
    setAddrForm({
      label: 'Home', full_name: '', phone: '', address_line1: '',
      address_line2: '', city: '', state: '', zip_code: '', country: 'US', is_default: false,
    });
  };

  return (
    <div className="profile-page">
      <div className="profile-sidebar">
        <div className="profile-avatar">
          <div className="avatar-circle">{user?.name?.charAt(0).toUpperCase()}</div>
          <h3>{user?.name}</h3>
          <p>{user?.email}</p>
        </div>
        <nav className="profile-nav">
          <button className={tab === 'profile' ? 'active' : ''} onClick={() => setTab('profile')}>
            👤 Profile
          </button>
          <button className={tab === 'addresses' ? 'active' : ''} onClick={() => setTab('addresses')}>
            📍 Addresses
          </button>
          <button className="logout-btn" onClick={logout}>↪ Logout</button>
        </nav>
      </div>

      <div className="profile-content">
        {tab === 'profile' && (
          <div className="content-card">
            <h2>Personal Information</h2>
            <form onSubmit={saveProfile} className="profile-form">
              <div className="form-row">
                <div className="form-group">
                  <label>Full Name</label>
                  <input value={profileForm.name}
                    onChange={e => setProfileForm(f => ({ ...f, name: e.target.value }))} />
                </div>
                <div className="form-group">
                  <label>Email</label>
                  <input value={user?.email || ''} disabled className="disabled" />
                </div>
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Phone</label>
                  <input value={profileForm.phone}
                    onChange={e => setProfileForm(f => ({ ...f, phone: e.target.value }))}
                    placeholder="+1-555-0100" />
                </div>
                <div className="form-group">
                  <label>Role</label>
                  <input value={user?.role || ''} disabled className="disabled" />
                </div>
              </div>
              <button type="submit" className="btn-save">Save Changes</button>
            </form>
          </div>
        )}

        {tab === 'addresses' && (
          <div className="content-card">
            <div className="card-header">
              <h2>Saved Addresses</h2>
              <button className="btn-add-addr" onClick={() => { resetAddrForm(); setEditAddrId(null); setShowAddrForm(true); }}>
                + Add Address
              </button>
            </div>

            {showAddrForm && (
              <form className="addr-form" onSubmit={saveAddress}>
                <h4>{editAddrId ? 'Edit Address' : 'New Address'}</h4>
                <div className="form-row">
                  <div className="form-group">
                    <label>Label</label>
                    <select value={addrForm.label} onChange={e => setAddrForm(f => ({ ...f, label: e.target.value }))}>
                      <option>Home</option><option>Office</option><option>Other</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Full Name</label>
                    <input required value={addrForm.full_name}
                      onChange={e => setAddrForm(f => ({ ...f, full_name: e.target.value }))} />
                  </div>
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label>Phone</label>
                    <input required value={addrForm.phone}
                      onChange={e => setAddrForm(f => ({ ...f, phone: e.target.value }))} />
                  </div>
                  <div className="form-group">
                    <label>Address Line 1</label>
                    <input required value={addrForm.address_line1}
                      onChange={e => setAddrForm(f => ({ ...f, address_line1: e.target.value }))} />
                  </div>
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label>Address Line 2</label>
                    <input value={addrForm.address_line2}
                      onChange={e => setAddrForm(f => ({ ...f, address_line2: e.target.value }))} />
                  </div>
                  <div className="form-group">
                    <label>City</label>
                    <input required value={addrForm.city}
                      onChange={e => setAddrForm(f => ({ ...f, city: e.target.value }))} />
                  </div>
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label>State</label>
                    <input required value={addrForm.state}
                      onChange={e => setAddrForm(f => ({ ...f, state: e.target.value }))} />
                  </div>
                  <div className="form-group">
                    <label>ZIP Code</label>
                    <input required value={addrForm.zip_code}
                      onChange={e => setAddrForm(f => ({ ...f, zip_code: e.target.value }))} />
                  </div>
                </div>
                <div className="form-actions">
                  <button type="submit" className="btn-save">{editAddrId ? 'Update' : 'Add'} Address</button>
                  <button type="button" className="btn-cancel" onClick={() => { setShowAddrForm(false); setEditAddrId(null); }}>Cancel</button>
                </div>
              </form>
            )}

            <div className="addresses-list">
              {addresses.length === 0 && <p className="no-addr">No addresses saved yet.</p>}
              {addresses.map(addr => (
                <div key={addr.id} className={`addr-card ${addr.is_default ? 'default' : ''}`}>
                  <div className="addr-header">
                    <span className="addr-label">{addr.label}</span>
                    {addr.is_default && <span className="default-badge">Default</span>}
                  </div>
                  <p className="addr-name">{addr.full_name}</p>
                  <p>{addr.address_line1}{addr.address_line2 ? `, ${addr.address_line2}` : ''}</p>
                  <p>{addr.city}, {addr.state} {addr.zip_code}</p>
                  <p>{addr.phone}</p>
                  <div className="addr-actions">
                    <button onClick={() => editAddress(addr)}>Edit</button>
                    {!addr.is_default && <button onClick={() => setDefault(addr.id)}>Set Default</button>}
                    <button className="del" onClick={() => deleteAddress(addr.id)}>Delete</button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
