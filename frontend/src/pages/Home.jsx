import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import API from '../api/axios';
import ProductCard from '../components/ProductCard';
import './Home.css';

export default function Home() {
  const [featured, setFeatured] = useState([]);
  const [deals, setDeals] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      API.get('/products/featured?limit=8'),
      API.get('/products/deals?limit=4'),
      API.get('/categories'),
    ]).then(([featRes, dealRes, catRes]) => {
      setFeatured(featRes.data.products);
      setDeals(dealRes.data.products);
      setCategories(catRes.data.categories);
    }).catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading-screen"><div className="spinner" /></div>;

  return (
    <div className="home">
      {/* Hero Banner */}
      <section className="hero">
        <div className="hero-content">
          <span className="hero-badge">New Season Collection</span>
          <h1>Discover Premium<br />Products at <span className="accent">ShopEase</span></h1>
          <p>Shop the latest tech, fashion, and lifestyle products with unbeatable prices and fast delivery.</p>
          <div className="hero-actions">
            <Link to="/products" className="btn-primary-lg">Shop Now</Link>
            <Link to="/products?featured=true" className="btn-outline-lg">View Deals</Link>
          </div>
          <div className="hero-stats">
            <div><strong>10K+</strong><span>Products</span></div>
            <div><strong>50K+</strong><span>Customers</span></div>
            <div><strong>99%</strong><span>Satisfaction</span></div>
          </div>
        </div>
        <div className="hero-visual">
          <div className="hero-floating-card card1">
            <span className="card-emoji">📱</span>
            <span>Latest Tech</span>
          </div>
          <div className="hero-floating-card card2">
            <span className="card-emoji">👟</span>
            <span>Fashion</span>
          </div>
          <div className="hero-floating-card card3">
            <span className="card-emoji">🏠</span>
            <span>Home</span>
          </div>
        </div>
      </section>

      {/* Categories Grid */}
      <section className="section">
        <div className="section-header">
          <h2>Shop by Category</h2>
          <Link to="/products" className="see-all">See All →</Link>
        </div>
        <div className="categories-grid">
          {categories.map(cat => (
            <Link to={`/products?category_id=${cat.id}`} key={cat.id} className="category-card">
              <div className="category-img-wrap">
                <img src={cat.image_url} alt={cat.name} />
                <div className="category-overlay" />
              </div>
              <div className="category-info">
                <h3>{cat.name}</h3>
                <p>{cat.description}</p>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Featured Products */}
      <section className="section">
        <div className="section-header">
          <h2>Featured Products</h2>
          <Link to="/products?featured=true" className="see-all">See All →</Link>
        </div>
        <div className="products-scroll">
          {featured.map(p => (
            <ProductCard key={p.id} product={p} />
          ))}
        </div>
      </section>

      {/* Deals Banner */}
      {deals.length > 0 && (
        <section className="deals-banner">
          <div className="deals-text">
            <span className="deals-badge">Limited Time Offers</span>
            <h2>Today's Best Deals</h2>
            <p>Save big on top-rated products. Don't miss out!</p>
          </div>
          <div className="deals-grid">
            {deals.map(p => (
              <ProductCard key={p.id} product={p} />
            ))}
          </div>
        </section>
      )}

      {/* Trust Badges */}
      <section className="trust-section">
        <div className="trust-item">
          <span className="trust-icon">🚚</span>
          <h4>Free Shipping</h4>
          <p>On orders over $50</p>
        </div>
        <div className="trust-item">
          <span className="trust-icon">🔄</span>
          <h4>Easy Returns</h4>
          <p>30-day return policy</p>
        </div>
        <div className="trust-item">
          <span className="trust-icon">🔒</span>
          <h4>Secure Payment</h4>
          <p>256-bit SSL encryption</p>
        </div>
        <div className="trust-item">
          <span className="trust-icon">💬</span>
          <h4>24/7 Support</h4>
          <p>We're always here to help</p>
        </div>
      </section>
    </div>
  );
}
