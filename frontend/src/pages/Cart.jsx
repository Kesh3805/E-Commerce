import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import API from '../api/axios';
import { toast } from 'react-toastify';
import './Cart.css';

export default function Cart() {
  const [cart, setCart] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [couponCode, setCouponCode] = useState('');
  const [couponResult, setCouponResult] = useState(null);
  const [applyingCoupon, setApplyingCoupon] = useState(false);
  const [addresses, setAddresses] = useState([]);
  const [selectedAddress, setSelectedAddress] = useState('');
  const [paymentMethod, setPaymentMethod] = useState('COD');
  const [placingOrder, setPlacingOrder] = useState(false);
  const [availableCoupons, setAvailableCoupons] = useState([]);
  const navigate = useNavigate();

  const fetchCart = async () => {
    setLoading(true);
    try {
      const res = await API.get('/cart');
      setCart(res.data.cart);
      const newTotal = res.data.total;
      setTotal(newTotal);
      
      // Revalidate coupon if applied and cart total changed
      if (couponResult && couponCode) {
        revalidateCoupon(couponCode, newTotal);
      }
    } catch {
      toast.error('Failed to load cart');
    } finally {
      setLoading(false);
    }
  };

  const fetchAddresses = async () => {
    try {
      const res = await API.get('/addresses');
      const addressData = Array.isArray(res.data) ? res.data : [];
      setAddresses(addressData);
      const def = addressData.find(a => a.is_default);
      if (def) setSelectedAddress(def.id);
    } catch (err) {
      console.error('Failed to fetch addresses:', err);
      setAddresses([]);
    }
  };

  const fetchAvailableCoupons = async () => {
    try {
      const res = await API.get('/coupons');
      setAvailableCoupons(res.data.coupons || []);
    } catch {
      // Silently fail if coupons can't be fetched
    }
  };

  useEffect(() => {
    fetchCart();
    fetchAddresses();
    fetchAvailableCoupons();
  }, []);

  const updateQuantity = async (productId, quantity) => {
    try {
      await API.put('/cart/update', { product_id: productId, quantity });
      fetchCart();
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to update');
    }
  };

  const removeItem = async (productId) => {
    try {
      await API.delete(`/cart/remove/${productId}`);
      toast.success('Item removed');
      fetchCart();
    } catch {
      toast.error('Failed to remove item');
    }
  };

  const applyCoupon = async () => {
    if (!couponCode.trim()) return;
    setApplyingCoupon(true);
    try {
      const res = await API.post('/coupons/validate', { code: couponCode, order_total: total });
      setCouponResult(res.data);
      toast.success(`Coupon applied! You save $${res.data.discount.toFixed(2)}`);
    } catch (err) {
      setCouponResult(null);
      toast.error(err.response?.data?.error || 'Invalid coupon');
    } finally {
      setApplyingCoupon(false);
    }
  };

  const revalidateCoupon = async (code, currentTotal) => {
    try {
      const res = await API.post('/coupons/validate', { code: code, order_total: currentTotal });
      setCouponResult(res.data);
    } catch {
      // Coupon no longer valid, remove it
      setCouponResult(null);
      setCouponCode('');
      toast.warning('Coupon removed: no longer valid for current cart total');
    }
  };

  const removeCoupon = () => {
    setCouponCode('');
    setCouponResult(null);
  };

  const placeOrder = async () => {
    setPlacingOrder(true);
    try {
      const body = { payment_method: paymentMethod };
      if (selectedAddress) body.address_id = selectedAddress;
      if (couponResult) body.coupon_code = couponCode;
      await API.post('/orders/place', body);
      toast.success('Order placed successfully!');
      navigate('/orders');
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to place order');
    } finally {
      setPlacingOrder(false);
    }
  };

  const finalTotal = couponResult ? couponResult.final_total : total;

  if (loading) return <div className="loading">Loading cart...</div>;

  return (
    <div className="cart-page">
      <h1>Shopping Cart <span className="cart-count">({cart.length} item{cart.length !== 1 ? 's' : ''})</span></h1>

      {cart.length === 0 ? (
        <div className="empty-state">
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🛒</div>
          <p>Your cart is empty</p>
          <Link to="/products" className="btn-primary">Browse Products</Link>
        </div>
      ) : (
        <div className="cart-layout">
          <div className="cart-items">
            {cart.map((item) => (
              <div key={item.id} className="cart-item">
                <Link to={`/product/${item.product_id}`} className="cart-item-image">
                  {item.product?.image_url ? (
                    <img src={item.product.image_url} alt={item.product.name} />
                  ) : (
                    <span>📦</span>
                  )}
                </Link>
                <div className="cart-item-info">
                  <Link to={`/product/${item.product_id}`}><h3>{item.product?.name}</h3></Link>
                  {item.product?.brand && <p className="cart-item-brand">{item.product.brand}</p>}
                  <p className="cart-item-price">${item.product?.price?.toFixed(2)} each</p>
                </div>
                <div className="cart-item-quantity">
                  <button onClick={() => updateQuantity(item.product_id, item.quantity - 1)} disabled={item.quantity <= 1}>−</button>
                  <span>{item.quantity}</span>
                  <button onClick={() => updateQuantity(item.product_id, item.quantity + 1)}>+</button>
                </div>
                <div className="cart-item-subtotal">${(item.product?.price * item.quantity).toFixed(2)}</div>
                <button className="btn-remove" onClick={() => removeItem(item.product_id)} title="Remove">✕</button>
              </div>
            ))}
          </div>

          <div className="cart-sidebar">
            {/* Coupon */}
            <div className="cart-card">
              <h3>Promo Code</h3>
              {couponResult ? (
                <div className="coupon-applied">
                  <div className="coupon-info">
                    <span className="coupon-badge">✓ {couponCode.toUpperCase()}</span>
                    <span className="coupon-savings">−${couponResult.discount.toFixed(2)}</span>
                  </div>
                  {couponResult.coupon.discount_type === 'percent' && (
                    <p className="coupon-details">{couponResult.coupon.discount_value}% off{couponResult.coupon.max_discount ? ` (max $${couponResult.coupon.max_discount})` : ''}</p>
                  )}
                  {couponResult.coupon.discount_type === 'flat' && (
                    <p className="coupon-details">${couponResult.coupon.discount_value} flat discount</p>
                  )}
                  <button className="btn-remove-coupon" onClick={removeCoupon}>Remove</button>
                </div>
              ) : (
                <div className="coupon-form">
                  <input 
                    type="text" 
              
              {!couponResult && availableCoupons.length > 0 && (
                <div className="available-coupons">
                  <p className="coupons-title">Available Coupons:</p>
                  {availableCoupons.slice(0, 4).map(coupon => (
                    <div 
                      key={coupon.id} 
                      className="coupon-chip"
                      onClick={() => {
                        setCouponCode(coupon.code);
                        setTimeout(applyCoupon, 100);
                      }}
                    >
                      <span className="chip-code">{coupon.code}</span>
                      <span className="chip-desc">
                        {coupon.discount_type === 'percent' 
                          ? `${coupon.discount_value}% off` 
                          : `$${coupon.discount_value} off`}
                        {coupon.min_order_amount > 0 && ` on $${coupon.min_order_amount}+`}
                      </span>
                    </div>
                  ))}
                </div>
              )}
                    value={couponCode} 
                    onChange={e => setCouponCode(e.target.value.toUpperCase())}
                    onKeyPress={e => e.key === 'Enter' && applyCoupon()}
                  />
                  <button onClick={applyCoupon} disabled={applyingCoupon || !couponCode.trim()}>
                    {applyingCoupon ? '...' : 'Apply'}
                  </button>
                </div>
              )}
              <p className="coupon-hint">💡 Try: WELCOME10, SAVE20, FLAT50, SUMMER25</p>
            </div>

            {/* Delivery Address */}
            <div className="cart-card">
              <h3>Delivery Address</h3>
              {addresses.length === 0 ? (
                <Link to="/profile" className="btn-add-address">+ Add Address</Link>
              ) : (
                <select value={selectedAddress} onChange={e => setSelectedAddress(e.target.value)} className="address-select">
                  <option value="">Select address</option>
                  {addresses.map(a => (
                    <option key={a.id} value={a.id}>{a.label} — {a.address_line1}, {a.city}</option>
                  ))}
                </select>
              )}
            </div>

            {/* Payment */}
            <div className="cart-card">
              <h3>Payment Method</h3>
              <div className="payment-options">
                {[
                  { value: 'COD', label: 'Cash on Delivery', icon: '💵' },
                  { value: 'CARD', label: 'Credit/Debit Card', icon: '💳' },
                  { value: 'UPI', label: 'UPI Payment', icon: '📱' },
                ].map(pm => (
                  <label key={pm.value} className={`payment-option ${paymentMethod === pm.value ? 'active' : ''}`}>
                    <input type="radio" name="payment" value={pm.value} checked={paymentMethod === pm.value} onChange={() => setPaymentMethod(pm.value)} />
                    <span className="pm-icon">{pm.icon}</span>
                    <span>{pm.label}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Summary */}
            <div className="cart-card summary-card">
              <h3>Order Summary</h3>
              <div className="summary-row"><span>Subtotal</span><span>${total.toFixed(2)}</span></div>
              {couponResult && <div className="summary-row discount"><span>Discount</span><span>−${couponResult.discount.toFixed(2)}</span></div>}
              <div className="summary-row"><span>Shipping</span><span className="free-shipping">FREE</span></div>
              <div className="summary-divider"></div>
              <div className="summary-row total-row"><span>Total</span><span>${finalTotal.toFixed(2)}</span></div>
              <button className="btn-checkout" onClick={placeOrder} disabled={placingOrder}>
                {placingOrder ? 'Placing Order...' : `Place Order — $${finalTotal.toFixed(2)}`}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
