import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { toast } from 'react-toastify';
import API from '../api/axios';
import './Wishlist.css';

export default function Wishlist() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchWishlist = () => {
    API.get('/wishlist')
      .then(res => setItems(res.data.wishlist))
      .catch(() => toast.error('Failed to load wishlist'))
      .finally(() => setLoading(false));
  };

  useEffect(fetchWishlist, []);

  const removeItem = async (productId) => {
    try {
      await API.delete(`/wishlist/remove/${productId}`);
      setItems(prev => prev.filter(i => i.product_id !== productId));
      toast.info('Removed from wishlist');
    } catch {
      toast.error('Failed to remove');
    }
  };

  const moveToCart = async (productId) => {
    try {
      await API.post(`/wishlist/move-to-cart/${productId}`);
      setItems(prev => prev.filter(i => i.product_id !== productId));
      toast.success('Moved to cart!');
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to move');
    }
  };

  if (loading) return <div className="loading-screen"><div className="spinner" /></div>;

  return (
    <div className="wishlist-page">
      <div className="page-header">
        <h1>My Wishlist</h1>
        <span className="count">{items.length} items</span>
      </div>

      {items.length === 0 ? (
        <div className="empty-state">
          <span className="empty-icon">♡</span>
          <h2>Your wishlist is empty</h2>
          <p>Save items you love to your wishlist and shop them anytime.</p>
          <Link to="/products" className="btn-shop">Start Shopping</Link>
        </div>
      ) : (
        <div className="wishlist-grid">
          {items.map(item => (
            <div key={item.id} className="wishlist-card">
              <Link to={`/product/${item.product?.id}`} className="wl-image">
                <img src={item.product?.image_url} alt={item.product?.name} />
              </Link>
              <div className="wl-info">
                <Link to={`/product/${item.product?.id}`} className="wl-name">{item.product?.name}</Link>
                {item.product?.brand && <span className="wl-brand">{item.product.brand}</span>}
                <div className="wl-price-row">
                  <span className="wl-price">${item.product?.price?.toFixed(2)}</span>
                  {item.product?.compare_price && (
                    <span className="wl-compare">${item.product.compare_price.toFixed(2)}</span>
                  )}
                </div>
                <div className={`wl-stock ${item.product?.stock_status}`}>
                  {item.product?.stock_status === 'in_stock' ? '✓ In Stock' :
                   item.product?.stock_status === 'low_stock' ? '⚡ Low Stock' : '✗ Out of Stock'}
                </div>
              </div>
              <div className="wl-actions">
                <button className="btn-move-cart" onClick={() => moveToCart(item.product_id)}>
                  Move to Cart
                </button>
                <button className="btn-remove-wl" onClick={() => removeItem(item.product_id)}>
                  Remove
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
