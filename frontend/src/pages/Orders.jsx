import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import API from '../api/axios';
import { toast } from 'react-toastify';
import './Orders.css';

export default function Orders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const res = await API.get('/orders');
        setOrders(res.data.orders);
      } catch {
        toast.error('Failed to load orders');
      } finally {
        setLoading(false);
      }
    };
    fetchOrders();
  }, []);

  const statusConfig = {
    PLACED: { color: '#f59e0b', bg: '#fef3c7', icon: '📋' },
    PROCESSING: { color: '#3b82f6', bg: '#dbeafe', icon: '⚙️' },
    SHIPPED: { color: '#8b5cf6', bg: '#ede9fe', icon: '🚚' },
    DELIVERED: { color: '#10b981', bg: '#d1fae5', icon: '✅' },
    CANCELLED: { color: '#ef4444', bg: '#fee2e2', icon: '❌' },
  };

  const cancelOrder = async (orderId) => {
    if (!window.confirm('Cancel this order?')) return;
    try {
      await API.put(`/orders/${orderId}/status`, { status: 'CANCELLED' });
      toast.success('Order cancelled');
      setOrders(orders.map(o => o.id === orderId ? { ...o, status: 'CANCELLED' } : o));
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to cancel');
    }
  };

  if (loading) return <div className="loading">Loading orders...</div>;

  return (
    <div className="orders-page">
      <h1>Your Orders</h1>

      {orders.length === 0 ? (
        <div className="empty-state">
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📦</div>
          <p>No orders yet</p>
          <Link to="/products" className="btn-shop">Start Shopping</Link>
        </div>
      ) : (
        <div className="orders-list">
          {orders.map((order) => {
            const sc = statusConfig[order.status] || statusConfig.PLACED;
            return (
              <div key={order.id} className="order-card">
                <div className="order-header">
                  <div className="order-meta">
                    <span className="order-id">Order #{order.id}</span>
                    <span className="order-date">{new Date(order.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })}</span>
                  </div>
                  <span className="order-status" style={{ color: sc.color, background: sc.bg }}>{sc.icon} {order.status}</span>
                </div>

                <div className="order-items">
                  {order.items.map((item) => (
                    <div key={item.id} className="order-item">
                      <Link to={`/product/${item.product_id}`} className="order-item-name">{item.product?.name || `Product #${item.product_id}`}</Link>
                      <span className="order-item-qty">×{item.quantity}</span>
                      <span className="order-item-price">${(item.price * item.quantity).toFixed(2)}</span>
                    </div>
                  ))}
                </div>

                <div className="order-details">
                  {order.payment_method && (
                    <div className="detail-chip">
                      {order.payment_method === 'COD' ? '💵' : order.payment_method === 'CARD' ? '💳' : '📱'} {order.payment_method}
                    </div>
                  )}
                  {order.coupon_code && (
                    <div className="detail-chip coupon-chip">🏷️ {order.coupon_code} (−${(order.discount_amount || 0).toFixed(2)})</div>
                  )}
                  {order.tracking_number && (
                    <div className="detail-chip">📍 {order.tracking_number}</div>
                  )}
                </div>

                <div className="order-footer">
                  <div className="order-total-section">
                    {order.discount_amount > 0 && (
                      <span className="order-subtotal">Subtotal: ${(order.subtotal || order.total_price + order.discount_amount).toFixed(2)}</span>
                    )}
                    <span className="order-total">Total: <strong>${order.total_price.toFixed(2)}</strong></span>
                  </div>
                  {order.status === 'PLACED' && (
                    <button className="btn-cancel" onClick={() => cancelOrder(order.id)}>Cancel Order</button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
