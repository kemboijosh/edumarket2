import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="navbar navbar-dark bg-dark p-3">
      <h3 className="text-white">EduMarket</h3>

      <div>
        <Link className="btn btn-light m-1" to="/">Home</Link>
        <Link className="btn btn-light m-1" to="/signin">Login</Link>
        <Link className="btn btn-light m-1" to="/signup">Signup</Link>
        <Link className="btn btn-warning m-1" to="/add">Add Product</Link>
      </div>
    </nav>
  );
}

export default Navbar;