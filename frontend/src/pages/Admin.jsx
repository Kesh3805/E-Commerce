import { useState, useEffect } from 'react';
import API from '../api/axios';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import './Admin.css';

export default function Admin() {
  const { isAdmin } = useAuth();
  const navigate = useNavigate();
  const [tab, setTab] = useState('products');
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  // Product form state
  const [showForm, setShowForm] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const [form, setForm] = useState({
    name: '', description: '', price: '', stock: '', image_url: '',
  });

  useEffect(() => {
    if (!isAdmin) {
      navigate('/');
      return;
    }
    if (tab === 'products') fetchProducts();
    else fetchOrders();
  }, [tab, isAdmin]);

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const res = await API.get('/products', { params: { per_page: 50 } });
      setProducts(res.data.products);
    } catch {
      toast.error('Failed to load products');
    } finally {
      setLoading(false);
    }
  };

  const fetchOrders = async () => {
    setLoading(true);
    try {
      const res = await API.get('/orders');
      setOrders(res.data.orders);
    } catch {
      toast.error('Failed to load orders');
    } finally {
      setLoading(false);
    }
  };

  const handleFormChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const openCreateForm = () => {
    setEditingProduct(null);
    setForm({ name: '', description: '', price: '', stock: '', image_url: '' });
    setShowForm(true);
  };

  const openEditForm = (product) => {
    setEditingProduct(product);
    setForm({
      name: product.name,
      description: product.description || '',
      price: product.price.toString(),
      stock: product.stock.toString(),
      image_url: product.image_url || '',
    });
    setShowForm(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = {
      name: form.name,
      description: form.description,
      price: parseFloat(form.price),
      stock: parseInt(form.stock, 10),
      image_url: form.image_url,
    };

    try {
      if (editingProduct) {
        await API.put(`/products/${editingProduct.id}`, payload);
        toast.success('Product updated');
      } else {
        await API.post('/products', payload);
        toast.success('Product created');
      }
      setShowForm(false);
      fetchProducts();
    } catch (err) {
      toast.error(err.response?.data?.error || 'Operation failed');
    }
  };

  const deleteProduct = async (id) => {
    if (!window.confirm('Delete this product?')) return;
    try {
      await API.delete(`/products/${id}`);
      toast.success('Product deleted');
      fetchProducts();
    } catch {
      toast.error('Failed to delete product');
    }
  };

  const updateOrderStatus = async (orderId, status) => {
    try {
      await API.put(`/orders/${orderId}/status`, { status });
      toast.success('Status updated');
      fetchOrders();
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to update status');
    }
  };

  return (
    <div className="admin-page">
      <h1>Admin Panel</h1>

      <div className="admin-tabs">
        <button
          className={tab === 'products' ? 'active' : ''}
          onClick={() => setTab('products')}
        >
          Products
        </button>
        <button
          className={tab === 'orders' ? 'active' : ''}
          onClick={() => setTab('orders')}
        >
          Orders
        </button>
      </div>

      {loading ? (
        <div className="loading">Loading...</div>
      ) : tab === 'products' ? (
        <div className="admin-section">
          <div className="admin-section-header">
            <h2>Manage Products ({products.length})</h2>
            <button className="btn-primary" onClick={openCreateForm}>
              + Add Product
            </button>
          </div>

          {showForm && (
            <form className="admin-form" onSubmit={handleSubmit}>
              <h3>{editingProduct ? 'Edit Product' : 'New Product'}</h3>
              <div className="form-row">
                <div className="form-group">
                  <label>Name</label>
                  <input name="name" value={form.name} onChange={handleFormChange} required />
                </div>
                <div className="form-group">
                  <label>Price ($)</label>
                  <input name="price" type="number" step="0.01" min="0" value={form.price} onChange={handleFormChange} required />
                </div>
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Stock</label>
                  <input name="stock" type="number" min="0" value={form.stock} onChange={handleFormChange} required />
                </div>
                <div className="form-group">
                  <label>Image URL</label>
                  <input name="image_url" value={form.image_url} onChange={handleFormChange} />
                </div>
              </div>
              <div className="form-group">
                <label>Description</label>
                <textarea name="description" value={form.description} onChange={handleFormChange} rows={3} />
              </div>
              <div className="form-actions">
                <button type="submit" className="btn-primary">
                  {editingProduct ? 'Update' : 'Create'}
                </button>
                <button type="button" className="btn-secondary" onClick={() => setShowForm(false)}>
                  Cancel
                </button>
              </div>
            </form>
          )}

          <table className="admin-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Price</th>
                <th>Stock</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {products.map((p) => (
                <tr key={p.id}>
                  <td>{p.id}</td>
                  <td>{p.name}</td>
                  <td>${p.price.toFixed(2)}</td>
                  <td>{p.stock}</td>
                  <td>
                    <button className="btn-sm btn-edit" onClick={() => openEditForm(p)}>Edit</button>
                    <button className="btn-sm btn-delete" onClick={() => deleteProduct(p.id)}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="admin-section">
          <h2>Manage Orders ({orders.length})</h2>
          <table className="admin-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>User ID</th>
                <th>Total</th>
                <th>Status</th>
                <th>Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((o) => (
                <tr key={o.id}>
                  <td>{o.id}</td>
                  <td>{o.user_id}</td>
                  <td>${o.total_price.toFixed(2)}</td>
                  <td>
                    <span className={`status-badge status-${o.status.toLowerCase()}`}>
                      {o.status}
                    </span>
                  </td>
                  <td>{new Date(o.created_at).toLocaleDateString()}</td>
                  <td>
                    <select
                      value={o.status}
                      onChange={(e) => updateOrderStatus(o.id, e.target.value)}
                      className="status-select"
                    >
                      <option value="PLACED">PLACED</option>
                      <option value="SHIPPED">SHIPPED</option>
                      <option value="DELIVERED">DELIVERED</option>
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
