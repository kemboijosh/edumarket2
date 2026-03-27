function Signup() {
  return (
    <div className="container mt-4">
      <h2>Signup</h2>
      <input className="form-control mb-2" placeholder="Username" />
      <input className="form-control mb-2" placeholder="Email" />
      <input className="form-control mb-2" placeholder="Password" type="password" />
      <button className="btn btn-success">Register</button>
    </div>
  );
}

export default Signup;