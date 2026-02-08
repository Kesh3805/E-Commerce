import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import API from '../api/axios';
import ProductCard from '../components/ProductCard';
import { useAuth } from '../context/AuthContext';
import { toast } from 'react-toastify';
import './Products.css';

export default function Products() {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [total, setTotal] = useState(0);
  const { user } = useAuth();
  const [searchParams, setSearchParams] = useSearchParams();

  const [filters, setFilters] = useState({
    search: searchParams.get('search') || '',
    category_id: searchParams.get('category') || '',
    sort: searchParams.get('sort') || 'newest',
    min_price: searchParams.get('min_price') || '',
    max_price: searchParams.get('max_price') || '',
    featured: searchParams.get('featured') || '',
  });

  useEffect(() => {
    API.get('/categories').then(res => setCategories(res.data.categories || res.data)).catch(() => {});
  }, []);

  const fetchProducts = async (pageNum = 1) => {
    setLoading(true);
    try {
      const params = { page: pageNum, per_page: 12 };
      if (filters.search) params.search = filters.search;
      if (filters.category_id) params.category_id = filters.category_id;
      if (filters.min_price) params.min_price = filters.min_price;
      if (filters.max_price) params.max_price = filters.max_price;
      if (filters.featured) params.featured = 'true';

      const sortMap = {
        newest: { sort_by: 'created_at', sort_order: 'desc' },
        oldest: { sort_by: 'created_at', sort_order: 'asc' },
        price_low: { sort_by: 'price', sort_order: 'asc' },
        price_high: { sort_by: 'price', sort_order: 'desc' },
        name_az: { sort_by: 'name', sort_order: 'asc' },
        name_za: { sort_by: 'name', sort_order: 'desc' },
      };
      const s = sortMap[filters.sort] || sortMap.newest;
      params.sort_by = s.sort_by;
      params.sort_order = s.sort_order;

      const res = await API.get('/products', { params });
      setProducts(res.data.products);
      setTotalPages(res.data.pages);
      setPage(res.data.current_page);
      setTotal(res.data.total);
    } catch {
      toast.error('Failed to load products');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts(1);
    // Update URL params
    const params = {};
    if (filters.search) params.search = filters.search;
    if (filters.category_id) params.category = filters.category_id;
    if (filters.sort !== 'newest') params.sort = filters.sort;
    if (filters.min_price) params.min_price = filters.min_price;
    if (filters.max_price) params.max_price = filters.max_price;
    if (filters.featured) params.featured = '1';
    setSearchParams(params, { replace: true });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters.search, filters.category_id, filters.sort, filters.min_price, filters.max_price, filters.featured]);

  const handleAddToCart = async (productId) => {
    if (!user) { toast.info('Please login to add items to cart'); return; }
    try {
      await API.post('/cart/add', { product_id: productId, quantity: 1 });
      toast.success('Added to cart!');
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to add to cart');
    }
  };

  const clearFilters = () => {
    setFilters({ search: '', category_id: '', sort: 'newest', min_price: '', max_price: '', featured: '' });
  };

  const hasActiveFilters = filters.search || filters.category_id || filters.min_price || filters.max_price || filters.featured;

  return (
    <div className="products-page">
      {/* Sidebar */}
      <aside className="products-sidebar">
        <div className="sidebar-section">
          <h3>Categories</h3>
          <ul className="cat-list">
            <li>
              <button className={!filters.category_id ? 'active' : ''} onClick={() => setFilters(f => ({ ...f, category_id: '' }))}>
                All Categories
              </button>
            </li>
            {categories.map(cat => (
              <li key={cat.id}>
                <button className={filters.category_id == cat.id ? 'active' : ''} onClick={() => setFilters(f => ({ ...f, category_id: cat.id }))}>
                  {cat.name}
                </button>
              </li>
            ))}
          </ul>
        </div>

        <div className="sidebar-section">
          <h3>Price Range</h3>
          <div className="price-inputs">
            <input type="number" placeholder="Min" value={filters.min_price} onChange={e => setFilters(f => ({ ...f, min_price: e.target.value }))} />
            <span>—</span>
            <input type="number" placeholder="Max" value={filters.max_price} onChange={e => setFilters(f => ({ ...f, max_price: e.target.value }))} />
          </div>
        </div>

        <div className="sidebar-section">
          <label className="filter-check">
            <input type="checkbox" checked={!!filters.featured} onChange={e => setFilters(f => ({ ...f, featured: e.target.checked ? '1' : '' }))} />
            <span>Featured Only</span>
          </label>
        </div>

        {hasActiveFilters && (
          <button className="btn-clear-filters" onClick={clearFilters}>Clear All Filters</button>
        )}
      </aside>

      {/* Main */}
      <div className="products-main">
        <div className="products-toolbar">
          <div className="toolbar-left">
            <h1>Products</h1>
            <span className="result-count">{total} result{total !== 1 ? 's' : ''}</span>
          </div>
          <div className="toolbar-right">
            <form className="search-form" onSubmit={e => { e.preventDefault(); fetchProducts(1); }}>
              <input type="text" placeholder="Search products..." value={filters.search} onChange={e => setFilters(f => ({ ...f, search: e.target.value }))} />
              <button type="submit">🔍</button>
            </form>
            <select className="sort-select" value={filters.sort} onChange={e => setFilters(f => ({ ...f, sort: e.target.value }))}>
              <option value="newest">Newest First</option>
              <option value="oldest">Oldest First</option>
              <option value="price_low">Price: Low → High</option>
              <option value="price_high">Price: High → Low</option>
              <option value="name_az">Name: A → Z</option>
              <option value="name_za">Name: Z → A</option>
            </select>
          </div>
        </div>

        {loading ? (
          <div className="loading">Loading products...</div>
        ) : products.length === 0 ? (
          <div className="empty-state">
            <p>No products found.</p>
            {hasActiveFilters && <button className="btn-clear-filters" onClick={clearFilters}>Clear Filters</button>}
          </div>
        ) : (
          <>
            <div className="products-grid">
              {products.map(product => (
                <ProductCard key={product.id} product={product} onAddToCart={handleAddToCart} />
              ))}
            </div>

            {totalPages > 1 && (
              <div className="pagination">
                <button disabled={page <= 1} onClick={() => fetchProducts(page - 1)}>← Prev</button>
                {Array.from({ length: Math.min(totalPages, 7) }, (_, i) => {
                  let p;
                  if (totalPages <= 7) p = i + 1;
                  else if (page <= 4) p = i + 1;
                  else if (page >= totalPages - 3) p = totalPages - 6 + i;
                  else p = page - 3 + i;
                  return (
                    <button key={p} className={p === page ? 'active' : ''} onClick={() => fetchProducts(p)}>{p}</button>
                  );
                })}
                <button disabled={page >= totalPages} onClick={() => fetchProducts(page + 1)}>Next →</button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
