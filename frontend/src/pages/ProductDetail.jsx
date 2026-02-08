import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import API from '../api/axios';
import { useAuth } from '../context/AuthContext';
import ProductCard from '../components/ProductCard';
import './ProductDetail.css';

export default function ProductDetail() {
  const { id } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [related, setRelated] = useState([]);
  const [reviewStats, setReviewStats] = useState({});
  const [inWishlist, setInWishlist] = useState(false);
  const [quantity, setQuantity] = useState(1);
  const [activeImg, setActiveImg] = useState(0);
  const [reviewForm, setReviewForm] = useState({ rating: 5, title: '', comment: '' });
  const [showReviewForm, setShowReviewForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState('description');

  useEffect(() => {
    setLoading(true);
    API.get(`/products/${id}`)
      .then(res => {
        setProduct(res.data.product);
        setActiveImg(0);
        // Fetch related products from same category
        if (res.data.product.category_id) {
          API.get(`/products?category_id=${res.data.product.category_id}&per_page=4`)
            .then(r => setRelated(r.data.products.filter(p => p.id !== parseInt(id))));
        }
      })
      .catch(() => navigate('/'))
      .finally(() => setLoading(false));

    API.get(`/reviews/product/${id}`)
      .then(res => {
        setReviews(res.data.reviews);
        setReviewStats({
          avg: res.data.avg_rating,
          total: res.data.total_reviews,
          distribution: res.data.rating_distribution,
        });
      });

    if (user) {
      API.get(`/wishlist/check/${id}`).then(r => setInWishlist(r.data.in_wishlist)).catch(() => {});
    }
  }, [id, user]);

  const addToCart = async () => {
    if (!user) return navigate('/login');
    try {
      await API.post('/cart/add', { product_id: product.id, quantity });
      toast.success('Added to cart!');
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to add');
    }
  };

  const toggleWishlist = async () => {
    if (!user) return navigate('/login');
    try {
      if (inWishlist) {
        await API.delete(`/wishlist/remove/${product.id}`);
        setInWishlist(false);
        toast.info('Removed from wishlist');
      } else {
        await API.post('/wishlist/add', { product_id: product.id });
        setInWishlist(true);
        toast.success('Added to wishlist!');
      }
    } catch (err) {
      toast.error(err.response?.data?.error || 'Action failed');
    }
  };

  const submitReview = async (e) => {
    e.preventDefault();
    try {
      const res = await API.post('/reviews', {
        product_id: parseInt(id),
        ...reviewForm,
      });
      setReviews(prev => [res.data.review, ...prev]);
      setShowReviewForm(false);
      setReviewForm({ rating: 5, title: '', comment: '' });
      toast.success('Review submitted!');
      // Refresh stats
      API.get(`/reviews/product/${id}`).then(r => {
        setReviewStats({ avg: r.data.avg_rating, total: r.data.total_reviews, distribution: r.data.rating_distribution });
      });
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to submit review');
    }
  };

  if (loading || !product) return <div className="loading-screen"><div className="spinner" /></div>;

  const images = product.images?.length > 0 ? product.images : [product.image_url];

  return (
    <div className="product-detail">
      {/* Breadcrumb */}
      <div className="breadcrumb">
        <Link to="/">Home</Link>
        <span>/</span>
        <Link to="/products">Products</Link>
        {product.category && (
          <>
            <span>/</span>
            <Link to={`/products?category_id=${product.category_id}`}>{product.category}</Link>
          </>
        )}
        <span>/</span>
        <span className="current">{product.name}</span>
      </div>

      <div className="detail-main">
        {/* Image Gallery */}
        <div className="gallery">
          <div className="main-image">
            <img src={images[activeImg]} alt={product.name} />
            {product.discount_percent > 0 && (
              <span className="badge-discount">-{product.discount_percent}%</span>
            )}
          </div>
          {images.length > 1 && (
            <div className="thumb-row">
              {images.map((img, i) => (
                <img
                  key={i}
                  src={img}
                  alt=""
                  className={i === activeImg ? 'thumb active' : 'thumb'}
                  onClick={() => setActiveImg(i)}
                />
              ))}
            </div>
          )}
        </div>

        {/* Product Info */}
        <div className="info">
          {product.brand && <span className="brand-label">{product.brand}</span>}
          <h1>{product.name}</h1>

          <div className="rating-row">
            <div className="stars">
              {[1,2,3,4,5].map(s => (
                <span key={s} className={s <= Math.round(reviewStats.avg || 0) ? 'star filled' : 'star'}>★</span>
              ))}
            </div>
            <span className="rating-text">
              {reviewStats.avg || 0} ({reviewStats.total || 0} reviews)
            </span>
          </div>

          <div className="price-block">
            <span className="price">${product.price.toFixed(2)}</span>
            {product.compare_price && (
              <span className="compare-price">${product.compare_price.toFixed(2)}</span>
            )}
            {product.discount_percent > 0 && (
              <span className="save-badge">Save {product.discount_percent}%</span>
            )}
          </div>

          <div className={`stock-indicator ${product.stock_status}`}>
            {product.stock_status === 'in_stock' && `✓ In Stock (${product.stock} available)`}
            {product.stock_status === 'low_stock' && `⚡ Only ${product.stock} left!`}
            {product.stock_status === 'out_of_stock' && '✗ Out of Stock'}
          </div>

          {product.is_available && (
            <div className="add-section">
              <div className="qty-control">
                <button onClick={() => setQuantity(q => Math.max(1, q - 1))}>−</button>
                <span>{quantity}</span>
                <button onClick={() => setQuantity(q => Math.min(product.stock, q + 1))}>+</button>
              </div>
              <button className="btn-add-cart" onClick={addToCart}>Add to Cart</button>
              <button className={`btn-wishlist ${inWishlist ? 'active' : ''}`} onClick={toggleWishlist}>
                {inWishlist ? '♥' : '♡'}
              </button>
            </div>
          )}

          {product.sku && <p className="sku">SKU: {product.sku}</p>}
        </div>
      </div>

      {/* Tabs */}
      <div className="tabs">
        <button className={tab === 'description' ? 'tab active' : 'tab'} onClick={() => setTab('description')}>
          Description
        </button>
        <button className={tab === 'reviews' ? 'tab active' : 'tab'} onClick={() => setTab('reviews')}>
          Reviews ({reviewStats.total || 0})
        </button>
      </div>

      {tab === 'description' && (
        <div className="tab-content">
          <p className="description-text">{product.description}</p>
        </div>
      )}

      {tab === 'reviews' && (
        <div className="tab-content">
          {/* Rating Summary */}
          <div className="review-summary">
            <div className="summary-left">
              <div className="big-rating">{reviewStats.avg || 0}</div>
              <div className="stars-row">
                {[1,2,3,4,5].map(s => (
                  <span key={s} className={s <= Math.round(reviewStats.avg || 0) ? 'star filled' : 'star'}>★</span>
                ))}
              </div>
              <p>{reviewStats.total || 0} reviews</p>
            </div>
            <div className="summary-bars">
              {[5,4,3,2,1].map(n => {
                const count = reviewStats.distribution?.[String(n)] || 0;
                const pct = reviewStats.total ? (count / reviewStats.total) * 100 : 0;
                return (
                  <div key={n} className="bar-row">
                    <span>{n}★</span>
                    <div className="bar-bg"><div className="bar-fill" style={{ width: `${pct}%` }} /></div>
                    <span className="bar-count">{count}</span>
                  </div>
                );
              })}
            </div>
          </div>

          {user && !showReviewForm && (
            <button className="btn-write-review" onClick={() => setShowReviewForm(true)}>
              Write a Review
            </button>
          )}

          {showReviewForm && (
            <form className="review-form" onSubmit={submitReview}>
              <h4>Write Your Review</h4>
              <div className="form-group">
                <label>Rating</label>
                <div className="star-select">
                  {[1,2,3,4,5].map(s => (
                    <span
                      key={s}
                      className={s <= reviewForm.rating ? 'star filled clickable' : 'star clickable'}
                      onClick={() => setReviewForm(f => ({ ...f, rating: s }))}
                    >★</span>
                  ))}
                </div>
              </div>
              <div className="form-group">
                <label>Title</label>
                <input
                  value={reviewForm.title}
                  onChange={e => setReviewForm(f => ({ ...f, title: e.target.value }))}
                  placeholder="Summarize your experience"
                />
              </div>
              <div className="form-group">
                <label>Comment</label>
                <textarea
                  rows={4}
                  value={reviewForm.comment}
                  onChange={e => setReviewForm(f => ({ ...f, comment: e.target.value }))}
                  placeholder="Tell others about this product..."
                />
              </div>
              <div className="form-actions">
                <button type="submit" className="btn-submit">Submit Review</button>
                <button type="button" className="btn-cancel" onClick={() => setShowReviewForm(false)}>Cancel</button>
              </div>
            </form>
          )}

          <div className="reviews-list">
            {reviews.length === 0 && <p className="no-reviews">No reviews yet. Be the first!</p>}
            {reviews.map(r => (
              <div key={r.id} className="review-card">
                <div className="review-header">
                  <div className="stars-small">
                    {[1,2,3,4,5].map(s => (
                      <span key={s} className={s <= r.rating ? 'star filled' : 'star'}>★</span>
                    ))}
                  </div>
                  <span className="review-date">{new Date(r.created_at).toLocaleDateString()}</span>
                </div>
                <h5>{r.title}</h5>
                <p>{r.comment}</p>
                <span className="reviewer">— {r.user_name}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Related Products */}
      {related.length > 0 && (
        <section className="related-section">
          <h2>Related Products</h2>
          <div className="related-grid">
            {related.slice(0, 4).map(p => (
              <ProductCard key={p.id} product={p} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
