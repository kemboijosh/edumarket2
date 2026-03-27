function Signin() {
  return (
    <div className="container mt-4">
      <h2>Login</h2>
      <input className="form-control mb-2" placeholder="Email" />
      <input className="form-control mb-2" placeholder="Password" type="password" />
      <button className="btn btn-primary">Login</button>
    </div>
  );
}

export default Signin;