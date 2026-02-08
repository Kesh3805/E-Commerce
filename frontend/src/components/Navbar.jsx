import { Link, useNavigate } from 'react-router-dom';
import { useState, useEffect, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import API from '../api/axios';
import './Navbar.css';

export default function Navbar() {
  const { user, logout, isAdmin } = useAuth();
  const navigate = useNavigate();
  const [categories, setCategories] = useState([]);
  const [showCats, setShowCats] = useState(false);
  const [search, setSearch] = useState('');
  const [showMobile, setShowMobile] = useState(false);
  const catRef = useRef();

  useEffect(() => {
    API.get('/categories').then(r => setCategories(r.data.categories)).catch(() => {});
  }, []);

  // Close dropdown on outside click
  useEffect(() => {
    const handler = (e) => { if (catRef.current && !catRef.current.contains(e.target)) setShowCats(false); };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    if (search.trim()) {
      navigate(`/products?search=${encodeURIComponent(search.trim())}`);
      setSearch('');
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <span className="brand-icon">🛒</span>
          <span className="brand-text">ShopEase</span>
        </Link>

        {/* Categories Dropdown */}
        <div className="nav-categories" ref={catRef}>
          <button className="nav-cat-btn" onClick={() => setShowCats(!showCats)}>
            <span className="hamburger">☰</span> Categories
          </button>
          {showCats && (
            <div className="cat-dropdown">
              {categories.map(cat => (
                <Link
                  key={cat.id}
                  to={`/products?category_id=${cat.id}`}
                  className="cat-item"
                  onClick={() => setShowCats(false)}
                >
                  {cat.name}
                </Link>
              ))}
            </div>
          )}
        </div>

        {/* Search Bar */}
        <form className="nav-search" onSubmit={handleSearch}>
          <input
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search products, brands..."
          />
          <button type="submit" className="search-btn">🔍</button>
        </form>

        {/* Mobile toggle */}
        <button className="mobile-toggle" onClick={() => setShowMobile(!showMobile)}>☰</button>

        {/* Navigation Links */}
        <div className={`navbar-links ${showMobile ? 'show' : ''}`}>
          <Link to="/products" onClick={() => setShowMobile(false)}>Products</Link>

          {user ? (
            <>
              <Link to="/wishlist" className="nav-icon-link" onClick={() => setShowMobile(false)}>♡ Wishlist</Link>
              <Link to="/cart" className="nav-icon-link" onClick={() => setShowMobile(false)}>🛒 Cart</Link>
              <Link to="/orders" onClick={() => setShowMobile(false)}>Orders</Link>
              {isAdmin && <Link to="/admin" className="admin-link" onClick={() => setShowMobile(false)}>Admin</Link>}
              <div className="nav-user-menu">
                <Link to="/profile" className="user-badge" onClick={() => setShowMobile(false)}>
                  <span className="user-avatar">{user.name.charAt(0).toUpperCase()}</span>
                  <span className="user-name">{user.name.split(' ')[0]}</span>
                </Link>
                <button onClick={handleLogout} className="btn-logout">Logout</button>
              </div>
            </>
          ) : (
            <div className="auth-btns">
              <Link to="/login" className="btn-login">Login</Link>
              <Link to="/register" className="btn-register">Register</Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
