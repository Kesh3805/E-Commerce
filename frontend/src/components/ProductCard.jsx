import { Link } from 'react-router-dom';
import './ProductCard.css';

export default function ProductCard({ product }) {
  return (
    <Link to={`/product/${product.id}`} className="product-card">
      <div className="pc-image-wrap">
        {product.image_url ? (
          <img src={product.image_url} alt={product.name} />
        ) : (
          <div className="pc-placeholder">📦</div>
        )}
        {product.discount_percent > 0 && (
          <span className="pc-discount-badge">-{product.discount_percent}%</span>
        )}
        {product.is_featured && (
          <span className="pc-featured-badge">Featured</span>
        )}
      </div>
      <div className="pc-body">
        {product.brand && <span className="pc-brand">{product.brand}</span>}
        <h3 className="pc-name">{product.name}</h3>
        <div className="pc-price-row">
          <span className="pc-price">${product.price?.toFixed(2)}</span>
          {product.compare_price && (
            <span className="pc-compare">${product.compare_price.toFixed(2)}</span>
          )}
        </div>
        <div className="pc-bottom">
          <div className={`pc-stock ${product.stock_status}`}>
            {product.stock_status === 'in_stock' ? 'In Stock' :
             product.stock_status === 'low_stock' ? 'Low Stock' : 'Out of Stock'}
          </div>
        </div>
      </div>
    </Link>
  );
}
